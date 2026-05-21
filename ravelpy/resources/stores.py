"""Sub-client for Ravelry Stores API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import StoreProductsResponse, StoresResponse


class Stores(Resource):
    """Wraps store list, products, and purchases endpoints.

    Auth: *authenticated* — all three endpoints return 403 with the read-only Basic Auth
    key despite not being marked *authenticated* in the official docs.  A personal key
    or OAuth 2.0 is required.
    """

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all stores (``GET /stores/list.json``)."""
        return self._get("/stores/list.json", etag=etag, model=StoresResponse)

    def products(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return products for a store (``GET /stores/{id}/products.json``)."""
        return self._get(f"/stores/{store_id}/products.json", {"page": page, "page_size": page_size}, etag=etag, model=StoreProductsResponse)

    def purchases(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return purchases for a store (``GET /stores/{id}/purchases.json``)."""
        return self._get(f"/stores/{store_id}/purchases.json", {"page": page, "page_size": page_size}, etag=etag)
