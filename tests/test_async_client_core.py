"""Tests for :class:`~ravelpy.client.AsyncRavelryClient` construction and core behaviour."""

import pytest
import respx
import httpx

from ravelpy import AsyncRavelryClient, RavelryAPIError

BASE = "https://api.ravelry.com"


@pytest.fixture
def async_client():
    return AsyncRavelryClient(username="testuser", api_key="testkey")


@pytest.mark.asyncio
async def test_async_none_params_stripped(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/color_families.json").respond(200, json={"color_families": []})
        await async_client.extras.color_families()
        request = mock.calls.last.request
        assert "None" not in str(request.url)


@pytest.mark.asyncio
async def test_async_basic_auth_sent(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/color_families.json").respond(200, json={})
        await async_client.extras.color_families()
        request = mock.calls.last.request
        assert request.headers.get("authorization", "").startswith("Basic ")


@pytest.mark.asyncio
async def test_async_raises_on_401(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/current_user.json").respond(401, text="Unauthorized")
        with pytest.raises(RavelryAPIError) as exc_info:
            await async_client.people.me()
        assert exc_info.value.status_code == 401
        assert "Unauthorized" in exc_info.value.message


@pytest.mark.asyncio
async def test_async_raises_on_404(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/patterns/999999.json").respond(404, text="Not Found")
        with pytest.raises(RavelryAPIError) as exc_info:
            await async_client.patterns.show(pattern_id=999999)
        assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_async_returns_parsed_json(async_client):
    payload = {"pattern": {"id": 42, "name": "Test Pattern"}}
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/patterns/42.json").respond(200, json=payload)
        _data, _etag, _raw = await async_client.patterns.show(pattern_id=42)
        assert _raw == payload


@pytest.mark.asyncio
async def test_async_304_returns_none_raw(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/patterns/search.json").respond(304)
        data, etag, raw = await async_client.patterns.search(query="socks", etag="abc")
        assert data is None
        assert raw is None
        assert etag == "abc"


@pytest.mark.asyncio
async def test_async_etag_sent_as_if_none_match(async_client):
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/color_families.json").respond(200, json={})
        await async_client.extras.color_families(etag='"abc123"')
        request = mock.calls.last.request
        assert request.headers.get("if-none-match") == '"abc123"'


@pytest.mark.asyncio
async def test_async_context_manager():
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/color_families.json").respond(200, json={"color_families": []})
        async with AsyncRavelryClient(username="u", api_key="k") as client:
            data, _etag, raw = await client.extras.color_families()
            assert raw == {"color_families": []}


@pytest.mark.asyncio
async def test_async_yarns_search(async_client):
    payload = {"yarns": [{"id": 1, "name": "Merino Worsted"}], "paginator": {"page": 1, "last_page": 1}}
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/yarns/search.json").respond(200, json=payload)
        _data, _etag, raw = await async_client.yarns.search(query="merino")
        assert raw == payload


@pytest.mark.asyncio
async def test_async_stash_list(async_client):
    payload = {"stash": [], "paginator": {"page": 1, "last_page": 1}}
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/people/testuser/stash/list.json").respond(200, json=payload)
        _data, _etag, raw = await async_client.stash.list(username="testuser")
        assert raw == payload


@pytest.mark.asyncio
async def test_async_from_oauth_token():
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        mock.get("/current_user.json").respond(200, json={"user": {"username": "oauthuser"}})
        client = AsyncRavelryClient.from_oauth_token("my-token")
        _data, _etag, raw = await client.people.me()
        request = mock.calls.last.request
        assert request.headers.get("authorization") == "Bearer my-token"
        await client.aclose()
