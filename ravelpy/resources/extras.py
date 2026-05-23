"""Sub-client for miscellaneous Ravelry reference and search endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ColorFamiliesResponse


class Extras(Resource):
    """Reference data and global endpoints not scoped to a specific resource.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    async def color_families(self, etag: Optional[str] = None) -> ApiResult:
        """Return all color families (``GET /color_families.json``)."""
        return await self._get("/color_families.json", etag=etag, model=ColorFamiliesResponse)

    async def search(
        self,
        query: str,
        types: Optional[str] = None,
        limit: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Run a global cross-resource search (``GET /search.json``)."""
        return await self._get("/search.json", {"query": query, "types": types, "limit": limit}, etag=etag)
