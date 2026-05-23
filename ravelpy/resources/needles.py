"""Sub-client for Ravelry Needles API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import NeedlesResponse, NeedleSizesResponse, NeedleTypesResponse


class Needles(Resource):
    """Wraps needle list, sizes, and types endpoints.

    Auth: ``sizes`` and ``types`` are public reference data — accessible with the
    read-only Basic Auth key (both marked *authenticated* in the official docs but
    return 200 in live testing).  ``list`` (user-specific needle records) returns 403
    with the read-only key and requires a personal key or OAuth 2.0.
    """

    async def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's needle records (``GET /people/{username}/needles/list.json``)."""
        return await self._get(f"/people/{username}/needles/list.json", etag=etag, model=NeedlesResponse)

    async def sizes(self, etag: Optional[str] = None) -> ApiResult:
        """Return all needle sizes (``GET /needles/sizes.json``)."""
        return await self._get("/needles/sizes.json", etag=etag, model=NeedleSizesResponse)

    async def types(self, etag: Optional[str] = None) -> ApiResult:
        """Return all needle types (``GET /needles/types.json``)."""
        return await self._get("/needles/types.json", etag=etag, model=NeedleTypesResponse)
