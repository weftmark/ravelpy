from typing import Optional
from .base import ETagResult, Resource


class Deliveries(Resource):
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/deliveries/list.json", {"page": page, "page_size": page_size}, etag=etag)
