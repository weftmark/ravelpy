"""Sub-client for Ravelry Friends API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import FriendActivityResponse, FriendsResponse


class Friends(Resource):
    """Wraps friend list and friend activity endpoints.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.
    """

    def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's friends (``GET /people/{username}/friends/list.json``)."""
        return self._get(f"/people/{username}/friends/list.json", etag=etag, model=FriendsResponse)

    def activity(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return recent activity from a user's friends (``GET /people/{username}/friends/activity.json``)."""
        return self._get(f"/people/{username}/friends/activity.json", etag=etag, model=FriendActivityResponse)


class AsyncFriends(AsyncResource):
    """Async version of :class:`Friends`."""

    async def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's friends (``GET /people/{username}/friends/list.json``)."""
        return await self._get(f"/people/{username}/friends/list.json", etag=etag, model=FriendsResponse)

    async def activity(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return recent activity from a user's friends (``GET /people/{username}/friends/activity.json``)."""
        return await self._get(f"/people/{username}/friends/activity.json", etag=etag, model=FriendActivityResponse)
