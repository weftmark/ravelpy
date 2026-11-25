"""Tests for :meth:`ravelpy.oauth.OAuthClient.local_flow` — the localhost callback server.

``webbrowser.open`` is patched to fire HTTP requests at the callback server from a
background thread, standing in for the browser redirect from Ravelry.
"""

import socket
import threading
import urllib.error
import urllib.parse
import urllib.request
from unittest.mock import patch

import pytest
import respx

from ravelpy.oauth import TOKEN_URL, OAuthClient, TokenResponse

SAMPLE_TOKEN_RESPONSE = {
    "access_token": "local_access_token",
    "token_type": "bearer",
    "expires_in": 86400,
    "refresh_token": "local_refresh_token",
    "scope": "offline",
}


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


@pytest.fixture
def oauth() -> OAuthClient:
    return OAuthClient("cid", "secret", f"http://localhost:{_free_port()}/callback")


def _fake_browser(oauth: OAuthClient, queries, statuses: list):
    """Return a ``webbrowser.open`` stand-in that hits the callback server.

    ``queries`` is a callable taking the expected state and returning a list of
    ``(path, query_dict)`` requests to send in order.  Response status codes are
    appended to ``statuses``.  ``local_flow`` can return before the thread has
    read its last response, so tests must call :func:`_wait` before asserting
    on ``statuses``.
    """
    base = oauth.redirect_uri.rsplit("/", 1)[0]

    def _open(url: str) -> bool:
        state = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["state"][0]

        def _run() -> None:
            for path, query in queries(state):
                try:
                    with urllib.request.urlopen(f"{base}{path}?{urllib.parse.urlencode(query)}", timeout=5) as r:
                        statuses.append(r.status)
                except urllib.error.HTTPError as e:
                    statuses.append(e.code)

        thread = threading.Thread(target=_run, daemon=True)
        _open.threads.append(thread)
        thread.start()
        return True

    _open.threads = []
    return _open


def _wait(browser) -> None:
    for thread in browser.threads:
        thread.join(timeout=5)
        assert not thread.is_alive()


def test_success_exchanges_code(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"code": "the_code", "state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock() as mock:
        route = mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
        result = oauth.local_flow(["offline"])

    assert isinstance(result, TokenResponse)
    assert result.access_token == "local_access_token"
    _wait(browser)
    assert statuses == [200]
    body = dict(urllib.parse.parse_qsl(route.calls.last.request.content.decode()))
    assert body["code"] == "the_code"


def test_unknown_path_returns_404_and_keeps_waiting(oauth):
    statuses: list = []
    browser = _fake_browser(
        oauth,
        lambda s: [("/favicon.ico", {}), ("/callback", {"code": "c", "state": s})],
        statuses,
    )
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock() as mock:
        mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
        oauth.local_flow(["offline"])

    _wait(browser)
    assert statuses == [404, 200]


def test_authorization_error_raises(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"error": "access_denied", "state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(RuntimeError, match="access_denied"):
            oauth.local_flow(["offline"])

    _wait(browser)
    assert statuses == [400]
    assert not route.called


@pytest.mark.parametrize(
    "bad_query",
    [
        {"code": "attacker_code", "state": "forged"},
        {"code": "attacker_code"},
        {"code": "attacker_code", "state": ""},
        {"error": "access_denied", "state": "forged"},
        {"error": "access_denied"},
    ],
    ids=["wrong-state", "missing-state", "empty-state", "error-wrong-state", "error-missing-state"],
)
def test_bad_state_is_rejected_and_keeps_waiting(oauth, bad_query):
    """A callback without the expected state gets a 400 but does not end the flow (#45)."""
    statuses: list = []
    browser = _fake_browser(
        oauth,
        lambda s: [("/callback", bad_query), ("/callback", {"code": "the_code", "state": s})],
        statuses,
    )
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock() as mock:
        route = mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
        result = oauth.local_flow(["offline"])

    assert result.access_token == "local_access_token"
    _wait(browser)
    assert statuses == [400, 200]
    assert route.call_count == 1
    body = dict(urllib.parse.parse_qsl(route.calls.last.request.content.decode()))
    assert body["code"] == "the_code"


def test_matching_state_without_code_raises(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(RuntimeError, match="missing_code"):
            oauth.local_flow(["offline"])

    _wait(browser)
    assert statuses == [400]
    assert not route.called


def test_timeout_raises_when_no_callback_arrives(oauth):
    browser = _fake_browser(oauth, lambda s: [], [])
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(TimeoutError, match="0.3 seconds"):
            oauth.local_flow(["offline"], timeout=0.3)

    assert not route.called


def test_timeout_not_reset_by_bad_state_requests(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"code": "c", "state": "forged"})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(TimeoutError):
            oauth.local_flow(["offline"], timeout=0.5)

    _wait(browser)
    assert statuses == [400]
    assert not route.called


def test_timeout_none_waits_for_callback(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"code": "the_code", "state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock() as mock:
        mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
        result = oauth.local_flow(["offline"], timeout=None)

    assert result.access_token == "local_access_token"
    _wait(browser)
    assert statuses == [200]
