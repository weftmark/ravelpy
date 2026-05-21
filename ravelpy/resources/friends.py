from typing import Optional
from .base import ETagResult, Resource


class Friends(Resource):
    def list(self, username: str, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/friends/list.json", etag=etag)

    def activity(self, username: str, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/friends/activity.json", etag=etag)
