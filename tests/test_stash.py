"""Tests for :class:`~ravelpy.resources.stash.Stash` resource methods."""

import pytest


@pytest.mark.asyncio
async def test_list_stash(client, mock_api):
    mock_api.get("/people/foo/stash/list.json").respond(200, json={"stash": []})
    await client.stash.list(username="foo")


@pytest.mark.asyncio
async def test_list_stash_pagination(client, mock_api):
    mock_api.get("/people/foo/stash/list.json").respond(200, json={"stash": []})
    await client.stash.list(username="foo", page=2, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


@pytest.mark.asyncio
async def test_show_stash(client, mock_api):
    mock_api.get("/people/foo/stash/7.json").respond(200, json={"stash": {"id": 7}})
    _, _, raw = await client.stash.show(username="foo", stash_id=7)
    assert raw["stash"]["id"] == 7


@pytest.mark.asyncio
async def test_search_stash(client, mock_api):
    mock_api.get("/stash/search.json").respond(200, json={"stash": []})
    await client.stash.search(query="merino", username="foo")
    url = str(mock_api.calls.last.request.url)
    assert "query=merino" in url
    assert "username=foo" in url


@pytest.mark.asyncio
async def test_unified_stash(client, mock_api):
    mock_api.get("/people/foo/stash/unified/list.json").respond(200, json={"stash": []})
    await client.stash.unified(username="foo")


@pytest.mark.asyncio
async def test_stash_comments(client, mock_api):
    mock_api.get("/people/foo/stash/7/comments.json").respond(200, json={"comments": []})
    await client.stash.comments(username="foo", stash_id=7)
