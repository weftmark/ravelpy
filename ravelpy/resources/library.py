from typing import Optional
from .base import ApiResult, Resource
from ..responses import LibraryResponse


class Library(Resource):
    def search(
        self,
        username: str,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(
            f"/people/{username}/library/search.json",
            {"query": query, "page": page, "page_size": page_size},
            etag=etag,
            model=LibraryResponse,
        )
