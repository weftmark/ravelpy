from typing import Optional
from .base import ETagResult, Resource


class PatternCategories(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/pattern_categories/list.json", etag=etag)
