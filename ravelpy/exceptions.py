"""Custom exceptions raised by the ravelpy client."""

import httpx


class RavelryError(Exception):
    """Base class for every error raised by a ravelpy resource method.

    Catch this to handle both HTTP-level failures (:class:`RavelryAPIError`)
    and network-level failures (:class:`RavelryConnectionError`) in one place.
    """


class RavelryAPIError(RavelryError):
    """Raised when the Ravelry API returns a non-2xx HTTP status code, or a
    2xx response whose body is not valid JSON."""

    def __init__(self, status_code: int, message: str):
        """
        Args:
            status_code: The HTTP status code returned by the API.
            message: The response body text describing the error.
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class RavelryConnectionError(RavelryError, httpx.TransportError):
    """Raised when a request fails before a response is received.

    Covers timeouts, DNS failures, refused or reset connections, and protocol
    errors.  The underlying :class:`httpx.TransportError` (e.g.
    :class:`httpx.ReadTimeout`) is available as ``__cause__``; use
    :attr:`is_timeout` to tell timeouts apart from other failures.

    Also a subclass of :class:`httpx.TransportError`, so existing
    ``except httpx.TransportError`` handlers keep working.
    """

    @property
    def is_timeout(self) -> bool:
        """``True`` if the underlying failure was an :class:`httpx.TimeoutException`."""
        return isinstance(self.__cause__, httpx.TimeoutException)
