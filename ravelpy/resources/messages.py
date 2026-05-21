from typing import Optional
from .base import ETagResult, Resource


class Messages(Resource):
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/messages/list.json", {"page": page, "page_size": page_size}, etag=etag)

    def show(self, message_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/messages/{message_id}.json", etag=etag)
