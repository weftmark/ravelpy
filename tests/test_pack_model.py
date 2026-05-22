"""Tests for Pack model fields and Stash.total_skeins property."""

from ravelpy.models import Pack, Stash


def _pack(**kwargs):
    return {"id": 1, **kwargs}


class TestPackFields:
    def test_skeins_parsed(self):
        p = Pack(**_pack(skeins=2.5))
        assert p.skeins == 2.5

    def test_primary_pack_id_none_on_primary(self):
        p = Pack(**_pack(primary_pack_id=None))
        assert p.primary_pack_id is None

    def test_primary_pack_id_set_on_secondary(self):
        p = Pack(**_pack(primary_pack_id=42))
        assert p.primary_pack_id == 42

    def test_totals_parsed(self):
        p = Pack(**_pack(total_yards=400.0, total_meters=365.8, total_grams=100.0, total_ounces=3.5))
        assert p.total_yards == 400.0
        assert p.total_meters == 365.8
        assert p.total_grams == 100.0
        assert p.total_ounces == 3.5

    def test_per_skein_fields_parsed(self):
        p = Pack(**_pack(yards_per_skein=200.0, meters_per_skein=182.9,
                         grams_per_skein=50.0, ounces_per_skein=1.76))
        assert p.yards_per_skein == 200.0
        assert p.grams_per_skein == 50.0

    def test_quantity_description(self):
        p = Pack(**_pack(quantity_description="2 skeins = 400 yards"))
        assert p.quantity_description == "2 skeins = 400 yards"

    def test_shop_fields(self):
        p = Pack(**_pack(shop_name="Gauge & Twist", shop_id=99))
        assert p.shop_name == "Gauge & Twist"
        assert p.shop_id == 99

    def test_preference_flags(self):
        p = Pack(**_pack(prefer_metric_weight=True, prefer_metric_length=False))
        assert p.prefer_metric_weight is True
        assert p.prefer_metric_length is False

    def test_color_attributes_list(self):
        p = Pack(**_pack(color_attributes=[{"id": 1, "name": "Red"}]))
        assert len(p.color_attributes) == 1

    def test_optional_fields_default_none(self):
        p = Pack(id=1)
        assert p.skeins is None
        assert p.total_yards is None
        assert p.primary_pack_id is None
        assert p.color_attributes is None


class TestStashTotalSkeins:
    def _stash(self, packs):
        return Stash(id=1, packs=packs)

    def test_sums_primary_packs(self):
        packs = [
            Pack(**_pack(id=1, skeins=2.0, primary_pack_id=None)),
            Pack(**_pack(id=2, skeins=1.0, primary_pack_id=None)),
        ]
        assert self._stash(packs).total_skeins == 3.0

    def test_excludes_secondary_packs(self):
        packs = [
            Pack(**_pack(id=1, skeins=2.0, primary_pack_id=None)),
            Pack(**_pack(id=2, skeins=1.0, primary_pack_id=1)),  # secondary
        ]
        assert self._stash(packs).total_skeins == 2.0

    def test_skips_packs_with_no_skeins(self):
        packs = [
            Pack(**_pack(id=1, skeins=3.0, primary_pack_id=None)),
            Pack(**_pack(id=2, skeins=None, primary_pack_id=None)),
        ]
        assert self._stash(packs).total_skeins == 3.0

    def test_returns_none_when_no_packs(self):
        assert self._stash(packs=None).total_skeins is None

    def test_returns_none_when_no_skein_data(self):
        packs = [Pack(**_pack(id=1, skeins=None, primary_pack_id=None))]
        assert self._stash(packs).total_skeins is None

    def test_fractional_skeins(self):
        packs = [Pack(**_pack(id=1, skeins=1.5, primary_pack_id=None))]
        assert self._stash(packs).total_skeins == 1.5
