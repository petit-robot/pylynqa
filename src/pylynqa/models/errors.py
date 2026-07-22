"""Exceptions raised by the Lynqa client."""

from __future__ import annotations


class LynqaClientError(Exception):
    """Raised when the Lynqa API returns a non-2xx HTTP response.

    :param status_code: HTTP status code returned by the server.
    :param error: Short error label from the response body (e.g. ``'Unauthorized'``).
    :param message: Human-readable description from the response body (e.g. ``'Missing authentication method'``).

    Common status codes:

    - ``400`` - Request body is malformed.
    - ``401`` - Authentication failed (invalid or missing API key).
    - ``403`` - Not enough credits to execute the test.
    - ``404`` - Resource not found.
    - ``410`` - Test run has expired.
    - ``422`` - URL is not safe to test.
    - ``429`` - Too many requests (rate limit exceeded).
    """

    def __init__(self, status_code: int, error: str = "", message: str = "") -> None:
        """Initialize the LynqaClientError."""
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"HTTP {status_code}: {error}" + (f" - {message}" if message else ""))
