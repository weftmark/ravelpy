"""Sub-client for Ravelry Forums API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import ForumPostResponse, ForumPostsResponse, ForumSetsResponse, TopicsResponse


class Forums(Resource):
    """Wraps forum sets, topics, filtered topics, and forum post endpoints.

    Auth: *authenticated* — all five endpoints require a personal key or OAuth 2.0.
    ``unread_posts`` is not marked *authenticated* in the official docs but returns
    403 with the read-only Basic Auth key in live testing.
    """

    def sets(self, etag: Optional[str] = None) -> ApiResult:
        """Return all forum sets (``GET /forums/sets.json``)."""
        return self._get("/forums/sets.json", etag=etag, model=ForumSetsResponse)

    def topics(
        self,
        forum_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return topics in a forum (``GET /forums/{forum_id}/topics.json``)."""
        return self._get(f"/forums/{forum_id}/topics.json", {"page": page, "page_size": page_size}, etag=etag, model=TopicsResponse)

    def filtered_topics(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return topics filtered by the authenticated user's groups (``GET /forums/filtered_topics.json``)."""
        return self._get("/forums/filtered_topics.json", {"page": page, "page_size": page_size}, etag=etag, model=TopicsResponse)

    def post(self, post_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single forum post (``GET /forum_posts/{id}.json``)."""
        return self._get(f"/forum_posts/{post_id}.json", etag=etag, model=ForumPostResponse)

    def unread_posts(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's unread forum posts (``GET /forum_posts/unread.json``)."""
        return self._get("/forum_posts/unread.json", etag=etag, model=ForumPostsResponse)
