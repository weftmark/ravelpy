"""Sub-client for colorway photo lookup via the Ravelry Projects search endpoint."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..models import ColorwayPhoto


class Colorways(Resource):
    """Provides colorway-level helpers that are not directly exposed by the Ravelry colorway endpoints.

    Auth: public catalog data — ``get_photo`` is accessible with the read-only Basic Auth key.

    .. note::
        ``GET /colorways/{id}.json`` redirects to the Ravelry login page and does not
        work with any developer credential.  Photos must be retrieved through the
        ``GET /projects/search.json`` endpoint, which aggregates crowd-sourced project
        photos and exposes the most representative one as ``first_photo``.
    """

    def get_photo(
        self,
        yarn_id: int,
        colorway_id: int,
    ) -> Optional[ColorwayPhoto]:
        """Return the first crowd-sourced project photo for a colorway, or ``None``.

        Calls ``GET /projects/search.json?yarn_id=X&colorway_id=Y&page_size=1`` and
        extracts the ``first_photo`` field.  This is the same image Ravelry's website
        displays on colorway grid tiles.  Returns ``None`` when no user has photographed
        that colorway yet.

        Args:
            yarn_id:     Ravelry yarn ID (e.g. ``95245``).
            colorway_id: Ravelry colorway ID from :class:`~ravelpy.models.Colorway`.

        Returns:
            A :class:`~ravelpy.models.ColorwayPhoto` with ``square_url``,
            ``thumbnail_url``, and ``small_url``, or ``None``.

        Raises:
            :class:`~ravelpy.exceptions.RavelryAPIError`: On any non-2xx response.
        """
        _parsed, _etag, raw = self._get(
            "/projects/search.json",
            {"yarn_id": yarn_id, "colorway_id": colorway_id, "page_size": 1},
        )
        if not raw:
            return None
        projects = raw.get("projects") or []
        fp = projects[0].get("first_photo") if projects else None
        return ColorwayPhoto(**fp) if fp else None


class AsyncColorways(AsyncResource):
    """Async version of :class:`Colorways`."""

    async def get_photo(
        self,
        yarn_id: int,
        colorway_id: int,
    ) -> Optional[ColorwayPhoto]:
        """Return the first crowd-sourced project photo for a colorway, or ``None``.

        Async equivalent of :meth:`Colorways.get_photo`.

        Args:
            yarn_id:     Ravelry yarn ID.
            colorway_id: Ravelry colorway ID from :class:`~ravelpy.models.Colorway`.

        Returns:
            A :class:`~ravelpy.models.ColorwayPhoto` or ``None``.

        Raises:
            :class:`~ravelpy.exceptions.RavelryAPIError`: On any non-2xx response.
        """
        _parsed, _etag, raw = await self._get(
            "/projects/search.json",
            {"yarn_id": yarn_id, "colorway_id": colorway_id, "page_size": 1},
        )
        if not raw:
            return None
        projects = raw.get("projects") or []
        fp = projects[0].get("first_photo") if projects else None
        return ColorwayPhoto(**fp) if fp else None
