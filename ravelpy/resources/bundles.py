"""Sub-client for Ravelry Bundles API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import BundleResponse, BundlesResponse


class Bundles(Resource):
    """Wraps bundle list and show endpoints."""

    def list(
        self,
        username: str,
        owner_types: Optional[str] = None,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's bundles (``GET /people/{username}/bundles/list.json``)."""
        return self._get(f"/people/{username}/bundles/list.json", {
            "owner_types": owner_types, "query": query,
            "page": page, "page_size": page_size,
        }, etag=etag, model=BundlesResponse)

    def show(self, username: str, bundle_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single bundle (``GET /people/{username}/bundles/{id}.json``)."""
        return self._get(f"/people/{username}/bundles/{bundle_id}.json", etag=etag, model=BundleResponse)
