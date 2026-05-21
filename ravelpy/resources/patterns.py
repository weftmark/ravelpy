from typing import Optional
from .base import ETagResult, Resource


class Patterns(Resource):
    def show(self, pattern_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/patterns/{pattern_id}.json", etag=etag)

    def list(self, ids: str, etag: Optional[str] = None) -> ETagResult:
        return self._get("/patterns.json", {"ids": ids}, etag=etag)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        craft: Optional[str] = None,
        weight: Optional[str] = None,
        colors: Optional[int] = None,
        fit: Optional[str] = None,
        gender: Optional[str] = None,
        availability: Optional[str] = None,
        language: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/patterns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "craft": craft, "weight": weight, "colors": colors, "fit": fit,
            "gender": gender, "availability": availability, "language": language,
        }, etag=etag)

    def comments(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/patterns/{pattern_id}/comments.json", {"page": page, "page_size": page_size, "sort": sort}, etag=etag)

    def highlights(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/patterns/highlights.json", etag=etag)

    def projects(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/patterns/{pattern_id}/projects.json", {"page": page, "page_size": page_size}, etag=etag)
