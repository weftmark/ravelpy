from typing import Optional
from .base import ApiResult, Resource
from ..responses import YarnAttributeGroupsResponse, YarnWeightsResponse


class YarnAttributes(Resource):
    def groups(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/yarn_attributes/groups.json", etag=etag, model=YarnAttributeGroupsResponse)

    def weights(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/yarn_weights.json", etag=etag, model=YarnWeightsResponse)
