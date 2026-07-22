"""Step execution report read models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pylynqa.models.commands import parse_command

if TYPE_CHECKING:
    from pylynqa.models.commands import Command


@dataclass
class AssertionChecking:
    """A single assertion evaluated during a step.

    :param assertion: Human-readable assertion text.
    :param checked: Whether the assertion evaluated to true.
    """

    assertion: str
    checked: bool

    @classmethod
    def from_dict(cls, d: dict) -> AssertionChecking:
        """Build from a JSON-decoded dict."""
        return cls(assertion=d["assertion"], checked=bool(d["checked"]))


@dataclass
class AssertionsReport:
    """The assertions evaluated for a step, present for ``success`` or ``failed`` steps.

    :param assertions: Individual assertion checks.
    :param screenshot: UUID of the screenshot taken at assertion time.
    """

    assertions: list[AssertionChecking] = field(default_factory=list)
    screenshot: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> AssertionsReport:
        """Build from a JSON-decoded dict."""
        return cls(
            assertions=[AssertionChecking.from_dict(a) for a in d.get("assertions", [])],
            screenshot=d.get("screenshot"),
        )


@dataclass
class StepReport:
    """The execution report of a single test step.

    Depending on the step ``status`` only some fields are populated (e.g. ``assertions_report`` is present for
    ``success`` or ``failed`` steps, ``error`` only for ``error`` steps).

    :param commands: Browser commands executed during this step.
    :param status: Step execution status, e.g. ``'success'``, ``'failed'``, ``'error'``.
    :param start: Step start date (ISO 8601), present once the step has started.
    :param end: Step end date (ISO 8601), present once the step has finished.
    :param assertions_report: Assertions evaluated, present for ``success`` or ``failed`` steps.
    :param test_verdict_cause: Human-readable failure reason, present when ``status`` is ``failed``.
    :param error: Internal error cause, present when ``status`` is ``error``.
    """

    commands: list[Command] = field(default_factory=list)
    status: str = ""
    start: str | None = None
    end: str | None = None
    assertions_report: AssertionsReport | None = None
    test_verdict_cause: str | None = None
    error: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> StepReport:
        """Build from a JSON-decoded step report dict.

        :param d: Step report dict as returned by the API.

        :returns: A typed :class:`StepReport`.
        """
        assertions_report = d.get("assertionsReport")
        return cls(
            commands=[parse_command(c) for c in d.get("commands", [])],
            status=d.get("status", ""),
            start=d.get("start"),
            end=d.get("end"),
            assertions_report=AssertionsReport.from_dict(assertions_report) if assertions_report else None,
            test_verdict_cause=d.get("testVerdictCause"),
            error=d.get("error"),
        )
