"""Sub-client for Ravelry Queue API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import QueuedProjectResponse, QueueResponse


class Queue(Resource):
    """Wraps queue list and show endpoints."""

    def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's queue (``GET /people/{username}/queue/list.json``)."""
        return self._get(f"/people/{username}/queue/list.json", {"page": page, "page_size": page_size}, etag=etag, model=QueueResponse)

    def show(self, username: str, queue_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single queued project (``GET /people/{username}/queue/{id}.json``)."""
        return self._get(f"/people/{username}/queue/{queue_id}.json", etag=etag, model=QueuedProjectResponse)
