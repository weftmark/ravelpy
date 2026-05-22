"""Base resource classes and shared return-type alias used by all resource sub-clients."""

import httpx
from typing import Any, Optional, Type
from pydantic import BaseModel

from ..exceptions import RavelryAPIError

ApiResult = tuple[Any, Optional[str], Optional[dict]]
"""3-tuple returned by every resource method: ``(parsed, etag, raw)``.

* **parsed** – a validated Pydantic model instance when the response matches
  the expected envelope, or the raw ``dict`` when validation fails or no
  model was supplied.  ``None`` on HTTP 304.
* **etag** – the ``ETag`` header value from the response, or the original
  etag echoed back on HTTP 304.  ``None`` when the server sends no ETag.
* **raw** – the unmodified JSON ``dict`` from the API body.  Always present
  alongside a non-``None`` ``parsed``; ``None`` on HTTP 304.
"""

BASE_URL = "https://api.ravelry.com"


def _process_response(
    response: httpx.Response,
    etag: Optional[str],
    model: Optional[Type[BaseModel]],
) -> ApiResult:
    returned_etag = response.headers.get("ETag")
    if response.status_code == 304:
        return None, etag, None
    if not response.is_success:
        raise RavelryAPIError(response.status_code, response.text)
    raw = response.json()
    if model is not None:
        try:
            parsed = model.model_validate(raw)
        except Exception:
            parsed = raw
    else:
        parsed = raw
    return parsed, returned_etag, raw


class Resource:
    """Base class for all synchronous Ravelry resource sub-clients."""

    BASE_URL = BASE_URL

    def __init__(self, session: httpx.Client) -> None:
        """
        Args:
            session: Authenticated :class:`httpx.Client` shared across all resources.
        """
        self._session = session

    def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        etag: Optional[str] = None,
        model: Optional[Type[BaseModel]] = None,
    ) -> ApiResult:
        """Execute a GET request and return ``(parsed, etag, raw)``.

        Args:
            path:   API path relative to ``BASE_URL`` (e.g. ``/yarns/1.json``).
            params: Query parameters; ``None`` values are stripped before sending.
            etag:   If provided, sent as ``If-None-Match`` for conditional caching.
            model:  Pydantic model class to validate the response body against.

        Returns:
            :data:`ApiResult` 3-tuple ``(parsed, etag, raw)``.

        Raises:
            :class:`~ravelpy.exceptions.RavelryAPIError`: On any non-2xx, non-304 response.
        """
        url = f"{self.BASE_URL}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        headers = {"If-None-Match": etag} if etag else {}
        response = self._session.get(url, params=clean_params, headers=headers)
        return _process_response(response, etag, model)


class AsyncResource:
    """Base class for all asynchronous Ravelry resource sub-clients."""

    BASE_URL = BASE_URL

    def __init__(self, session: httpx.AsyncClient) -> None:
        """
        Args:
            session: Authenticated :class:`httpx.AsyncClient` shared across all resources.
        """
        self._session = session

    async def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        etag: Optional[str] = None,
        model: Optional[Type[BaseModel]] = None,
    ) -> ApiResult:
        """Execute an async GET request and return ``(parsed, etag, raw)``.

        Args:
            path:   API path relative to ``BASE_URL``.
            params: Query parameters; ``None`` values are stripped before sending.
            etag:   If provided, sent as ``If-None-Match`` for conditional caching.
            model:  Pydantic model class to validate the response body against.

        Returns:
            :data:`ApiResult` 3-tuple ``(parsed, etag, raw)``.

        Raises:
            :class:`~ravelpy.exceptions.RavelryAPIError`: On any non-2xx, non-304 response.
        """
        url = f"{self.BASE_URL}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        headers = {"If-None-Match": etag} if etag else {}
        response = await self._session.get(url, params=clean_params, headers=headers)
        return _process_response(response, etag, model)
