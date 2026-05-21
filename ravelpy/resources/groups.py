from typing import Optional
from .base import ApiResult, Resource
from ..responses import GroupsResponse


class Groups(Resource):
    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/groups/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=GroupsResponse)
