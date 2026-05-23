"""Tests for :class:`~ravelpy.client.RavelryClient` async behaviour and context manager."""

import pytest
import respx

from ravelpy import RavelryClient, RavelryAPIError

BASE = "https://api.ravelry.com"


@pytest.mark.asyncio
async def test_context_manager():
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/color_families.json").respond(200, json={"color_families": []})
        async with RavelryClient(username="u", api_key="k") as client:
            data, _etag, raw = await client.extras.color_families()
            assert raw == {"color_families": []}


@pytest.mark.asyncio
async def test_from_oauth_token(client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/current_user.json").respond(200, json={"user": {"username": "oauthuser"}})
        c = RavelryClient.from_oauth_token("my-token")
        _data, _etag, raw = await c.people.me()
        request = mock.calls.last.request
        assert request.headers.get("authorization") == "Bearer my-token"
        await c.aclose()


@pytest.mark.asyncio
async def test_304_returns_none_raw(client, mock_api):
    mock_api.get("/patterns/search.json").respond(304)
    data, etag, raw = await client.patterns.search(query="socks", etag="abc")
    assert data is None
    assert raw is None
    assert etag == "abc"


@pytest.mark.asyncio
async def test_etag_sent_as_if_none_match(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={})
    await client.extras.color_families(etag='"abc123"')
    request = mock_api.calls.last.request
    assert request.headers.get("if-none-match") == '"abc123"'
