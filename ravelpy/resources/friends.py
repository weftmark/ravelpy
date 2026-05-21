from typing import Optional
from .base import ApiResult, Resource
from ..responses import FriendActivityResponse, FriendsResponse


class Friends(Resource):
    def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}/friends/list.json", etag=etag, model=FriendsResponse)

    def activity(self, username: str, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}/friends/activity.json", etag=etag, model=FriendActivityResponse)
