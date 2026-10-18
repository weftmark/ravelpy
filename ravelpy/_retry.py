"""Opt-in retry transport for idempotent GET requests."""

import asyncio
import email.utils
import random
import time
from typing import Optional

import httpx

RETRY_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.ReadError,
    httpx.RemoteProtocolError,
)
"""Transport failures that are safe to retry for a GET request."""

RETRY_STATUSES = frozenset({429, 502, 503, 504})
"""HTTP statuses that indicate a transient server-side condition."""

BACKOFF_BASE = 0.5
"""Delay before the first retry, in seconds; doubles on each attempt."""

MAX_DELAY = 30.0
"""Upper bound on any single delay, including one requested via ``Retry-After``."""

_sleep = asyncio.sleep  # indirection so tests can avoid real waits


def _backoff(attempt: int) -> float:
    """Exponential backoff with jitter: ~0.5 s, 1 s, 2 s … scaled by 50–100%."""
    return min(MAX_DELAY, BACKOFF_BASE * 2**attempt) * random.uniform(0.5, 1.0)


def _retry_after(response: httpx.Response) -> Optional[float]:
    """Parse a ``Retry-After`` header (delta-seconds or HTTP-date) into seconds."""
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    value = value.strip()
    if value.isdigit():
        return min(MAX_DELAY, float(value))
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return min(MAX_DELAY, max(0.0, when.timestamp() - time.time()))


class RetryTransport(httpx.AsyncBaseTransport):
    """Wrap an async transport and retry failed GET requests.

    Only ``GET`` requests are retried — writes are passed through untouched,
    since a timed-out POST may already have been applied.  A request is retried
    on any of :data:`RETRY_EXCEPTIONS` or :data:`RETRY_STATUSES`, up to
    ``max_retries`` extra attempts.  When attempts run out, the last exception
    is raised or the last response returned, so callers see exactly what they
    would without retries.
    """

    def __init__(self, wrapped: httpx.AsyncBaseTransport, max_retries: int) -> None:
        self._wrapped = wrapped
        self._max_retries = max_retries

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.method != "GET":
            return await self._wrapped.handle_async_request(request)

        attempt = 0
        while True:
            try:
                response = await self._wrapped.handle_async_request(request)
            except RETRY_EXCEPTIONS:
                if attempt >= self._max_retries:
                    raise
                delay = _backoff(attempt)
            else:
                if response.status_code not in RETRY_STATUSES or attempt >= self._max_retries:
                    return response
                delay = _retry_after(response)
                if delay is None:
                    delay = _backoff(attempt)
                await response.aclose()
            attempt += 1
            await _sleep(delay)

    async def aclose(self) -> None:
        await self._wrapped.aclose()
