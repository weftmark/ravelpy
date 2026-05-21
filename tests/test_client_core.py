import pytest
import respx
import httpx

from ravelpy import RavelryClient, RavelryAPIError

BASE = "https://api.ravelry.com"


def test_none_params_stripped(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={"color_families": []})
    client.get_color_families()
    request = mock_api.calls.last.request
    assert "None" not in str(request.url)


def test_basic_auth_sent(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={})
    client.get_color_families()
    request = mock_api.calls.last.request
    assert request.headers.get("authorization", "").startswith("Basic ")


def test_raises_ravelry_api_error_on_401(client, mock_api):
    mock_api.get("/current_user.json").respond(401, text="Unauthorized")
    with pytest.raises(RavelryAPIError) as exc_info:
        client.get_current_user()
    assert exc_info.value.status_code == 401
    assert "Unauthorized" in exc_info.value.message


def test_raises_ravelry_api_error_on_404(client, mock_api):
    mock_api.get("/patterns/999999.json").respond(404, text="Not Found")
    with pytest.raises(RavelryAPIError) as exc_info:
        client.get_pattern(pattern_id=999999)
    assert exc_info.value.status_code == 404


def test_raises_ravelry_api_error_on_500(client, mock_api):
    mock_api.get("/yarns/1.json").respond(500, text="Internal Server Error")
    with pytest.raises(RavelryAPIError) as exc_info:
        client.get_yarn(yarn_id=1)
    assert exc_info.value.status_code == 500


def test_returns_parsed_json(client, mock_api):
    payload = {"pattern": {"id": 42, "name": "Test Pattern"}}
    mock_api.get("/patterns/42.json").respond(200, json=payload)
    data, _etag = client.get_pattern(pattern_id=42)
    assert data == payload
