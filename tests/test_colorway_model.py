"""Tests for :class:`~ravelpy.models.Colorway` and :class:`~ravelpy.models.ColorwayPhoto` models."""

import pytest

from ravelpy.models import Colorway, ColorwayPhoto

BASE = "https://api.ravelry.com"

FULL_COLORWAY = {
    "id": 5294540,
    "name": "Kaki",
    "code": "KAK",
    "yarn_id": 95245,
    "current_status": None,
    "projects_count": 12,
    "stashes_count": 34,
    "usage_count": 46,
    "photos": [
        {"square_url": "https://example.com/sq.jpg", "thumbnail_url": "https://example.com/th.jpg"}
    ],
}

DISCONTINUED_COLORWAY = {
    "id": 9999,
    "name": "Old Blue",
    "current_status": "discontinued",
    "photos": [],
}


class TestColorwayPhoto:
    def test_both_urls_present(self):
        p = ColorwayPhoto(square_url="https://s.jpg", thumbnail_url="https://t.jpg")
        assert p.square_url == "https://s.jpg"
        assert p.thumbnail_url == "https://t.jpg"

    def test_defaults_to_none(self):
        p = ColorwayPhoto()
        assert p.square_url is None
        assert p.thumbnail_url is None


class TestColorwayFields:
    def test_full_response_roundtrip(self):
        cw = Colorway(**FULL_COLORWAY)
        assert cw.id == 5294540
        assert cw.name == "Kaki"
        assert cw.code == "KAK"
        assert cw.yarn_id == 95245
        assert cw.current_status is None
        assert cw.projects_count == 12
        assert cw.stashes_count == 34
        assert cw.usage_count == 46

    def test_photos_parsed_as_list_of_colorway_photo(self):
        cw = Colorway(**FULL_COLORWAY)
        assert len(cw.photos) == 1
        assert isinstance(cw.photos[0], ColorwayPhoto)
        assert cw.photos[0].square_url == "https://example.com/sq.jpg"
        assert cw.photos[0].thumbnail_url == "https://example.com/th.jpg"

    def test_current_status_discontinued(self):
        cw = Colorway(**DISCONTINUED_COLORWAY)
        assert cw.current_status == "discontinued"

    def test_photos_defaults_to_empty_list(self):
        cw = Colorway(id=1)
        assert cw.photos == []

    def test_backward_compat_minimal_fields(self):
        """A dict with only id should parse without error."""
        cw = Colorway(id=42)
        assert cw.id == 42
        assert cw.current_status is None
        assert cw.photos == []

    def test_extra_api_fields_ignored(self):
        """Unknown fields from the API should not raise a ValidationError."""
        data = dict(FULL_COLORWAY, future_field="whatever")
        cw = Colorway(**data)
        assert cw.id == FULL_COLORWAY["id"]


class TestColorwayViaYarnsShow:
    def test_show_with_include_sends_param(self, client, mock_api):
        payload = {
            "yarn": {"id": 95245, "name": "8/2 Unmercerized Cotton"},
            "colorways": [FULL_COLORWAY],
        }
        mock_api.get("/yarns/95245.json").respond(200, json=payload)
        _data, _etag, raw = client.yarns.show(yarn_id=95245, include="colorways")
        request = mock_api.calls.last.request
        assert "include=colorways" in str(request.url)
        assert len(raw["colorways"]) == 1

    def test_show_without_include_colorways_is_absent(self, client, mock_api):
        payload = {"yarn": {"id": 95245, "name": "8/2 Unmercerized Cotton"}}
        mock_api.get("/yarns/95245.json").respond(200, json=payload)
        _data, _etag, raw = client.yarns.show(yarn_id=95245)
        assert "colorways" not in raw

    def test_parsed_result_colorways_populated(self, client, mock_api):
        payload = {
            "yarn": {"id": 95245, "name": "8/2 Unmercerized Cotton"},
            "colorways": [FULL_COLORWAY, DISCONTINUED_COLORWAY],
        }
        mock_api.get("/yarns/95245.json").respond(200, json=payload)
        data, _etag, _raw = client.yarns.show(yarn_id=95245, include="colorways")
        assert data.colorways is not None
        assert len(data.colorways) == 2
        active = [c for c in data.colorways if c.current_status is None]
        discontinued = [c for c in data.colorways if c.current_status == "discontinued"]
        assert len(active) == 1
        assert len(discontinued) == 1
