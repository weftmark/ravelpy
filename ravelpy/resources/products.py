"""Sub-client for Ravelry Products API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ProductAttachmentsResponse, ProductResponse


class Products(Resource):
    """Wraps product show and attachments endpoints."""

    def show(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single product (``GET /products/{id}.json``)."""
        return self._get(f"/products/{product_id}.json", etag=etag, model=ProductResponse)

    def attachments(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a product's attachments (``GET /products/{id}/attachments.json``)."""
        return self._get(f"/products/{product_id}/attachments.json", etag=etag, model=ProductAttachmentsResponse)
