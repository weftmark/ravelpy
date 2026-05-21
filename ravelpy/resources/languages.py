from typing import Optional
from .base import ETagResult, Resource


class Languages(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/languages/list.json", etag=etag)
