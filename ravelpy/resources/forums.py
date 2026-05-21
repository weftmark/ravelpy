from typing import Optional
from .base import ApiResult, Resource
from ..responses import ForumPostResponse, ForumPostsResponse, ForumSetsResponse, TopicsResponse


class Forums(Resource):
    def sets(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/forums/sets.json", etag=etag, model=ForumSetsResponse)

    def topics(
        self,
        forum_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/forums/{forum_id}/topics.json", {"page": page, "page_size": page_size}, etag=etag, model=TopicsResponse)

    def filtered_topics(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/forums/filtered_topics.json", {"page": page, "page_size": page_size}, etag=etag, model=TopicsResponse)

    def post(self, post_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/forum_posts/{post_id}.json", etag=etag, model=ForumPostResponse)

    def unread_posts(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/forum_posts/unread.json", etag=etag, model=ForumPostsResponse)
