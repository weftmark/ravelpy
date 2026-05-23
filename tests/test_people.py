"""Tests for :class:`~ravelpy.resources.people.People` resource methods."""

import pytest

from ravelpy import RavelryAPIError


@pytest.mark.asyncio
async def test_get_current_user(client, mock_api):
    mock_api.get("/current_user.json").respond(200, json={"user": {"username": "testuser"}})
    _data, _etag, _raw = await client.people.me()
    assert _raw["user"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_person(client, mock_api):
    mock_api.get("/people/foo.json").respond(200, json={"user": {"username": "foo"}})
    _data, _etag, _raw = await client.people.show(username="foo")
    assert _raw["user"]["username"] == "foo"


@pytest.mark.asyncio
async def test_get_person_comments(client, mock_api):
    mock_api.get("/people/foo/comments/list.json").respond(200, json={"comments": []})
    await client.people.comments(username="foo")


@pytest.mark.asyncio
async def test_get_person_comments_pagination(client, mock_api):
    mock_api.get("/people/foo/comments/list.json").respond(200, json={"comments": []})
    await client.people.comments(username="foo", page=2, page_size=10)
    request = mock_api.calls.last.request
    url = str(request.url)
    assert "page=2" in url
    assert "page_size=10" in url


@pytest.mark.asyncio
async def test_get_friends(client, mock_api):
    mock_api.get("/people/foo/friends/list.json").respond(200, json={"users": []})
    await client.friends.list(username="foo")


@pytest.mark.asyncio
async def test_get_friends_activity(client, mock_api):
    mock_api.get("/people/foo/friends/activity.json").respond(200, json={"feed": []})
    await client.friends.activity(username="foo")


@pytest.mark.asyncio
async def test_get_saved_searches(client, mock_api):
    mock_api.get("/saved_searches/list.json").respond(200, json={"saved_searches": []})
    await client.saved_searches.list()


@pytest.mark.asyncio
async def test_search_library(client, mock_api):
    mock_api.get("/people/foo/library/search.json").respond(200, json={"volumes": []})
    await client.library.search(username="foo", query="lace")
    request = mock_api.calls.last.request
    assert "query=lace" in str(request.url)


@pytest.mark.asyncio
async def test_person_not_found(client, mock_api):
    mock_api.get("/people/nobody.json").respond(404, text="Not Found")
    with pytest.raises(RavelryAPIError) as exc_info:
        await client.people.show(username="nobody")
    assert exc_info.value.status_code == 404
