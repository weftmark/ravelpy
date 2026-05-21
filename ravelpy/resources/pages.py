from typing import Optional
from .base import ETagResult, Resource


class Pages(Resource):
    def show(self, page_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/pages/{page_id}.json", etag=etag)
