"""Sub-client for Ravelry Packs API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import PackResponse


class Packs(Resource):
    """Wraps the pack show endpoint.

    Auth: public catalog data — accessible with the read-only Basic Auth key.  The
    endpoint is marked *authenticated* in the official docs but returns 200 in live
    testing, indicating auth is not enforced.
    """

    def show(self, pack_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single pack (``GET /packs/{id}.json``)."""
        return self._get(f"/packs/{pack_id}.json", etag=etag, model=PackResponse)


class AsyncPacks(AsyncResource):
    """Async version of :class:`Packs`."""

    async def show(self, pack_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single pack (``GET /packs/{id}.json``)."""
        return await self._get(f"/packs/{pack_id}.json", etag=etag, model=PackResponse)
