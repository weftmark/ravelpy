"""Sub-client for Ravelry Yarn Attributes reference endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import YarnAttributeGroupsResponse, YarnWeightsResponse


class YarnAttributes(Resource):
    """Wraps yarn attribute groups and yarn weights endpoints.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    async def groups(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn attribute groups (``GET /yarn_attributes/groups.json``)."""
        return await self._get("/yarn_attributes/groups.json", etag=etag, model=YarnAttributeGroupsResponse)

    async def weights(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn weights (``GET /yarn_weights.json``)."""
        return await self._get("/yarn_weights.json", etag=etag, model=YarnWeightsResponse)
