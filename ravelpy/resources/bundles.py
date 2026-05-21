from typing import Optional
from .base import ApiResult, Resource
from ..responses import BundleResponse, BundlesResponse


class Bundles(Resource):
    def list(
        self,
        username: str,
        owner_types: Optional[str] = None,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/people/{username}/bundles/list.json", {
            "owner_types": owner_types, "query": query,
            "page": page, "page_size": page_size,
        }, etag=etag, model=BundlesResponse)

    def show(self, username: str, bundle_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}/bundles/{bundle_id}.json", etag=etag, model=BundleResponse)
