from typing import Optional
from .base import ApiResult, Resource
from ..responses import YarnCompaniesResponse


class YarnCompanies(Resource):
    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/yarn_companies/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=YarnCompaniesResponse)
