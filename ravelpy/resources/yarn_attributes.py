"""Sub-client for Ravelry Yarn Attributes reference endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import YarnAttributeGroupsResponse, YarnWeightsResponse


class YarnAttributes(Resource):
    """Wraps yarn attribute groups and yarn weights endpoints.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    def groups(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn attribute groups (``GET /yarn_attributes/groups.json``)."""
        return self._get("/yarn_attributes/groups.json", etag=etag, model=YarnAttributeGroupsResponse)

    def weights(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn weights (``GET /yarn_weights.json``)."""
        return self._get("/yarn_weights.json", etag=etag, model=YarnWeightsResponse)


class AsyncYarnAttributes(AsyncResource):
    """Async version of :class:`YarnAttributes`."""

    async def groups(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn attribute groups (``GET /yarn_attributes/groups.json``)."""
        return await self._get("/yarn_attributes/groups.json", etag=etag, model=YarnAttributeGroupsResponse)

    async def weights(self, etag: Optional[str] = None) -> ApiResult:
        """Return all yarn weights (``GET /yarn_weights.json``)."""
        return await self._get("/yarn_weights.json", etag=etag, model=YarnWeightsResponse)
