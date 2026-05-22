"""Sub-client for Ravelry Volumes API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import VolumeResponse


class Volumes(Resource):
    """Wraps the volume show endpoint.

    Auth: *authenticated* — requires a personal key or OAuth 2.0.
    """

    def show(self, volume_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single volume (``GET /volumes/{id}.json``)."""
        return self._get(f"/volumes/{volume_id}.json", etag=etag, model=VolumeResponse)


class AsyncVolumes(AsyncResource):
    """Async version of :class:`Volumes`."""

    async def show(self, volume_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single volume (``GET /volumes/{id}.json``)."""
        return await self._get(f"/volumes/{volume_id}.json", etag=etag, model=VolumeResponse)
