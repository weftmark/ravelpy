"""Tests for ETag / conditional-GET behaviour across resource methods."""

import pytest
import respx
import httpx


def test_200_returns_data_and_etag(client, mock_api):
    mock_api.get("/patterns/1.json").respond(
        200,
        json={"pattern": {"id": 1}},
        headers={"ETag": '"abc123"'},
    )
    _data, etag, _raw = client.patterns.show(pattern_id=1)
    assert _raw == {"pattern": {"id": 1}}
    assert etag == '"abc123"'


def test_200_without_etag_header_returns_none_etag(client, mock_api):
    mock_api.get("/patterns/1.json").respond(200, json={"pattern": {"id": 1}})
    data, etag, _raw = client.patterns.show(pattern_id=1)
    assert data is not None
    assert etag is None


def test_304_returns_none_data_with_original_etag(client, mock_api):
    mock_api.get("/patterns/1.json").respond(304)
    data, etag, _raw = client.patterns.show(pattern_id=1, etag='"abc123"')
    assert data is None
    assert etag == '"abc123"'


def test_if_none_match_header_sent_when_etag_provided(client, mock_api):
    mock_api.get("/patterns/1.json").respond(304)
    client.patterns.show(pattern_id=1, etag='"abc123"')
    request = mock_api.calls.last.request
    assert request.headers.get("if-none-match") == '"abc123"'


def test_if_none_match_not_sent_when_no_etag(client, mock_api):
    mock_api.get("/patterns/1.json").respond(200, json={})
    client.patterns.show(pattern_id=1)
    request = mock_api.calls.last.request
    assert "if-none-match" not in request.headers


def test_etag_round_trip_yarn(client, mock_api):
    mock_api.get("/yarns/5.json").respond(
        200,
        json={"yarn": {"id": 5}},
        headers={"ETag": '"xyz999"'},
    )
    _data, etag, _raw = client.yarns.show(yarn_id=5)
    assert etag == '"xyz999"'

    mock_api.get("/yarns/5.json").respond(304)
    data2, etag2, _raw2 = client.yarns.show(yarn_id=5, etag=etag)
    assert data2 is None
    assert etag2 == '"xyz999"'


def test_etag_round_trip_reference_data(client, mock_api):
    mock_api.get("/yarn_weights.json").respond(
        200,
        json={"yarn_weights": []},
        headers={"ETag": '"weights-v1"'},
    )
    _data, etag, _raw = client.yarn_attributes.weights()
    assert etag == '"weights-v1"'

    mock_api.get("/yarn_weights.json").respond(304)
    data2, etag2, _raw2 = client.yarn_attributes.weights(etag=etag)
    assert data2 is None
    assert etag2 == '"weights-v1"'
