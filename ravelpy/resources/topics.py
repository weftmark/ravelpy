"""Sub-client for Ravelry Topics API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import ForumPostsResponse, TopicResponse


class Topics(Resource):
    """Wraps topic show and topic posts endpoints.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.  Any valid OAuth
    token (baseline or higher) is sufficient for read access; no specific scope needed.
    Write operations (create, reply, update) require the ``forum-write`` OAuth scope
    per API docs; not yet implemented in this library.
    """

    def show(self, topic_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single topic (``GET /topics/{id}.json``)."""
        return self._get(f"/topics/{topic_id}.json", etag=etag, model=TopicResponse)

    def posts(
        self,
        topic_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return posts in a topic (``GET /topics/{id}/posts.json``)."""
        return self._get(f"/topics/{topic_id}/posts.json", {"page": page, "page_size": page_size}, etag=etag, model=ForumPostsResponse)


class AsyncTopics(AsyncResource):
    """Async version of :class:`Topics`."""

    async def show(self, topic_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single topic (``GET /topics/{id}.json``)."""
        return await self._get(f"/topics/{topic_id}.json", etag=etag, model=TopicResponse)

    async def posts(
        self,
        topic_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return posts in a topic (``GET /topics/{id}/posts.json``)."""
        return await self._get(f"/topics/{topic_id}/posts.json", {"page": page, "page_size": page_size}, etag=etag, model=ForumPostsResponse)
