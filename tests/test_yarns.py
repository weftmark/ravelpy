import pytest
import respx

from ravelpy import RavelryAPIError

BASE = "https://api.ravelry.com"


def test_get_yarn_hits_correct_url(client, mock_api):
    mock_api.get("/yarns/123.json").respond(200, json={"yarn": {"id": 123}})
    data, _etag = client.yarns.show(yarn_id=123)
    assert data["yarn"]["id"] == 123


def test_get_yarns_multi(client, mock_api):
    mock_api.get("/yarns.json").respond(200, json={"yarns": {}})
    client.yarns.list(ids="1,2,3")
    request = mock_api.calls.last.request
    assert "ids=1%2C2%2C3" in str(request.url) or "ids=1,2,3" in str(request.url)


def test_get_yarn_comments(client, mock_api):
    mock_api.get("/yarns/5/comments.json").respond(200, json={"comments": []})
    client.yarns.comments(yarn_id=5)


def test_search_yarns_no_args_sends_no_params(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search()
    request = mock_api.calls.last.request
    assert str(request.url).endswith("/yarns/search.json")


def test_search_yarns_with_query(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search(query="merino")
    request = mock_api.calls.last.request
    assert "query=merino" in str(request.url)


def test_search_yarns_color_family_id(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search(color_family_id=7)
    request = mock_api.calls.last.request
    assert "color_family_id=7" in str(request.url)


def test_search_yarns_fiber_category_id(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search(fiber_category_id=3)
    request = mock_api.calls.last.request
    assert "fiber_category_id=3" in str(request.url)


def test_search_yarns_discontinued(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search(discontinued=True)
    request = mock_api.calls.last.request
    assert "discontinued=True" in str(request.url) or "discontinued=true" in str(request.url)


def test_search_yarns_personal_attributes(client, mock_api):
    mock_api.get("/yarns/search.json").respond(200, json={"yarns": []})
    client.yarns.search(personal_attributes="queued")
    request = mock_api.calls.last.request
    assert "personal_attributes=queued" in str(request.url)


def test_search_yarn_companies(client, mock_api):
    mock_api.get("/yarn_companies/search.json").respond(200, json={"yarn_companies": []})
    client.yarn_companies.search(query="malabrigo")
    request = mock_api.calls.last.request
    assert "query=malabrigo" in str(request.url)


def test_yarn_error_propagates(client, mock_api):
    mock_api.get("/yarns/999.json").respond(404, text="Not Found")
    with pytest.raises(RavelryAPIError):
        client.yarns.show(yarn_id=999)
