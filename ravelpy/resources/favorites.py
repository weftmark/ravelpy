"""Sub-client for Ravelry Favorites API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import FavoriteResponse, FavoritesResponse


class Favorites(Resource):
    """Wraps favorites list and show endpoints.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.
    """

    def list(
        self,
        username: str,
        types: Optional[str] = None,
        query: Optional[str] = None,
        tag: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's favorites (``GET /people/{username}/favorites/list.json``)."""
        return self._get(f"/people/{username}/favorites/list.json", {
            "types": types, "query": query, "tag": tag,
            "page": page, "page_size": page_size,
        }, etag=etag, model=FavoritesResponse)

    def show(self, username: str, favorite_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single favorite (``GET /people/{username}/favorites/{id}.json``)."""
        return self._get(f"/people/{username}/favorites/{favorite_id}.json", etag=etag, model=FavoriteResponse)
