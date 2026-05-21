from typing import Optional
from .base import ApiResult, Resource
from ..responses import FavoriteResponse, FavoritesResponse


class Favorites(Resource):
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
        return self._get(f"/people/{username}/favorites/list.json", {
            "types": types, "query": query, "tag": tag,
            "page": page, "page_size": page_size,
        }, etag=etag, model=FavoritesResponse)

    def show(self, username: str, favorite_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}/favorites/{favorite_id}.json", etag=etag, model=FavoriteResponse)
