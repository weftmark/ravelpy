from typing import Optional
from .base import ETagResult, Resource


class Fiber(Resource):
    def show(self, username: str, fiber_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/fiber/{fiber_id}.json", etag=etag)

    def comments(
        self,
        username: str,
        fiber_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(
            f"/people/{username}/fiber/{fiber_id}/comments.json",
            {"page": page, "page_size": page_size, "sort": sort},
            etag=etag,
        )
