"""Tests for :class:`~ravelpy.resources.shops.Shops` resource methods."""

import pytest


@pytest.mark.asyncio
async def test_search_shops(client, mock_api):
    mock_api.get("/shops/search.json").respond(200, json={"shops": []})
    await client.shops.search(query="wool")
    assert "query=wool" in str(mock_api.calls.last.request.url)


@pytest.mark.asyncio
async def test_show_shop(client, mock_api):
    mock_api.get("/shops/8.json").respond(200, json={"shop": {"id": 8}})
    _, _, raw = await client.shops.show(shop_id=8)
    assert raw["shop"]["id"] == 8
