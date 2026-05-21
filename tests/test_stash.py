def test_list_stash(client, mock_api):
    mock_api.get("/people/foo/stash/list.json").respond(200, json={"stash": []})
    client.stash.list(username="foo")


def test_list_stash_pagination(client, mock_api):
    mock_api.get("/people/foo/stash/list.json").respond(200, json={"stash": []})
    client.stash.list(username="foo", page=2, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


def test_show_stash(client, mock_api):
    mock_api.get("/people/foo/stash/7.json").respond(200, json={"stash": {"id": 7}})
    _, _, raw = client.stash.show(username="foo", stash_id=7)
    assert raw["stash"]["id"] == 7


def test_search_stash(client, mock_api):
    mock_api.get("/stash/search.json").respond(200, json={"stash": []})
    client.stash.search(query="merino", username="foo")
    url = str(mock_api.calls.last.request.url)
    assert "query=merino" in url
    assert "username=foo" in url


def test_unified_stash(client, mock_api):
    mock_api.get("/people/foo/stash/unified/list.json").respond(200, json={"stash": []})
    client.stash.unified(username="foo")


def test_stash_comments(client, mock_api):
    mock_api.get("/people/foo/stash/7/comments.json").respond(200, json={"comments": []})
    client.stash.comments(username="foo", stash_id=7)
