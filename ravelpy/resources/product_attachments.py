"""Sub-client for Ravelry Product Attachments API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ProductAttachmentResponse


class ProductAttachments(Resource):
    """Wraps the product attachment show endpoint.

    Auth: *authenticated* — requires a personal key or OAuth 2.0; the read-only
    Basic Auth key cannot call this endpoint.
    """

    async def show(self, attachment_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single product attachment (``GET /product_attachments/{id}.json``)."""
        return await self._get(f"/product_attachments/{attachment_id}.json", etag=etag, model=ProductAttachmentResponse)
