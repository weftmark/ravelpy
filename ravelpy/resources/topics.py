from typing import Optional
from .base import ETagResult, Resource


class Topics(Resource):
    def show(self, topic_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/topics/{topic_id}.json", etag=etag)

    def posts(
        self,
        topic_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/topics/{topic_id}/posts.json", {"page": page, "page_size": page_size}, etag=etag)
