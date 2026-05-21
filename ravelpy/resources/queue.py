from typing import Optional
from .base import ETagResult, Resource


class Queue(Resource):
    def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/people/{username}/queue/list.json", {"page": page, "page_size": page_size}, etag=etag)

    def show(self, username: str, queue_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/queue/{queue_id}.json", etag=etag)
