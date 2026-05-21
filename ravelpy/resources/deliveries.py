"""Sub-client for Ravelry Deliveries API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import DeliveriesResponse


class Deliveries(Resource):
    """Wraps the deliveries list endpoint.

    Auth: not marked *authenticated* in the docs, but requires the
    ``deliveries-read`` OAuth scope.  A personal key grants this scope
    automatically; an OAuth 2.0 token must explicitly request it.  The
    read-only Basic Auth key cannot access delivery data.
    """

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return the authenticated user's deliveries (``GET /deliveries/list.json``)."""
        return self._get("/deliveries/list.json", {"page": page, "page_size": page_size}, etag=etag, model=DeliveriesResponse)
