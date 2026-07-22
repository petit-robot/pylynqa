"""Shared value objects used across Lynqa API models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextualData:
    """A guidance hint passed to the Lynqa agent during test execution.

    :param text: Plain-text guidance, e.g. ``'The user is between 18 and 49'``.
    """

    text: str

    def to_dict(self) -> dict:
        """Transform to a JSON-compatible dict."""
        return {"text": self.text}


@dataclass
class CreateAttachment:
    """A file attachment to include with a test run (creation only).

    :param name: File name, e.g. ``'invoice_260313.pdf'``.
    :param data: Base64-encoded data URI, e.g. ``'data:text/plain;base64,SGVsbG8gd29ybGQh'``.
    """

    name: str
    data: str

    def to_dict(self) -> dict:
        """Transform to a JSON-compatible dict."""
        return {"name": self.name, "data": self.data}


@dataclass
class Attachment:
    """A file attachment returned by the API (server-assigned id).

    :param name: File name, e.g. ``'invoice_260313.pdf'``.
    :param id: UUID of the attachment assigned by the server.
    """

    name: str
    id: str


@dataclass
class TestData:
    """A name/value pair used to inject secrets or test data into test steps.

    :param name: Name of the data entry, e.g. ``'password'``.
    :param value: Value of the data entry, e.g. ``'mys3cr3t!'``.
    """

    name: str
    value: str

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict.

        :returns: Dict with ``name`` and ``value``.
        """
        return {"name": self.name, "value": self.value}


@dataclass
class TimePeriod:
    """A relative time window used in :class:`~pylynqa.models.TestRunsFilter`.

    :param count: Number of units, e.g. ``3`` for "last 3 hours".
    :param unit: Time unit — ``'m'`` minutes, ``'h'`` hours, ``'d'`` days, ``'M'`` months.
    """

    count: int
    unit: str

    def to_dict(self) -> dict:
        """Transform to a JSON-compatible dict."""
        return {"count": self.count, "unit": self.unit}
