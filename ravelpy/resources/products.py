from typing import Optional
from .base import ApiResult, Resource
from ..responses import ProductAttachmentsResponse, ProductResponse


class Products(Resource):
    def show(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/products/{product_id}.json", etag=etag, model=ProductResponse)

    def attachments(self, product_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/products/{product_id}/attachments.json", etag=etag, model=ProductAttachmentsResponse)
