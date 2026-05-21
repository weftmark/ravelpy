from typing import Optional
from .base import ETagResult, Resource


class PatternSources(Resource):
    def show(self, source_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/pattern_sources/{source_id}.json", etag=etag)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/pattern_sources/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag)

    def patterns(
        self,
        source_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/pattern_sources/{source_id}/patterns.json", {"page": page, "page_size": page_size}, etag=etag)
