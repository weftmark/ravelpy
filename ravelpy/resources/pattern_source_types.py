from typing import Optional
from .base import ETagResult, Resource


class PatternSourceTypes(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/pattern_source_types/list.json", etag=etag)
