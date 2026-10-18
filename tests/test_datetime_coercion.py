"""Tests for Ravelry's non-ISO datetime format handling in :mod:`ravelpy.models`."""

from datetime import datetime, timedelta, timezone

import pytest

from ravelpy.models import DownloadLink, _coerce_ravelry_datetime


class TestCoerceRavelryDatetime:
    def test_slashes_and_offset_normalized(self):
        assert _coerce_ravelry_datetime("2026/05/21 14:30:00 -0400") == "2026-05-21 14:30:00-04:00"

    def test_positive_offset(self):
        assert _coerce_ravelry_datetime("2026/05/21 14:30:00 +0530") == "2026-05-21 14:30:00+05:30"

    def test_iso_string_unchanged(self):
        assert _coerce_ravelry_datetime("2026-05-21T14:30:00+00:00") == "2026-05-21T14:30:00+00:00"

    def test_non_string_passed_through(self):
        dt = datetime(2026, 5, 21)
        assert _coerce_ravelry_datetime(dt) is dt
        assert _coerce_ravelry_datetime(None) is None


class TestRavelryDatetimeField:
    def test_model_parses_ravelry_format(self):
        link = DownloadLink.model_validate({"activated_at": "2026/05/21 14:30:00 -0400"})
        assert link.activated_at == datetime(2026, 5, 21, 14, 30, tzinfo=timezone(timedelta(hours=-4)))

    def test_model_accepts_iso_format(self):
        link = DownloadLink.model_validate({"expires_at": "2026-05-21T14:30:00Z"})
        assert link.expires_at == datetime(2026, 5, 21, 14, 30, tzinfo=timezone.utc)

    def test_model_rejects_garbage(self):
        with pytest.raises(ValueError):
            DownloadLink.model_validate({"activated_at": "not a date"})
