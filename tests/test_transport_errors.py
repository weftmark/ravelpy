"""Tests for how network-level failures and timeouts reach callers.

Transport failures are re-raised as :class:`~ravelpy.exceptions.RavelryConnectionError`
(which is also an :class:`httpx.TransportError`); HTTP status failures and
non-JSON bodies become :class:`~ravelpy.exceptions.RavelryAPIError`.  No
retries are performed unless explicitly configured.
"""

import httpx
import pytest

from ravelpy import RavelryAPIError, RavelryClient, RavelryConnectionError, RavelryError
from ravelpy.client import DEFAULT_TIMEOUT
from ravelpy.resources.base import _send


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc, is_timeout",
    [
        (httpx.ConnectTimeout, True),
        (httpx.ReadTimeout, True),
        (httpx.ConnectError, False),
        (httpx.RemoteProtocolError, False),
    ],
)
async def test_get_transport_error_wrapped(client, mock_api, exc, is_timeout):
    route = mock_api.get("/color_families.json").mock(side_effect=exc("boom"))
    with pytest.raises(RavelryConnectionError) as excinfo:
        await client.extras.color_families()
    assert isinstance(excinfo.value.__cause__, exc)
    assert excinfo.value.is_timeout is is_timeout
    assert "boom" in str(excinfo.value)
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_connection_error_is_still_httpx_transport_error(client, mock_api):
    mock_api.get("/color_families.json").mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(httpx.TransportError) as excinfo:
        await client.extras.color_families()
    assert isinstance(excinfo.value, RavelryError)
    assert not isinstance(excinfo.value, RavelryAPIError)


@pytest.mark.asyncio
async def test_connection_error_keeps_request(client, mock_api):
    mock_api.get("/color_families.json").mock(side_effect=httpx.ConnectError("down"))
    with pytest.raises(RavelryConnectionError) as excinfo:
        await client.extras.color_families()
    assert excinfo.value.request.url.path == "/color_families.json"


@pytest.mark.asyncio
async def test_post_transport_error_wrapped_without_retry(client, mock_api):
    route = mock_api.post("/people/u/stash/create.json").mock(side_effect=httpx.ConnectError("down"))
    with pytest.raises(RavelryConnectionError):
        await client.stash.create("u", {"yarn_id": 1})
    assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
async def test_server_errors_raise_api_error_without_retry(client, mock_api, status):
    route = mock_api.get("/color_families.json").respond(status, text="nope")
    with pytest.raises(RavelryAPIError) as excinfo:
        await client.extras.color_families()
    assert isinstance(excinfo.value, RavelryError)
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_non_json_success_body_raises_api_error(client, mock_api):
    mock_api.get("/color_families.json").respond(200, text="<html>maintenance</html>")
    with pytest.raises(RavelryAPIError) as excinfo:
        await client.extras.color_families()
    assert excinfo.value.status_code == 200
    assert "<html>maintenance</html>" in excinfo.value.message


@pytest.mark.asyncio
async def test_default_timeout_unchanged():
    assert DEFAULT_TIMEOUT == 5.0
    for c in (RavelryClient(username="u", api_key="k"), RavelryClient.from_oauth_token("t")):
        assert c._session.timeout == httpx.Timeout(5.0)
        await c.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "timeout, expected",
    [
        (30.0, httpx.Timeout(30.0)),
        (httpx.Timeout(10.0, connect=2.0), httpx.Timeout(10.0, connect=2.0)),
        (None, httpx.Timeout(None)),
    ],
)
async def test_custom_timeout_reaches_session(timeout, expected):
    for c in (
        RavelryClient(username="u", api_key="k", timeout=timeout),
        RavelryClient.from_oauth_token("t", timeout=timeout),
    ):
        assert c._session.timeout == expected
        await c.aclose()


@pytest.mark.asyncio
async def test_from_oauth_token_with_timeout_still_sends_bearer(mock_api):
    mock_api.get("/current_user.json").respond(200, json={"user": {}})
    c = RavelryClient.from_oauth_token("tok", timeout=12)
    await c.people.me()
    assert mock_api.calls.last.request.headers["authorization"] == "Bearer tok"
    await c.aclose()


@pytest.mark.asyncio
async def test_send_tolerates_error_without_request():
    # httpx raises RuntimeError from ``.request`` when none is attached.
    async def _fail():
        raise httpx.ConnectError("no request attached")

    with pytest.raises(RavelryConnectionError) as excinfo:
        await _send(_fail())
    with pytest.raises(RuntimeError):
        _ = excinfo.value.request
