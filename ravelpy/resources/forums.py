from typing import Optional
from .base import ETagResult, Resource


class Forums(Resource):
    def sets(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/forums/sets.json", etag=etag)

    def topics(
        self,
        forum_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/forums/{forum_id}/topics.json", {"page": page, "page_size": page_size}, etag=etag)

    def filtered_topics(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/forums/filtered_topics.json", {"page": page, "page_size": page_size}, etag=etag)

    def post(self, post_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/forum_posts/{post_id}.json", etag=etag)

    def unread_posts(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/forum_posts/unread.json", etag=etag)
