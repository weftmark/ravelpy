from typing import Optional
from .base import ApiResult, Resource
from ..responses import StoreProductsResponse, StoresResponse


class Stores(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/stores/list.json", etag=etag, model=StoresResponse)

    def products(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/stores/{store_id}/products.json", {"page": page, "page_size": page_size}, etag=etag, model=StoreProductsResponse)

    def purchases(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/stores/{store_id}/purchases.json", {"page": page, "page_size": page_size}, etag=etag)
