"""Sub-client for Ravelry People (user profile) API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, UserResponse


class People(Resource):
    """Wraps current-user, profile show, and profile comment endpoints.

    Auth: *authenticated* — all methods require a personal key or OAuth 2.0.  Any valid
    OAuth token is sufficient for read access; no specific scope needed.

    The profile update write operation requires ``profile-write`` OAuth scope per API
    docs; not yet implemented in this library.

    Note: ``people.comments`` returns 403 for all tested credentials including personal
    key.  See GitHub issue #2 — likely requires a valid username that has comments, or
    may require specific parameters.

    TODO: validate ``people.comments`` with a username known to have profile comments.
    """

    def me(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's profile (``GET /current_user.json``)."""
        return self._get("/current_user.json", etag=etag, model=UserResponse)

    def show(self, username: str, etag: Optional[str] = None) -> ApiResult:
        """Return a user's public profile (``GET /people/{username}.json``)."""
        return self._get(f"/people/{username}.json", etag=etag, model=UserResponse)

    def comments(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments on a user's profile (``GET /people/{username}/comments/list.json``)."""
        return self._get(f"/people/{username}/comments/list.json", {"page": page, "page_size": page_size}, etag=etag, model=CommentsResponse)
