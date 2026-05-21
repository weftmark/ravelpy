from typing import Optional
from .base import ETagResult, Resource


class Shops(Resource):
    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/shops/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag)

    def show(self, shop_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/shops/{shop_id}.json", etag=etag)
