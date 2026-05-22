"""Sub-client for Ravelry Yarn Companies API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import YarnCompaniesResponse


class YarnCompanies(Resource):
    """Wraps the yarn company search endpoint.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search yarn companies (``GET /yarn_companies/search.json``)."""
        return self._get("/yarn_companies/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=YarnCompaniesResponse)


class AsyncYarnCompanies(AsyncResource):
    """Async version of :class:`YarnCompanies`."""

    async def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search yarn companies (``GET /yarn_companies/search.json``)."""
        return await self._get("/yarn_companies/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=YarnCompaniesResponse)
