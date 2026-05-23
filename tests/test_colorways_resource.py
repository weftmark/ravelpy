"""Tests for :mod:`ravelpy.resources.colorways`."""

from ravelpy.models import ColorwayPhoto
from ravelpy.resources import Colorways


class TestColorwaysSubClientExists:
    def test_client_has_colorways_attribute(self, client):
        assert isinstance(client.colorways, Colorways)


class TestColorwayPhotoModel:
    def test_all_url_fields_present(self):
        p = ColorwayPhoto(
            square_url="https://images4.ravelry.com/sq.jpg",
            thumbnail_url="https://images4.ravelry.com/th.jpg",
            small_url="https://images4.ravelry.com/sm.jpg",
        )
        assert p.square_url == "https://images4.ravelry.com/sq.jpg"
        assert p.thumbnail_url == "https://images4.ravelry.com/th.jpg"
        assert p.small_url == "https://images4.ravelry.com/sm.jpg"

    def test_all_fields_optional(self):
        p = ColorwayPhoto()
        assert p.square_url is None
        assert p.thumbnail_url is None
        assert p.small_url is None
