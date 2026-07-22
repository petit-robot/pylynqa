"""Test-run request models: steps, context, and creation payloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pylynqa.models.common import (
        Attachment,
        CreateAttachment,
        TestData,
        TextualData,
        TimePeriod,
    )


@dataclass
class CreateTestStep:
    """A single step to include when creating a test run.

    :param action: Human-readable description of the action to perform, e.g. ``'Click on the "Login" button'``.
    :param expected_result: Optional assertion that should hold after the action is executed, e.g. ``'The user is
        redirected to /dashboard'``.
    :param guidance: Optional guidance hints to help the agent execute this step.
    :param attachments: Optional file attachments for this step (base64-encoded).
    """

    action: str
    expected_result: str | None = None
    guidance: list[TextualData] = field(default_factory=list)
    attachments: list[CreateAttachment] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict.

        :returns: Dict with ``action`` and, when set, optional fields.
        """
        d: dict = {"action": self.action}
        if self.expected_result is not None:
            d["expectedResult"] = self.expected_result
        if self.guidance:
            d["guidance"] = [g.to_dict() for g in self.guidance]
        if self.attachments:
            d["attachments"] = [a.to_dict() for a in self.attachments]
        return d


@dataclass
class TestStep:
    """A single step returned by the API for a test run.

    :param action: Human-readable description of the action performed.
    :param expected_result: Assertion associated with this step, if any.
    :param guidance: Guidance hints attached to this step.
    :param attachments: File attachments returned by the server (read-only, server-assigned ids).
    """

    action: str
    expected_result: str | None = None
    guidance: list[TextualData] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)


@dataclass
class TestRunContext:
    """Optional context attached to a test run.

    Provides locale information and secrets that the Lynqa engine can use when executing the test steps.

    :param client_language: BCP-47 language tag or plain language name representing the browser locale, e.g.
        ``'en-US'``.
    :param client_datetime: Human-readable local date/time string passed to the agent, e.g. ``'Thu Feb 26 2026 09:26:12
        GMT+0100'``. :param secrets: List of :class:`~pylynqa.models.TestData` entries that will be injected into the
        test steps at execution time.
    """

    client_language: str | None = None
    client_datetime: str | None = None
    secrets: list[TestData] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict, omitting unset fields.

        :returns: Dict representation of the context.
        """
        d: dict = {}
        if self.client_language is not None:
            d["clientLanguage"] = self.client_language
        if self.client_datetime is not None:
            d["clientDatetime"] = self.client_datetime
        if self.secrets:
            d["secrets"] = [s.to_dict() for s in self.secrets]
        return d


@dataclass
class TestRunsFilter:
    """Filter criteria for :meth:`~pylynqa.client.LynqaClient.query_test_runs`.

    All fields are optional; omitted fields are not sent in the request body.

    :param statuses: Keep only runs with these statuses. Allowed values: ``'waiting'``, ``'running'``, ``'success'``,
        ``'failed'``, ``'error'``, ``'stopped'``, ``'not_run'``.
    :param relative_period: Relative time window, e.g. ``TimePeriod(count=3, unit='h')`` for the last 3 hours.
    :param start_date: Start of an explicit date range (ISO 8601).
    :param end_date: End of an explicit date range (ISO 8601).
    :param api_key_ids: Keep only runs created by these API key IDs.
    :param test_run_ids: Keep only runs with these IDs.
    """

    statuses: list[str] | None = None
    relative_period: TimePeriod | None = None
    start_date: str | None = None
    end_date: str | None = None
    api_key_ids: list[str] | None = None
    test_run_ids: list[str] | None = None

    def to_dict(self) -> dict:
        """Transform to a JSON-compatible dict."""
        d: dict = {}
        if self.statuses is not None:
            d["statuses"] = self.statuses
        if self.relative_period is not None:
            d["relativePeriod"] = self.relative_period.to_dict()
        if self.start_date is not None:
            d["startDate"] = self.start_date
        if self.end_date is not None:
            d["endDate"] = self.end_date
        if self.api_key_ids is not None:
            d["apiKeyIds"] = self.api_key_ids
        if self.test_run_ids is not None:
            d["testRunIds"] = self.test_run_ids
        return d


@dataclass
class CreateTest:
    """A manual test to execute (creation payload).

    Mirrors the ``CreateTest`` schema. Used both by :meth:`~pylynqa.client.LynqaClient.add_test_run` and, together with
    :class:`~pylynqa.models.CreateGherkinTest`, inside a :meth:`~pylynqa.client.LynqaClient.add_test_batch` call.

    :param url: URL of the system under test, e.g. ``'https://example.com'``.
    :param steps: Ordered list of test steps to execute.
    :param name: Optional human-readable name for this run.
    :param context: Optional locale and secrets context.
    :param guidance: Optional global guidance hints for the agent.
    :param attachments: Optional files attached to the test run (base64-encoded).
    :param webhooks: Optional list of webhook URLs to notify once the test run has ended.
    """

    url: str
    steps: list[CreateTestStep] = field(default_factory=list)
    name: str | None = None
    context: TestRunContext | None = None
    guidance: list[TextualData] = field(default_factory=list)
    attachments: list[CreateAttachment] = field(default_factory=list)
    webhooks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict, omitting unset optional fields.

        :returns: Dict with ``url`` and ``steps`` always present.
        """
        d: dict = {"url": self.url, "steps": [s.to_dict() for s in self.steps]}
        if self.name is not None:
            d["name"] = self.name
        if self.context is not None:
            d["context"] = self.context.to_dict()
        if self.guidance:
            d["guidance"] = [g.to_dict() for g in self.guidance]
        if self.attachments:
            d["attachments"] = [a.to_dict() for a in self.attachments]
        if self.webhooks:
            d["webhooks"] = self.webhooks
        return d


@dataclass
class CreateGherkinTest:
    """A Gherkin (BDD) test to execute (creation payload).

    Mirrors the ``CreateGherkinTest`` schema. Used both by :meth:`~pylynqa.client.LynqaClient.add_gherkin_test_run` and,
    together with :class:`~pylynqa.models.CreateTest`, inside a :meth:`~pylynqa.client.LynqaClient.add_test_batch` call.

    :param url: URL of the system under test.
    :param scenario: Full Gherkin scenario text, including ``Given``, ``When``, and ``Then`` steps.
    :param name: Optional human-readable name for this run.
    :param context: Optional locale and secrets context.
    :param guidance: Optional global guidance hints for the agent.
    :param attachments: Optional files attached to the test run (base64-encoded).
    :param webhooks: Optional list of webhook URLs to notify once the test run has ended.
    """

    url: str
    scenario: str
    name: str | None = None
    context: TestRunContext | None = None
    guidance: list[TextualData] = field(default_factory=list)
    attachments: list[CreateAttachment] = field(default_factory=list)
    webhooks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict, omitting unset optional fields.

        :returns: Dict with ``url`` and ``scenario`` always present.
        """
        d: dict = {"url": self.url, "scenario": self.scenario}
        if self.name is not None:
            d["name"] = self.name
        if self.context is not None:
            d["context"] = self.context.to_dict()
        if self.guidance:
            d["guidance"] = [g.to_dict() for g in self.guidance]
        if self.attachments:
            d["attachments"] = [a.to_dict() for a in self.attachments]
        if self.webhooks:
            d["webhooks"] = self.webhooks
        return d
