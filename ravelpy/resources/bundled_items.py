"""Sub-client for Ravelry Bundled Items API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import BundledItemResponse


class BundledItems(Resource):
    """Wraps the bundled item show endpoint.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.
    """

    def show(self, bundled_item_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single bundled item (``GET /bundled_items/{id}.json``)."""
        return self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag, model=BundledItemResponse)
