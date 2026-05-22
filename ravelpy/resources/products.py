"""Sub-client for Ravelry Products API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import ProductAttachmentsResponse, ProductResponse


class Products(Resource):
    """Wraps product show and attachments endpoints.

    Auth: *authenticated* — requires a personal key or OAuth 2.0; the read-only
    Basic Auth key cannot call these endpoints.

    The ``products/loveknitting/export`` write operation requires ``patternstore-pdf``
    OAuth scope per API docs; not yet implemented in this library.
    """

    def show(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single product (``GET /products/{id}.json``).

        TODO: returns 403 for all tested credentials including personal key; may
        require a valid product ID the user owns (pattern store product).
        See GitHub issue #2.
        """
        return self._get(f"/products/{product_id}.json", etag=etag, model=ProductResponse)

    def attachments(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a product's attachments (``GET /products/{id}/attachments.json``).

        TODO: returns 403 for all tested credentials including personal key; may
        require a valid product ID the user owns.  See GitHub issue #2.
        """
        return self._get(f"/products/{product_id}/attachments.json", etag=etag, model=ProductAttachmentsResponse)


class AsyncProducts(AsyncResource):
    """Async version of :class:`Products`."""

    async def show(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single product (``GET /products/{id}.json``)."""
        return await self._get(f"/products/{product_id}.json", etag=etag, model=ProductResponse)

    async def attachments(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a product's attachments (``GET /products/{id}/attachments.json``)."""
        return await self._get(f"/products/{product_id}/attachments.json", etag=etag, model=ProductAttachmentsResponse)
