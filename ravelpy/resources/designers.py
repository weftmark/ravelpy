"""Sub-client for Ravelry Designers API endpoints."""

from typing import Optional
from .base import ApiResult, Resource


class Designers(Resource):
    """Wraps the designer show endpoint.

    Auth: public catalog data — accessible with the read-only Basic Auth key.  The
    endpoint is marked *authenticated* in the official docs but returns 200 in live
    testing, indicating auth is not enforced.
    """

    async def show(
        self,
        designer_id: int,
        include: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a single designer (``GET /designers/{id}.json``)."""
        return await self._get(self._path("/designers/{}.json", designer_id), {"include": include}, etag=etag)
