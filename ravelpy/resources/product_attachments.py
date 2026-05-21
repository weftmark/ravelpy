"""Sub-client for Ravelry Product Attachments API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ProductAttachmentResponse


class ProductAttachments(Resource):
    """Wraps the product attachment show endpoint."""

    def show(self, attachment_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single product attachment (``GET /product_attachments/{id}.json``)."""
        return self._get(f"/product_attachments/{attachment_id}.json", etag=etag, model=ProductAttachmentResponse)
