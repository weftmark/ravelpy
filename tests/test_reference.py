"""Tests for reference data endpoints (color families, needles, languages, etc.)."""

import pytest


@pytest.mark.asyncio
async def test_get_color_families(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={"color_families": []})
    _data, _etag, _raw = await client.extras.color_families()
    assert "color_families" in _raw


@pytest.mark.asyncio
async def test_get_yarn_weights(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(200, json={"yarn_weights": []})
    _data, _etag, _raw = await client.yarn_attributes.weights()
    assert "yarn_weights" in _raw


@pytest.mark.asyncio
async def test_get_fiber_categories(client, mock_api):
    mock_api.get("/fiber_categories.json").respond(200, json={"fiber_categories": []})
    _data, _etag, _raw = await client.fiber_attribute_groups.categories()
    assert "fiber_categories" in _raw


@pytest.mark.asyncio
async def test_get_fiber_attributes(client, mock_api):
    mock_api.get("/fiber_attributes.json").respond(200, json={"fiber_attributes": []})
    await client.fiber_attribute_groups.attributes()


@pytest.mark.asyncio
async def test_get_fiber_attribute_groups(client, mock_api):
    mock_api.get("/fiber_attribute_groups/list.json").respond(200, json={})
    await client.fiber_attribute_groups.list()


@pytest.mark.asyncio
async def test_get_yarn_attributes(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(200, json={})
    await client.yarn_attributes.groups()


@pytest.mark.asyncio
async def test_get_languages(client, mock_api):
    mock_api.get("/languages/list.json").respond(200, json={"languages": []})
    await client.languages.list()


@pytest.mark.asyncio
async def test_get_needles(client, mock_api):
    mock_api.get("/people/foo/needles/list.json").respond(200, json={"needles": []})
    await client.needles.list(username="foo")


@pytest.mark.asyncio
async def test_get_needle_sizes(client, mock_api):
    mock_api.get("/needles/sizes.json").respond(200, json={})
    await client.needles.sizes()


@pytest.mark.asyncio
async def test_get_needle_types(client, mock_api):
    mock_api.get("/needles/types.json").respond(200, json={})
    await client.needles.types()


@pytest.mark.asyncio
async def test_get_pattern_attributes(client, mock_api):
    mock_api.get("/pattern_attributes/groups.json").respond(200, json={})
    await client.pattern_attributes.groups()


@pytest.mark.asyncio
async def test_get_pattern_categories(client, mock_api):
    mock_api.get("/pattern_categories/list.json").respond(200, json={})
    await client.pattern_categories.list()


@pytest.mark.asyncio
async def test_get_pattern_source_types(client, mock_api):
    mock_api.get("/pattern_source_types/list.json").respond(200, json={})
    await client.pattern_source_types.list()


@pytest.mark.asyncio
async def test_get_project_crafts(client, mock_api):
    mock_api.get("/projects/crafts.json").respond(200, json={})
    await client.projects.crafts()


@pytest.mark.asyncio
async def test_get_project_statuses(client, mock_api):
    mock_api.get("/projects/project_statuses.json").respond(200, json={})
    await client.projects.statuses()


@pytest.mark.asyncio
async def test_get_photo_dimensions(client, mock_api):
    mock_api.get("/photos/dimensions.json").respond(200, json={})
    await client.photos.dimensions()


@pytest.mark.asyncio
async def test_get_photo_sizes(client, mock_api):
    mock_api.get("/photos/1/sizes.json").respond(200, json={})
    await client.photos.sizes(photo_id=1)
