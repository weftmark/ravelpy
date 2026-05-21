import pytest


def test_get_color_families(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={"color_families": []})
    _data, _etag, _raw = client.extras.color_families()
    assert "color_families" in _raw


def test_get_yarn_weights(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(200, json={"yarn_weights": []})
    _data, _etag, _raw = client.yarn_attributes.weights()
    assert "yarn_weights" in _raw


def test_get_fiber_categories(client, mock_api):
    mock_api.get("/fiber_categories.json").respond(200, json={"fiber_categories": []})
    _data, _etag, _raw = client.fiber_attribute_groups.categories()
    assert "fiber_categories" in _raw


def test_get_fiber_attributes(client, mock_api):
    mock_api.get("/fiber_attributes.json").respond(200, json={"fiber_attributes": []})
    client.fiber_attribute_groups.attributes()


def test_get_fiber_attribute_groups(client, mock_api):
    mock_api.get("/fiber_attribute_groups/list.json").respond(200, json={})
    client.fiber_attribute_groups.list()


def test_get_yarn_attributes(client, mock_api):
    mock_api.get("/yarn_attributes/groups.json").respond(200, json={})
    client.yarn_attributes.groups()


def test_get_languages(client, mock_api):
    mock_api.get("/languages/list.json").respond(200, json={"languages": []})
    client.languages.list()


def test_get_needles(client, mock_api):
    mock_api.get("/people/foo/needles/list.json").respond(200, json={"needles": []})
    client.needles.list(username="foo")


def test_get_needle_sizes(client, mock_api):
    mock_api.get("/needles/sizes.json").respond(200, json={})
    client.needles.sizes()


def test_get_needle_types(client, mock_api):
    mock_api.get("/needles/types.json").respond(200, json={})
    client.needles.types()


def test_get_pattern_attributes(client, mock_api):
    mock_api.get("/pattern_attributes/groups.json").respond(200, json={})
    client.pattern_attributes.groups()


def test_get_pattern_categories(client, mock_api):
    mock_api.get("/pattern_categories/list.json").respond(200, json={})
    client.pattern_categories.list()


def test_get_pattern_source_types(client, mock_api):
    mock_api.get("/pattern_source_types/list.json").respond(200, json={})
    client.pattern_source_types.list()


def test_get_project_crafts(client, mock_api):
    mock_api.get("/projects/crafts.json").respond(200, json={})
    client.projects.crafts()


def test_get_project_statuses(client, mock_api):
    mock_api.get("/projects/project_statuses.json").respond(200, json={})
    client.projects.statuses()


def test_get_photo_dimensions(client, mock_api):
    mock_api.get("/photos/dimensions.json").respond(200, json={})
    client.photos.dimensions()


def test_get_photo_sizes(client, mock_api):
    mock_api.get("/photos/1/sizes.json").respond(200, json={})
    client.photos.sizes(photo_id=1)
