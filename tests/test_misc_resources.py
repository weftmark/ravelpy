import pytest

"""Tests for smaller resources not covered elsewhere."""
import importlib
from unittest.mock import patch
from importlib.metadata import PackageNotFoundError


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_app_config(client, mock_api):
    mock_api.get("/app/config/get.json").respond(200, json={"config": {}})
    await client.app.config()


@pytest.mark.asyncio
async def test_app_config_with_keys(client, mock_api):
    mock_api.get("/app/config/get.json").respond(200, json={"config": {}})
    await client.app.config(keys="foo,bar")
    assert "keys=foo" in str(mock_api.calls.last.request.url)


@pytest.mark.asyncio
async def test_app_data(client, mock_api):
    mock_api.get("/app/data/get.json").respond(200, json={"data": {}})
    await client.app.data()


@pytest.mark.asyncio
async def test_app_data_with_keys(client, mock_api):
    mock_api.get("/app/data/get.json").respond(200, json={"data": {}})
    await client.app.data(keys="setting1")
    assert "keys=setting1" in str(mock_api.calls.last.request.url)


# ---------------------------------------------------------------------------
# Stores
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_stores(client, mock_api):
    mock_api.get("/stores/list.json").respond(200, json={"stores": []})
    await client.stores.list()


@pytest.mark.asyncio
async def test_store_products(client, mock_api):
    mock_api.get("/stores/2/products.json").respond(200, json={"products": []})
    await client.stores.products(store_id=2)


@pytest.mark.asyncio
async def test_store_products_pagination(client, mock_api):
    mock_api.get("/stores/2/products.json").respond(200, json={"products": []})
    await client.stores.products(store_id=2, page=2, page_size=10)
    assert "page=2" in str(mock_api.calls.last.request.url)


@pytest.mark.asyncio
async def test_store_purchases(client, mock_api):
    mock_api.get("/stores/2/purchases.json").respond(200, json={"purchases": []})
    await client.stores.purchases(store_id=2)


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_groups(client, mock_api):
    mock_api.get("/groups/search.json").respond(200, json={"groups": []})
    await client.groups.search(query="knitters")
    assert "query=knitters" in str(mock_api.calls.last.request.url)


# ---------------------------------------------------------------------------
# Designers
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_show_designer(client, mock_api):
    mock_api.get("/designers/7.json").respond(200, json={"designer": {"id": 7}})
    _, _, raw = await client.designers.show(designer_id=7)
    assert raw["designer"]["id"] == 7


@pytest.mark.asyncio
async def test_show_designer_with_include(client, mock_api):
    mock_api.get("/designers/7.json").respond(200, json={"designer": {"id": 7}})
    await client.designers.show(designer_id=7, include="featured_bundles")
    assert "include=featured_bundles" in str(mock_api.calls.last.request.url)


# ---------------------------------------------------------------------------
# Bundled Items
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_show_bundled_item(client, mock_api):
    mock_api.get("/bundled_items/9.json").respond(200, json={"bundled_item": {"id": 9}})
    _, _, raw = await client.bundled_items.show(bundled_item_id=9)
    assert raw["bundled_item"]["id"] == 9


# ---------------------------------------------------------------------------
# Deliveries
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_deliveries(client, mock_api):
    mock_api.get("/deliveries/list.json").respond(200, json={"deliveries": []})
    await client.deliveries.list()


@pytest.mark.asyncio
async def test_list_deliveries_pagination(client, mock_api):
    mock_api.get("/deliveries/list.json").respond(200, json={"deliveries": []})
    await client.deliveries.list(page=2, page_size=10)
    assert "page=2" in str(mock_api.calls.last.request.url)


# ---------------------------------------------------------------------------
# Packs
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_show_pack(client, mock_api):
    mock_api.get("/packs/12.json").respond(200, json={"pack": {"id": 12}})
    _, _, raw = await client.packs.show(pack_id=12)
    assert raw["pack"]["id"] == 12


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_show_page(client, mock_api):
    mock_api.get("/pages/3.json").respond(200, json={"page": {"id": 3}})
    _, _, raw = await client.pages.show(page_id=3)
    assert raw["page"]["id"] == 3


# ---------------------------------------------------------------------------
# Volumes
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_show_volume(client, mock_api):
    mock_api.get("/volumes/10.json").respond(200, json={"volume": {"id": 10}})
    _, _, raw = await client.volumes.show(volume_id=10)
    assert raw["volume"]["id"] == 10


# ---------------------------------------------------------------------------
# Extras search
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_global_search(client, mock_api):
    mock_api.get("/search.json").respond(200, json={"results": []})
    await client.extras.search(query="linen")
    assert "query=linen" in str(mock_api.calls.last.request.url)


@pytest.mark.asyncio
async def test_global_search_with_types_and_limit(client, mock_api):
    mock_api.get("/search.json").respond(200, json={"results": []})
    await client.extras.search(query="linen", types="yarns", limit=5)
    url = str(mock_api.calls.last.request.url)
    assert "types=yarns" in url
    assert "limit=5" in url


# ---------------------------------------------------------------------------
# Photos status
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_photo_status(client, mock_api):
    mock_api.get("/photos/status.json").respond(200, json={"status": "ok"})
    await client.photos.status()


# ---------------------------------------------------------------------------
# __init__ version fallback
# ---------------------------------------------------------------------------

def test_version_fallback():
    import ravelpy
    with patch("importlib.metadata.version", side_effect=PackageNotFoundError):
        importlib.reload(ravelpy)
        assert ravelpy.__version__ == "0.0.0"
    importlib.reload(ravelpy)
