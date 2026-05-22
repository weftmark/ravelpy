"""Sub-client for Ravelry Bundled Items API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import BundledItemResponse


class BundledItems(Resource):
    """Wraps the bundled item show endpoint.

    Auth: public catalog data — accessible with the read-only Basic Auth key.  The
    endpoint is marked *authenticated* in the official docs but returns 200 or 404
    in live testing, indicating auth is not enforced.
    """

    def show(self, bundled_item_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single bundled item (``GET /bundled_items/{id}.json``)."""
        return self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag, model=BundledItemResponse)


class AsyncBundledItems(AsyncResource):
    """Async version of :class:`BundledItems`."""

    async def show(self, bundled_item_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single bundled item (``GET /bundled_items/{id}.json``)."""
        return await self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag, model=BundledItemResponse)
