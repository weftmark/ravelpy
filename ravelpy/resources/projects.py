from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, ProjectCraftsResponse, ProjectResponse, ProjectsResponse, ProjectStatusesResponse


class Projects(Resource):
    def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/projects/{username}/list.json", {"page": page, "page_size": page_size}, etag=etag, model=ProjectsResponse)

    def show(self, username: str, project_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/projects/{username}/{project_id}.json", etag=etag, model=ProjectResponse)

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        craft: Optional[str] = None,
        status: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/projects/search.json", {
            "query": query, "page": page, "page_size": page_size,
            "craft": craft, "status": status,
        }, etag=etag, model=ProjectsResponse)

    def comments(
        self,
        username: str,
        project_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/projects/{username}/{project_id}/comments.json", {"page": page, "page_size": page_size}, etag=etag, model=CommentsResponse)

    def crafts(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/projects/crafts.json", etag=etag, model=ProjectCraftsResponse)

    def statuses(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/projects/project_statuses.json", etag=etag, model=ProjectStatusesResponse)
