from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, UserResponse


class People(Resource):
    def me(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/current_user.json", etag=etag, model=UserResponse)

    def show(self, username: str, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}.json", etag=etag, model=UserResponse)

    def comments(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/people/{username}/comments/list.json", {"page": page, "page_size": page_size}, etag=etag, model=CommentsResponse)
