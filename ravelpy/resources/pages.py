from typing import Optional
from .base import ApiResult, Resource
from ..responses import PageResponse


class Pages(Resource):
    def show(self, page_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/pages/{page_id}.json", etag=etag, model=PageResponse)
