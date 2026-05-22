"""Sub-client for Ravelry Messages API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import MessageResponse, MessagesResponse


class Messages(Resource):
    """Wraps message list and show endpoints.

    Auth: *authenticated* — personal key only for read access.  **No OAuth scope
    grants read access to messages** — ``messages.list`` returns 403 under every tested
    OAuth scope including baseline (``offline`` only).
    See ``docs/authentication.md`` scope matrix.

    Write operations (archive, create, delete, reply, unarchive) require the
    ``message-write`` OAuth scope per API docs; not yet implemented in this library.
    """

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return the authenticated user's messages (``GET /messages/list.json``).

        Personal key only — returns 403 under any OAuth scope.
        See ``docs/authentication.md`` scope matrix.
        """
        return self._get("/messages/list.json", {"page": page, "page_size": page_size}, etag=etag, model=MessagesResponse)

    def show(self, message_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single message (``GET /messages/{id}.json``).

        TODO: returns 403 for all tested credentials including personal key; may
        require a valid message ID the user owns.  See GitHub issue #2.
        """
        return self._get(f"/messages/{message_id}.json", etag=etag, model=MessageResponse)


class AsyncMessages(AsyncResource):
    """Async version of :class:`Messages`."""

    async def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return the authenticated user's messages (``GET /messages/list.json``)."""
        return await self._get("/messages/list.json", {"page": page, "page_size": page_size}, etag=etag, model=MessagesResponse)

    async def show(self, message_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single message (``GET /messages/{id}.json``)."""
        return await self._get(f"/messages/{message_id}.json", etag=etag, model=MessageResponse)
