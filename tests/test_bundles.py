"""Tests for :class:`~ravelpy.resources.bundles.Bundles` resource methods."""

import pytest


@pytest.mark.asyncio
async def test_list_bundles(client, mock_api):
    mock_api.get("/people/foo/bundles/list.json").respond(200, json={"bundles": []})
    await client.bundles.list(username="foo")


@pytest.mark.asyncio
async def test_list_bundles_with_filters(client, mock_api):
    mock_api.get("/people/foo/bundles/list.json").respond(200, json={"bundles": []})
    await client.bundles.list(username="foo", owner_types="user", query="winter", page=1, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "owner_types=user" in url
    assert "query=winter" in url


@pytest.mark.asyncio
async def test_show_bundle(client, mock_api):
    mock_api.get("/people/foo/bundles/6.json").respond(200, json={"bundle": {"id": 6}})
    _, _, raw = await client.bundles.show(username="foo", bundle_id=6)
    assert raw["bundle"]["id"] == 6
