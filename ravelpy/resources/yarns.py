from typing import Optional
from .base import ETagResult, Resource


class Yarns(Resource):
    def show(self, yarn_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/yarns/{yarn_id}.json", etag=etag)

    def list(self, ids: str, etag: Optional[str] = None) -> ETagResult:
        return self._get("/yarns.json", {"ids": ids}, etag=etag)

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
    ) -> ETagResult:
        return self._get("/yarns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "weight": weight, "fiber_min_weight_pct": fiber_min_weight_pct,
            "color_family_id": color_family_id, "fiber_category_id": fiber_category_id,
            "discontinued": discontinued, "personal_attributes": personal_attributes,
        }, etag=etag)

    def comments(
        self,
        yarn_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/yarns/{yarn_id}/comments.json", {"page": page, "page_size": page_size, "sort": sort}, etag=etag)
