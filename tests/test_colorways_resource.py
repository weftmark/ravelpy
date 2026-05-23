"""Tests for :class:`~ravelpy.resources.colorways.Colorways` resource methods."""

import pytest
import respx

from ravelpy import RavelryAPIError
from ravelpy.models import ColorwayPhoto

BASE = "https://api.ravelry.com"

PHOTO_PAYLOAD = {
    "square_url": "https://images4.ravelry.com/sq.jpg",
    "thumbnail_url": "https://images4.ravelry.com/th.jpg",
    "small_url": "https://images4.ravelry.com/sm.jpg",
}


class TestGetPhoto:
    def test_returns_colorway_photo_when_present(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(
            200,
            json={"projects": [{"first_photo": PHOTO_PAYLOAD}], "paginator": {"page": 1}},
        )
        photo = client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        assert isinstance(photo, ColorwayPhoto)
        assert photo.square_url == PHOTO_PAYLOAD["square_url"]
        assert photo.thumbnail_url == PHOTO_PAYLOAD["thumbnail_url"]
        assert photo.small_url == PHOTO_PAYLOAD["small_url"]

    def test_returns_none_when_first_photo_is_null(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(
            200,
            json={"projects": [{"first_photo": None}], "paginator": {"page": 1}},
        )
        photo = client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        assert photo is None

    def test_returns_none_when_first_photo_absent(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(
            200,
            json={"projects": [{}], "paginator": {"page": 1}},
        )
        photo = client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        assert photo is None

    def test_returns_none_when_projects_empty(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(
            200,
            json={"projects": [], "paginator": {"page": 1}},
        )
        photo = client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        assert photo is None

    def test_sends_correct_query_params(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(
            200, json={"projects": [], "paginator": {"page": 1}}
        )
        client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        url = str(mock_api.calls.last.request.url)
        assert "yarn_id=95245" in url
        assert "colorway_id=5294540" in url
        assert "page_size=1" in url

    def test_raises_on_http_error(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(401, text="Unauthorized")
        with pytest.raises(RavelryAPIError) as exc_info:
            client.colorways.get_photo(yarn_id=95245, colorway_id=5294540)
        assert exc_info.value.status_code == 401

    def test_raises_on_404(self, client, mock_api):
        mock_api.get("/projects/search.json").respond(404, text="Not Found")
        with pytest.raises(RavelryAPIError):
            client.colorways.get_photo(yarn_id=0, colorway_id=0)


class TestColorwayPhotoModel:
    def test_all_url_fields_present(self):
        p = ColorwayPhoto(**PHOTO_PAYLOAD)
        assert p.square_url == PHOTO_PAYLOAD["square_url"]
        assert p.thumbnail_url == PHOTO_PAYLOAD["thumbnail_url"]
        assert p.small_url == PHOTO_PAYLOAD["small_url"]

    def test_small_url_defaults_to_none(self):
        p = ColorwayPhoto(square_url="https://s.jpg", thumbnail_url="https://t.jpg")
        assert p.small_url is None

    def test_all_fields_optional(self):
        p = ColorwayPhoto()
        assert p.square_url is None
        assert p.thumbnail_url is None
        assert p.small_url is None


class TestColorwayPhotosFieldUnpopulated:
    """Regression: Colorway.photos is always empty from the yarn embed."""

    def test_yarn_embed_colorways_photos_empty(self, client, mock_api):
        payload = {
            "yarn": {"id": 95245, "name": "8/2 Unmercerized Cotton"},
            "colorways": [
                {"id": 5294540, "name": "Kaki", "yarn_id": 95245},
            ],
        }
        mock_api.get("/yarns/95245.json").respond(200, json=payload)
        data, _etag, _raw = client.yarns.show(yarn_id=95245, include="colorways")
        assert data.colorways[0].photos == []
