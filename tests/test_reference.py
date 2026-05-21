import pytest


def test_get_color_families(client, mock_api):
    mock_api.get("/color_families.json").respond(200, json={"color_families": []})
    data, _etag = client.get_color_families()
    assert "color_families" in data


def test_get_yarn_weights(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(200, json={"yarn_weights": []})
    data, _etag = client.get_yarn_weights()
    assert "yarn_weights" in data


def test_get_fiber_categories(client, mock_api):
    mock_api.get("/fiber_categories.json").respond(200, json={"fiber_categories": []})
    data, _etag = client.get_fiber_categories()
    assert "fiber_categories" in data


def test_get_fiber_attributes(client, mock_api):
    mock_api.get("/fiber_attributes.json").respond(200, json={"fiber_attributes": []})
    client.get_fiber_attributes()


def test_get_fiber_attribute_groups(client, mock_api):
    mock_api.get("/fiber_attribute_groups/list.json").respond(200, json={})
    client.get_fiber_attribute_groups()


def test_get_yarn_attributes(client, mock_api):
    mock_api.get("/yarn_attributes/list.json").respond(200, json={})
    client.get_yarn_attributes()


def test_get_languages(client, mock_api):
    mock_api.get("/languages/languages.json").respond(200, json={"languages": []})
    client.get_languages()


def test_get_needles(client, mock_api):
    mock_api.get("/needles/list.json").respond(200, json={"needles": []})
    client.get_needles()


def test_get_needle_sizes(client, mock_api):
    mock_api.get("/needles/sizes.json").respond(200, json={})
    client.get_needle_sizes()


def test_get_needle_types(client, mock_api):
    mock_api.get("/needles/types.json").respond(200, json={})
    client.get_needle_types()


def test_get_pattern_attributes(client, mock_api):
    mock_api.get("/pattern_attributes/list.json").respond(200, json={})
    client.get_pattern_attributes()


def test_get_pattern_categories(client, mock_api):
    mock_api.get("/pattern_categories/list.json").respond(200, json={})
    client.get_pattern_categories()


def test_get_pattern_source_types(client, mock_api):
    mock_api.get("/pattern_source_types/list.json").respond(200, json={})
    client.get_pattern_source_types()


def test_get_project_crafts(client, mock_api):
    mock_api.get("/projects/crafts.json").respond(200, json={})
    client.get_project_crafts()


def test_get_project_statuses(client, mock_api):
    mock_api.get("/projects/project_statuses.json").respond(200, json={})
    client.get_project_statuses()


def test_get_photo_dimensions(client, mock_api):
    mock_api.get("/photos/dimensions.json").respond(200, json={})
    client.get_photo_dimensions()


def test_get_photo_sizes(client, mock_api):
    mock_api.get("/photos/sizes.json").respond(200, json={})
    client.get_photo_sizes()
