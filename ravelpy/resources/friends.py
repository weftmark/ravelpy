"""Sub-client for Ravelry Friends API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import FriendActivityResponse, FriendsResponse


class Friends(Resource):
    """Wraps friend list and friend activity endpoints."""

    def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's friends (``GET /people/{username}/friends/list.json``)."""
        return self._get(f"/people/{username}/friends/list.json", etag=etag, model=FriendsResponse)

    def activity(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return recent activity from a user's friends (``GET /people/{username}/friends/activity.json``)."""
        return self._get(f"/people/{username}/friends/activity.json", etag=etag, model=FriendActivityResponse)
