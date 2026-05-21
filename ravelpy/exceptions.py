"""Custom exceptions raised by the ravelpy client."""


class RavelryAPIError(Exception):
    """Raised when the Ravelry API returns a non-2xx HTTP status code."""

    def __init__(self, status_code: int, message: str):
        """
        Args:
            status_code: The HTTP status code returned by the API.
            message: The response body text describing the error.
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")
