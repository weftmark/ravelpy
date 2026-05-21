import httpx
from typing import Optional

from ..exceptions import RavelryAPIError

ETagResult = tuple[Optional[dict], Optional[str]]


class Resource:
    BASE_URL = "https://api.ravelry.com"

    def __init__(self, session: httpx.Client) -> None:
        self._session = session

    def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        url = f"{self.BASE_URL}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        headers = {"If-None-Match": etag} if etag else {}
        response = self._session.get(url, params=clean_params, headers=headers)
        returned_etag = response.headers.get("ETag")
        if response.status_code == 304:
            return None, etag
        if not response.is_success:
            raise RavelryAPIError(response.status_code, response.text)
        return response.json(), returned_etag
