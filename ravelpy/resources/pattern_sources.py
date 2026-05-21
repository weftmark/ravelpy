"""Sub-client for Ravelry Pattern Sources API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternSearchResponse, PatternSourceResponse, PatternSourcesSearchResponse


class PatternSources(Resource):
    """Wraps pattern source show, search, and patterns-by-source endpoints."""

    def show(self, source_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single pattern source (``GET /pattern_sources/{id}.json``)."""
        return self._get(f"/pattern_sources/{source_id}.json", etag=etag, model=PatternSourceResponse)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search pattern sources (``GET /pattern_sources/search.json``)."""
        return self._get("/pattern_sources/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=PatternSourcesSearchResponse)

    def patterns(
        self,
        source_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return patterns from a source (``GET /pattern_sources/{id}/patterns.json``)."""
        return self._get(f"/pattern_sources/{source_id}/patterns.json", {"page": page, "page_size": page_size}, etag=etag, model=PatternSearchResponse)
