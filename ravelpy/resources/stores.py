"""Sub-client for Ravelry Stores API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import StoreProductsResponse, StoresResponse


class Stores(Resource):
    """Wraps store list, products, and purchases endpoints.

    Auth: *authenticated* — all three endpoints return 403 with the read-only Basic Auth
    key despite not being marked *authenticated* in the official docs.  A personal key
    or OAuth 2.0 is required.

    Required OAuth scopes (per API docs):
    - ``stores.list``: ``patternstore-read`` or ``patternstore-write`` — confirmed 200
      in scope matrix with ``patternstore-read``.
    - ``stores.products``: ``patternstore-read`` or ``patternstore-write`` — but scope
      matrix shows 403 across all tested scopes; may require a store ID the user owns.
      See GitHub issue #2.
    - ``stores.purchases``: ``patternstore-purchases`` — a scope not in the standard
      OAuth scope list and not yet tested in the scope matrix.  See GitHub issue #2.

    See ``docs/authentication.md`` for full scope test results.
    """

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return the current user's stores (``GET /stores/list.json``).

        Requires ``patternstore-read`` or ``patternstore-write`` OAuth scope.
        Scope matrix result: 200 with ``patternstore-read``. See ``docs/authentication.md``.
        """
        return self._get("/stores/list.json", etag=etag, model=StoresResponse)

    def products(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return products for a store (``GET /stores/{id}/products.json``).

        Requires ``patternstore-read`` or ``patternstore-write`` OAuth scope per API docs.

        TODO: scope matrix returned 403 across all tested scopes including
        ``patternstore-read``; may require a valid store ID owned by the user, or
        additional parameters.  See GitHub issue #2.
        """
        return self._get(f"/stores/{store_id}/products.json", {"page": page, "page_size": page_size}, etag=etag, model=StoreProductsResponse)

    def purchases(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return purchases for a store (``GET /stores/{id}/purchases.json``).

        Requires ``patternstore-purchases`` OAuth scope per API docs — this scope is not
        in the standard documented scope list and has not been tested in the scope matrix.

        TODO: obtain a ``patternstore-purchases`` token and validate; currently returns
        403 under all tested scopes.  See GitHub issue #2.
        """
        return self._get(f"/stores/{store_id}/purchases.json", {"page": page, "page_size": page_size}, etag=etag)
