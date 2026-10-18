"""Tests pinning down how network-level failures reach callers.

The client currently performs no retries and does not wrap transport errors:
httpx exceptions propagate unchanged and only HTTP status failures become
:class:`~ravelpy.exceptions.RavelryAPIError`.  If retry or error-wrapping
behaviour is added, these tests should be updated deliberately alongside it.
"""

import json

import httpx
import pytest

from ravelpy import RavelryAPIError, RavelryClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError],
)
async def test_get_transport_error_propagates(client, mock_api, exc):
    route = mock_api.get("/color_families.json").mock(side_effect=exc("boom"))
    with pytest.raises(exc):
        await client.extras.color_families()
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_transport_error_is_not_api_error(client, mock_api):
    mock_api.get("/color_families.json").mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(httpx.TransportError) as excinfo:
        await client.extras.color_families()
    assert not isinstance(excinfo.value, RavelryAPIError)


@pytest.mark.asyncio
async def test_post_transport_error_propagates_without_retry(client, mock_api):
    route = mock_api.post("/people/u/stash/create.json").mock(side_effect=httpx.ConnectError("down"))
    with pytest.raises(httpx.ConnectError):
        await client.stash.create("u", {"yarn_id": 1})
    assert route.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
async def test_server_errors_raise_api_error_without_retry(client, mock_api, status):
    route = mock_api.get("/color_families.json").respond(status, text="nope")
    with pytest.raises(RavelryAPIError):
        await client.extras.color_families()
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_non_json_success_body_raises_decode_error(client, mock_api):
    mock_api.get("/color_families.json").respond(200, text="<html>maintenance</html>")
    with pytest.raises(json.JSONDecodeError):
        await client.extras.color_families()


@pytest.mark.asyncio
async def test_default_timeout_is_httpx_default():
    for c in (RavelryClient(username="u", api_key="k"), RavelryClient.from_oauth_token("t")):
        assert c._session.timeout == httpx.Timeout(5.0)
        await c.aclose()
