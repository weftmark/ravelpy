"""Sub-client for Ravelry Needles API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import NeedlesResponse, NeedleSizesResponse, NeedleTypesResponse


class Needles(Resource):
    """Wraps needle list, sizes, and types endpoints.

    Auth: *authenticated* — all three endpoints require a personal key or OAuth
    2.0, including the reference endpoints ``sizes`` and ``types``.
    """

    def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's needle records (``GET /people/{username}/needles/list.json``)."""
        return self._get(f"/people/{username}/needles/list.json", etag=etag, model=NeedlesResponse)

    def sizes(self, etag: Optional[str] = None) -> ApiResult:
        """Return all needle sizes (``GET /needles/sizes.json``)."""
        return self._get("/needles/sizes.json", etag=etag, model=NeedleSizesResponse)

    def types(self, etag: Optional[str] = None) -> ApiResult:
        """Return all needle types (``GET /needles/types.json``)."""
        return self._get("/needles/types.json", etag=etag, model=NeedleTypesResponse)
