"""Sub-client for Ravelry Library API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import LibraryResponse


class Library(Resource):
    """Wraps the library search endpoint."""

    def search(
        self,
        username: str,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search a user's library (``GET /people/{username}/library/search.json``)."""
        return self._get(
            f"/people/{username}/library/search.json",
            {"query": query, "page": page, "page_size": page_size},
            etag=etag,
            model=LibraryResponse,
        )
