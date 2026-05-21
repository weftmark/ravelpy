import httpx
from typing import Any, Optional, Type
from pydantic import BaseModel

from ..exceptions import RavelryAPIError

ApiResult = tuple[Any, Optional[str], Optional[dict]]


class Resource:
    BASE_URL = "https://api.ravelry.com"

    def __init__(self, session: httpx.Client) -> None:
        self._session = session

    def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        etag: Optional[str] = None,
        model: Optional[Type[BaseModel]] = None,
    ) -> ApiResult:
        url = f"{self.BASE_URL}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        headers = {"If-None-Match": etag} if etag else {}
        response = self._session.get(url, params=clean_params, headers=headers)
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
