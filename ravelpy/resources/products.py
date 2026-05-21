from typing import Optional
from .base import ETagResult, Resource


class Products(Resource):
    def show(self, product_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/products/{product_id}.json", etag=etag)

    def attachments(self, product_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/products/{product_id}/attachments.json", etag=etag)
