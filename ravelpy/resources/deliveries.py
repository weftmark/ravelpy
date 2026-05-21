"""Sub-client for Ravelry Deliveries API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import DeliveriesResponse


class Deliveries(Resource):
    """Wraps the deliveries list endpoint."""

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return the authenticated user's deliveries (``GET /deliveries/list.json``)."""
        return self._get("/deliveries/list.json", {"page": page, "page_size": page_size}, etag=etag, model=DeliveriesResponse)
