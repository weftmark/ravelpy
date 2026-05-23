"""Tests for :class:`~ravelpy.resources.yarn_attributes.YarnAttributes` resource methods."""

import pytest

from ravelpy import RavelryAPIError


@pytest.mark.asyncio
async def test_groups_hits_correct_url(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(200, json={"yarn_attribute_groups": []})
    _data, _etag, _raw = await client.yarn_attributes.groups()
    assert "yarn_attribute_groups" in _raw


@pytest.mark.asyncio
async def test_groups_returns_etag(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(
        200, json={"yarn_attribute_groups": []}, headers={"ETag": '"attr-v1"'}
    )
    _data, etag, _raw = await client.yarn_attributes.groups()
    assert etag == '"attr-v1"'


@pytest.mark.asyncio
async def test_groups_sends_no_spurious_params(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(200, json={})
    await client.yarn_attributes.groups()
    request = mock_api.calls.last.request
    assert "None" not in str(request.url)
    assert str(request.url).endswith("/yarn_attributes/groups.json")


@pytest.mark.asyncio
async def test_weights_hits_correct_url(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(200, json={"yarn_weights": []})
    _data, _etag, _raw = await client.yarn_attributes.weights()
    assert "yarn_weights" in _raw


@pytest.mark.asyncio
async def test_weights_returns_etag(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(
        200, json={"yarn_weights": []}, headers={"ETag": '"weights-v2"'}
    )
    _data, etag, _raw = await client.yarn_attributes.weights()
    assert etag == '"weights-v2"'


@pytest.mark.asyncio
async def test_weights_304_with_etag(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(304)
    data, etag, _raw = await client.yarn_attributes.weights(etag='"weights-v2"')
    assert data is None
    assert etag == '"weights-v2"'


@pytest.mark.asyncio
async def test_groups_error_propagates(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(500, text="Server Error")
    with pytest.raises(RavelryAPIError) as exc_info:
        await client.yarn_attributes.groups()
    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_weights_error_propagates(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(401, text="Unauthorized")
    with pytest.raises(RavelryAPIError) as exc_info:
        await client.yarn_attributes.weights()
    assert exc_info.value.status_code == 401
