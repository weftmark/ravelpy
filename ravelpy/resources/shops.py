"""Sub-client for Ravelry Shops API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ShopResponse, ShopsResponse


class Shops(Resource):
    """Wraps shop search and show endpoints.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    async def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search shops (``GET /shops/search.json``)."""
        return await self._get("/shops/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=ShopsResponse)

    async def show(self, shop_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single shop (``GET /shops/{id}.json``)."""
        return await self._get(f"/shops/{shop_id}.json", etag=etag, model=ShopResponse)
