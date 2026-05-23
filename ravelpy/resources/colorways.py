"""Sub-client stub for colorway-related helpers."""

from .base import Resource


class Colorways(Resource):
    """Namespace for colorway-related helpers.

    Auth: public catalog data — accessible with the read-only Basic Auth key.

    .. note::
        The Ravelry API does not expose a usable colorway-level photo endpoint.
        ``GET /colorways/{id}.json`` redirects to the login page for all
        developer credential types.  ``GET /projects/search.json`` accepts a
        ``colorway_id`` query parameter, but the parameter is silently ignored
        by the API — every call returns the same top project photo for the
        yarn regardless of which colorway is requested (confirmed with both
        Basic Auth and OAuth 2.0 Bearer tokens).  No colorway-specific photo
        helper is provided for this reason.
    """
