from typing import Optional
from .base import ETagResult, Resource


class People(Resource):
    def me(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/current_user.json", etag=etag)

    def show(self, username: str, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}.json", etag=etag)

    def comments(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/people/{username}/comments/list.json", {"page": page, "page_size": page_size}, etag=etag)
