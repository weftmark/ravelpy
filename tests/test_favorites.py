"""Tests for :class:`~ravelpy.resources.favorites.Favorites` resource methods."""


def test_list_favorites(client, mock_api):
    mock_api.get("/people/foo/favorites/list.json").respond(200, json={"favorites": []})
    client.favorites.list(username="foo")


def test_list_favorites_with_filters(client, mock_api):
    mock_api.get("/people/foo/favorites/list.json").respond(200, json={"favorites": []})
    client.favorites.list(username="foo", types="pattern", tag="lace", page=1, page_size=20)
    url = str(mock_api.calls.last.request.url)
    assert "types=pattern" in url
    assert "tag=lace" in url


def test_show_favorite(client, mock_api):
    mock_api.get("/people/foo/favorites/3.json").respond(200, json={"favorite": {"id": 3}})
    _, _, raw = client.favorites.show(username="foo", favorite_id=3)
    assert raw["favorite"]["id"] == 3
