from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternAttributeGroupsResponse


class PatternAttributes(Resource):
    def groups(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/pattern_attributes/groups.json", etag=etag, model=PatternAttributeGroupsResponse)
