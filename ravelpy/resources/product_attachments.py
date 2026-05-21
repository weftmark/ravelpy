from typing import Optional
from .base import ETagResult, Resource


class ProductAttachments(Resource):
    def show(self, attachment_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/product_attachments/{attachment_id}.json", etag=etag)
