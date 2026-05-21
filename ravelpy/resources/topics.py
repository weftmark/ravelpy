from typing import Optional
from .base import ApiResult, Resource
from ..responses import ForumPostsResponse, TopicResponse


class Topics(Resource):
    def show(self, topic_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/topics/{topic_id}.json", etag=etag, model=TopicResponse)

    def posts(
        self,
        topic_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/topics/{topic_id}/posts.json", {"page": page, "page_size": page_size}, etag=etag, model=ForumPostsResponse)
