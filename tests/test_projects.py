"""Tests for :class:`~ravelpy.resources.projects.Projects` resource methods."""


def test_list_projects(client, mock_api):
    mock_api.get("/projects/foo/list.json").respond(200, json={"projects": []})
    client.projects.list(username="foo")


def test_list_projects_pagination(client, mock_api):
    mock_api.get("/projects/foo/list.json").respond(200, json={"projects": []})
    client.projects.list(username="foo", page=2, page_size=20)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url
    assert "page_size=20" in url


def test_show_project(client, mock_api):
    mock_api.get("/projects/foo/42.json").respond(200, json={"project": {"id": 42}})
    _, _, raw = client.projects.show(username="foo", project_id=42)
    assert raw["project"]["id"] == 42


def test_search_projects(client, mock_api):
    mock_api.get("/projects/search.json").respond(200, json={"projects": []})
    client.projects.search(query="socks", craft="knitting")
    url = str(mock_api.calls.last.request.url)
    assert "query=socks" in url
    assert "craft=knitting" in url


def test_project_comments(client, mock_api):
    mock_api.get("/projects/foo/42/comments.json").respond(200, json={"comments": []})
    client.projects.comments(username="foo", project_id=42)
