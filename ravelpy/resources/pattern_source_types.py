from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternSourceTypesResponse


class PatternSourceTypes(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/pattern_source_types/list.json", etag=etag, model=PatternSourceTypesResponse)
