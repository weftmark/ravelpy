from typing import Optional
from .base import ETagResult, Resource


class Groups(Resource):
    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/groups/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag)
