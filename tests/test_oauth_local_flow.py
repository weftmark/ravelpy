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
    appended to ``statuses``.
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

        threading.Thread(target=_run, daemon=True).start()
        return True

    return _open


def test_success_exchanges_code(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"code": "the_code", "state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock() as mock:
        route = mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
        result = oauth.local_flow(["offline"])

    assert isinstance(result, TokenResponse)
    assert result.access_token == "local_access_token"
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

    assert statuses == [404, 200]


def test_authorization_error_raises(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"error": "access_denied", "state": s})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(RuntimeError, match="access_denied"):
            oauth.local_flow(["offline"])

    assert statuses == [400]
    assert not route.called


def test_state_mismatch_raises(oauth):
    statuses: list = []
    browser = _fake_browser(oauth, lambda s: [("/callback", {"code": "c", "state": "forged"})], statuses)
    with patch("ravelpy.oauth.webbrowser.open", side_effect=browser), respx.mock(assert_all_called=False) as mock:
        route = mock.post(TOKEN_URL)
        with pytest.raises(RuntimeError, match="state_mismatch"):
            oauth.local_flow(["offline"])

    assert statuses == [400]
    assert not route.called
