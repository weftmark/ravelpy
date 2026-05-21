from typing import Optional
from .base import ETagResult, Resource


class Stores(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/stores/list.json", etag=etag)

    def products(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/stores/{store_id}/products.json", {"page": page, "page_size": page_size}, etag=etag)

    def purchases(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/stores/{store_id}/purchases.json", {"page": page, "page_size": page_size}, etag=etag)
