"""Sub-client for Ravelry Messages API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import MessageResponse, MessagesResponse


class Messages(Resource):
    """Wraps message list and show endpoints.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.  With OAuth,
    also requires the ``message-write`` scope to send messages (not yet in this
    library).
    """

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return the authenticated user's messages (``GET /messages/list.json``)."""
        return self._get("/messages/list.json", {"page": page, "page_size": page_size}, etag=etag, model=MessagesResponse)

    def show(self, message_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single message (``GET /messages/{id}.json``)."""
        return self._get(f"/messages/{message_id}.json", etag=etag, model=MessageResponse)
