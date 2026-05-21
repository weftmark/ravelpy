from typing import Optional
from .base import ETagResult, Resource


class PatternAttributes(Resource):
    def groups(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/pattern_attributes/groups.json", etag=etag)
