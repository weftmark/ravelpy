"""Sub-client for Ravelry Projects API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, ProjectCraftsResponse, ProjectResponse, ProjectsResponse, ProjectStatusesResponse


class Projects(Resource):
    """Wraps project list, show, search, comments, crafts, and statuses endpoints.

    Auth: ``search``, ``list``, ``show``, ``crafts``, and ``statuses`` are accessible with
    the read-only Basic Auth key (``list``, ``crafts``, and ``statuses`` are marked
    *authenticated* in the official docs but return 200 in live testing).  ``comments``
    returns 403 with the read-only key and requires a personal key or OAuth 2.0.
    """

    async def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's projects (``GET /projects/{username}/list.json``)."""
        return await self._get(f"/projects/{username}/list.json", {"page": page, "page_size": page_size}, etag=etag, model=ProjectsResponse)

    async def show(self, username: str, project_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single project (``GET /projects/{username}/{id}.json``)."""
        return await self._get(f"/projects/{username}/{project_id}.json", etag=etag, model=ProjectResponse)

    async def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        craft: Optional[str] = None,
        status: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search projects with optional filters (``GET /projects/search.json``)."""
        return await self._get("/projects/search.json", {
            "query": query, "page": page, "page_size": page_size,
            "craft": craft, "status": status,
        }, etag=etag, model=ProjectsResponse)

    async def comments(
        self,
        username: str,
        project_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments on a project (``GET /projects/{username}/{id}/comments.json``).

        Authenticated — requires a personal key or OAuth 2.0.
        """
        return await self._get(f"/projects/{username}/{project_id}/comments.json", {"page": page, "page_size": page_size}, etag=etag, model=CommentsResponse)

    async def crafts(self, etag: Optional[str] = None) -> ApiResult:
        """Return the list of craft types (``GET /projects/crafts.json``)."""
        return await self._get("/projects/crafts.json", etag=etag, model=ProjectCraftsResponse)

    async def statuses(self, etag: Optional[str] = None) -> ApiResult:
        """Return the list of project status values (``GET /projects/project_statuses.json``)."""
        return await self._get("/projects/project_statuses.json", etag=etag, model=ProjectStatusesResponse)
