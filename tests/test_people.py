import pytest

from ravelpy import RavelryAPIError


def test_get_current_user(client, mock_api):
    mock_api.get("/current_user.json").respond(200, json={"user": {"username": "testuser"}})
    data, _etag = client.get_current_user()
    assert data["user"]["username"] == "testuser"


def test_get_person(client, mock_api):
    mock_api.get("/people/foo.json").respond(200, json={"user": {"username": "foo"}})
    data, _etag = client.get_person(username="foo")
    assert data["user"]["username"] == "foo"


def test_get_person_comments(client, mock_api):
    mock_api.get("/people/foo/comments/list.json").respond(200, json={"comments": []})
    client.get_person_comments(username="foo")


def test_get_person_comments_pagination(client, mock_api):
    mock_api.get("/people/foo/comments/list.json").respond(200, json={"comments": []})
    client.get_person_comments(username="foo", page=2, page_size=10)
    request = mock_api.calls.last.request
    url = str(request.url)
    assert "page=2" in url
    assert "page_size=10" in url


def test_get_friends(client, mock_api):
    mock_api.get("/people/foo/friends/list.json").respond(200, json={"users": []})
    client.get_friends(username="foo")


def test_get_friends_activity(client, mock_api):
    mock_api.get("/people/foo/friends/activity.json").respond(200, json={"feed": []})
    client.get_friends_activity(username="foo")


def test_get_saved_searches(client, mock_api):
    mock_api.get("/people/foo/saved_searches/list.json").respond(200, json={"saved_searches": []})
    client.get_saved_searches(username="foo")


def test_search_library(client, mock_api):
    mock_api.get("/library/foo/search.json").respond(200, json={"volumes": []})
    client.search_library(username="foo", query="lace")
    request = mock_api.calls.last.request
    assert "query=lace" in str(request.url)


def test_person_not_found(client, mock_api):
    mock_api.get("/people/nobody.json").respond(404, text="Not Found")
    with pytest.raises(RavelryAPIError) as exc_info:
        client.get_person(username="nobody")
    assert exc_info.value.status_code == 404
