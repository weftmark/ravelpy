from typing import Optional
from .base import ApiResult, Resource
from ..responses import ProductAttachmentResponse


class ProductAttachments(Resource):
    def show(self, attachment_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/product_attachments/{attachment_id}.json", etag=etag, model=ProductAttachmentResponse)
