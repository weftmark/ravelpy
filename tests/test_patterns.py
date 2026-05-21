import pytest

from ravelpy import RavelryAPIError


def test_get_pattern(client, mock_api):
    mock_api.get("/patterns/456.json").respond(200, json={"pattern": {"id": 456}})
    data, _etag = client.patterns.show(pattern_id=456)
    assert data["pattern"]["id"] == 456


def test_get_patterns_multi(client, mock_api):
    mock_api.get("/patterns.json").respond(200, json={"patterns": {}})
    client.patterns.list(ids="1,2,3")
    request = mock_api.calls.last.request
    assert "ids=" in str(request.url)


def test_search_patterns_with_pagination(client, mock_api):
    mock_api.get("/patterns/search.json").respond(200, json={"patterns": []})
    client.patterns.search(query="socks", page=2, page_size=50)
    request = mock_api.calls.last.request
    url = str(request.url)
    assert "query=socks" in url
    assert "page=2" in url
    assert "page_size=50" in url


def test_search_patterns_no_args(client, mock_api):
    mock_api.get("/patterns/search.json").respond(200, json={"patterns": []})
    client.patterns.search()
    request = mock_api.calls.last.request
    assert str(request.url).endswith("/patterns/search.json")


def test_get_pattern_comments(client, mock_api):
    mock_api.get("/patterns/1/comments.json").respond(200, json={"comments": []})
    client.patterns.comments(pattern_id=1)


def test_get_pattern_highlights(client, mock_api):
    mock_api.get("/patterns/highlights.json").respond(200, json={})
    client.patterns.highlights()


def test_get_pattern_projects(client, mock_api):
    mock_api.get("/patterns/1/projects.json").respond(200, json={"projects": []})
    client.patterns.projects(pattern_id=1)


def test_get_pattern_source(client, mock_api):
    mock_api.get("/pattern_sources/10.json").respond(200, json={"pattern_source": {}})
    client.pattern_sources.show(source_id=10)


def test_search_pattern_sources(client, mock_api):
    mock_api.get("/pattern_sources/search.json").respond(200, json={"pattern_sources": []})
    client.pattern_sources.search(query="vogue")
    request = mock_api.calls.last.request
    assert "query=vogue" in str(request.url)


def test_get_pattern_source_patterns(client, mock_api):
    mock_api.get("/pattern_sources/10/patterns.json").respond(200, json={"patterns": []})
    client.pattern_sources.patterns(source_id=10)


def test_pattern_error_propagates(client, mock_api):
    mock_api.get("/patterns/0.json").respond(404, text="Not Found")
    with pytest.raises(RavelryAPIError):
        client.patterns.show(pattern_id=0)
