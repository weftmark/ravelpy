"""Sub-client for Ravelry Pages API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PageResponse


class Pages(Resource):
    """Wraps the page show endpoint.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.
    """

    def show(self, page_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single page (``GET /pages/{id}.json``)."""
        return self._get(f"/pages/{page_id}.json", etag=etag, model=PageResponse)
