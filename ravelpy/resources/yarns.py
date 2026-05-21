"""Sub-client for Ravelry Yarns API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, YarnResponse, YarnsMultiResponse, YarnSearchResponse


class Yarns(Resource):
    """Wraps yarn show, multi-fetch, search, and comment endpoints."""

    def show(self, yarn_id: int, include: Optional[str] = None, etag: Optional[str] = None) -> ApiResult:
        """Return a single yarn by ID (``GET /yarns/{id}.json``)."""
        return self._get(f"/yarns/{yarn_id}.json", {"include": include}, etag=etag, model=YarnResponse)

    def list(self, ids: str, etag: Optional[str] = None) -> ApiResult:
        """Return multiple yarns by comma-separated IDs (``GET /yarns.json``)."""
        return self._get("/yarns.json", {"ids": ids}, etag=etag, model=YarnsMultiResponse)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        weight: Optional[str] = None,
        fiber_min_weight_pct: Optional[int] = None,
        color_family_id: Optional[int] = None,
        fiber_category_id: Optional[int] = None,
        discontinued: Optional[bool] = None,
        personal_attributes: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search yarns with optional filters (``GET /yarns/search.json``)."""
        return self._get("/yarns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "weight": weight, "fiber_min_weight_pct": fiber_min_weight_pct,
            "color_family_id": color_family_id, "fiber_category_id": fiber_category_id,
            "discontinued": discontinued, "personal_attributes": personal_attributes,
        }, etag=etag, model=YarnSearchResponse)

    def comments(
        self,
        yarn_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments for a yarn (``GET /yarns/{id}/comments.json``)."""
        return self._get(f"/yarns/{yarn_id}/comments.json", {"page": page, "page_size": page_size, "sort": sort}, etag=etag, model=CommentsResponse)
