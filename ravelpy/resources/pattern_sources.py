from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternSearchResponse, PatternSourceResponse, PatternSourcesSearchResponse


class PatternSources(Resource):
    def show(self, source_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/pattern_sources/{source_id}.json", etag=etag, model=PatternSourceResponse)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/pattern_sources/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=PatternSourcesSearchResponse)

    def patterns(
        self,
        source_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/pattern_sources/{source_id}/patterns.json", {"page": page, "page_size": page_size}, etag=etag, model=PatternSearchResponse)
