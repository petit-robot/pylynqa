"""Data models for Lynqa API: test steps, test data, and test run context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


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
class TestRunContext:
    """Optional context attached to a test run.

    Provides locale information and secrets that the Lynqa engine can use when executing the test steps.

    :param client_language: BCP-47 language tag or plain language name representing the browser locale, e.g.
        ``'en-US'``.
    :param client_datetime: Human-readable local date/time string passed to the agent, e.g. ``'Thu Feb 26 2026 09:26:12
        GMT+0100'``. :param secrets: List of :class:`TestData` entries that will be injected into the test steps at
        execution time.
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
class TimePeriod:
    """A relative time window used in :class:`TestRunsFilter`.

    :param count: Number of units, e.g. ``3`` for "last 3 hours".
    :param unit: Time unit — ``'m'`` minutes, ``'h'`` hours, ``'d'`` days, ``'M'`` months.
    """

    count: int
    unit: str

    def to_dict(self) -> dict:
        """Transform to a JSON-compatible dict."""
        return {"count": self.count, "unit": self.unit}


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
    :class:`CreateGherkinTest`, inside a :meth:`~pylynqa.client.LynqaClient.add_test_batch` call.

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
    together with :class:`CreateTest`, inside a :meth:`~pylynqa.client.LynqaClient.add_test_batch` call.

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


# ----------------------------------------------------------------------
# Step reports (read models)
# ----------------------------------------------------------------------


@dataclass
class ErrorResponse:
    """Failure outcome of a browser command.

    :param error: Machine-readable error cause, e.g. ``'not_visible_element'`` or ``'host_not_reachable'``.
    """

    error: str

    @classmethod
    def from_dict(cls, d: dict) -> ErrorResponse:
        """Build from a JSON-decoded response dict."""
        return cls(error=d["error"])


@dataclass
class ClickCommandResponse:
    """Result payload of a successful ``click`` command.

    :param new_url: URL after the click, if navigation occurred.
    """

    new_url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ClickCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(new_url=d.get("newUrl"))


@dataclass
class ClickCommandSuccess:
    """Success outcome of a ``click`` command.

    :param success: One entry per resolved click.
    """

    success: list[ClickCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ClickCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[ClickCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class DoubleClickCommandResponse:
    """Result payload of a successful ``doubleClick`` command.

    :param new_url: URL after the double click, if navigation occurred.
    """

    new_url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> DoubleClickCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(new_url=d.get("newUrl"))


@dataclass
class DoubleClickCommandSuccess:
    """Success outcome of a ``doubleClick`` command.

    :param success: One entry per resolved double click.
    """

    success: list[DoubleClickCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> DoubleClickCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[DoubleClickCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class FillCommandResponse:
    """Result payload of a successful ``fill`` command.

    :param new_value: Value present in the field after filling.
    """

    new_value: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> FillCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(new_value=d.get("newValue"))


@dataclass
class FillCommandSuccess:
    """Success outcome of a ``fill`` command.

    :param success: One entry per resolved fill.
    """

    success: list[FillCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> FillCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[FillCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class SelectCommandResponse:
    """Result payload of a successful ``select`` command.

    :param selected_options: Options selected as a result of the command.
    """

    selected_options: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> SelectCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(selected_options=d.get("selectedOptions", []))


@dataclass
class SelectCommandSuccess:
    """Success outcome of a ``select`` command.

    :param success: One entry per resolved select.
    """

    success: list[SelectCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> SelectCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[SelectCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class PressKeyCommandResponse:
    """Result payload of a successful ``pressKey`` command.

    :param new_url: URL after pressing the keys, if navigation occurred.
    """

    new_url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> PressKeyCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(new_url=d.get("newUrl"))


@dataclass
class PressKeyCommandSuccess:
    """Success outcome of a ``pressKey`` command.

    :param success: One entry per resolved key press.
    """

    success: list[PressKeyCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> PressKeyCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[PressKeyCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class ScrollCommandResponse:
    """Result payload of a successful ``scroll`` command.

    :param direction: Direction of the scroll, ``'up'`` or ``'down'``.
    :param delta: Number of pixels scrolled.
    """

    direction: str | None = None
    delta: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ScrollCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(direction=d.get("direction"), delta=d.get("delta"))


@dataclass
class ScrollCommandSuccess:
    """Success outcome of a ``scroll`` command.

    :param success: One entry per resolved scroll.
    """

    success: list[ScrollCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> ScrollCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[ScrollCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class GotoCommandResponse:
    """Result payload of a successful ``goto`` command.

    :param url: URL that was reached.
    """

    url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> GotoCommandResponse:
        """Build from a JSON-decoded response dict."""
        return cls(url=d.get("url"))


@dataclass
class GotoCommandSuccess:
    """Success outcome of a ``goto`` command.

    :param success: One entry per resolved navigation.
    """

    success: list[GotoCommandResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> GotoCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=[GotoCommandResponse.from_dict(x) for x in d.get("success", [])])


@dataclass
class HoverCommandSuccess:
    """Success outcome of a ``hover`` command.

    :param success: Whether the hover succeeded.
    """

    success: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> HoverCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=bool(d.get("success")))


@dataclass
class TypeCommandSuccess:
    """Success outcome of a ``type`` command.

    :param success: Whether the type succeeded.
    """

    success: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> TypeCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=bool(d.get("success")))


@dataclass
class DragCommandSuccess:
    """Success outcome of a ``drag`` command.

    :param success: Whether the drag succeeded.
    """

    success: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> DragCommandSuccess:
        """Build from a JSON-decoded response dict."""
        return cls(success=bool(d.get("success")))


def _parse_command_response(raw: dict | None, success_from_dict: Callable[[dict], Any]) -> Any:
    """Parse a command ``response`` into an error or a command-specific success object.

    :param raw: Raw ``response`` dict, or ``None`` when the command has not resolved yet.
    :param success_from_dict: The ``from_dict`` of the command's success type, used when there is no error.

    :returns: An :class:`ErrorResponse`, a command-specific success object, or ``None``.
    """
    if raw is None:
        return None
    if "error" in raw:
        return ErrorResponse.from_dict(raw)
    return success_from_dict(raw)


@dataclass
class ClickCommand:
    """A ``click`` browser command executed during a step.

    :param name: Command discriminator (``'click'``).
    :param button: Mouse button used, e.g. ``'left'``.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`ClickCommandSuccess`).
    """

    name: str
    button: str | None = None
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | ClickCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ClickCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            button=d.get("button"),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), ClickCommandSuccess.from_dict),
        )


@dataclass
class DoubleClickCommand:
    """A ``doubleClick`` browser command executed during a step.

    :param name: Command discriminator (``'doubleClick'``).
    :param button: Mouse button used, e.g. ``'left'``.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`DoubleClickCommandSuccess`).
    """

    name: str
    button: str | None = None
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | DoubleClickCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> DoubleClickCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            button=d.get("button"),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), DoubleClickCommandSuccess.from_dict),
        )


@dataclass
class FillCommand:
    """A ``fill`` browser command executed during a step.

    :param name: Command discriminator (``'fill'``).
    :param value: Value used to fill the input.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`FillCommandSuccess`).
    """

    name: str
    value: str | None = None
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | FillCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> FillCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            value=d.get("value"),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), FillCommandSuccess.from_dict),
        )


@dataclass
class SelectCommand:
    """A ``select`` browser command executed during a step.

    :param name: Command discriminator (``'select'``).
    :param value: Concatenated selected options.
    :param options: Selected options.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`SelectCommandSuccess`).
    """

    name: str
    value: str | None = None
    options: list[str] = field(default_factory=list)
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | SelectCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> SelectCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            value=d.get("value"),
            options=d.get("options", []),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), SelectCommandSuccess.from_dict),
        )


@dataclass
class PressKeyCommand:
    """A ``pressKey`` browser command executed during a step.

    :param name: Command discriminator (``'pressKey'``).
    :param value: Sequence of keys, comma separated.
    :param keys_sequence: Sequence of keys as a list.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`PressKeyCommandSuccess`).
    """

    name: str
    value: str | None = None
    keys_sequence: list[str] = field(default_factory=list)
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | PressKeyCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> PressKeyCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            value=d.get("value"),
            keys_sequence=d.get("keysSequence", []),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), PressKeyCommandSuccess.from_dict),
        )


@dataclass
class ScrollCommand:
    """A ``scroll`` browser command executed during a step.

    :param name: Command discriminator (``'scroll'``).
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`ScrollCommandSuccess`).
    """

    name: str
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | ScrollCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ScrollCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), ScrollCommandSuccess.from_dict),
        )


@dataclass
class HoverCommand:
    """A ``hover`` browser command executed during a step.

    :param name: Command discriminator (``'hover'``).
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`HoverCommandSuccess`).
    """

    name: str
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | HoverCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> HoverCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), HoverCommandSuccess.from_dict),
        )


@dataclass
class TypeCommand:
    """A ``type`` browser command executed during a step.

    :param name: Command discriminator (``'type'``).
    :param value: Value typed.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`TypeCommandSuccess`).
    """

    name: str
    value: str | None = None
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | TypeCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> TypeCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            value=d.get("value"),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), TypeCommandSuccess.from_dict),
        )


@dataclass
class DragCommand:
    """A ``drag`` browser command executed during a step.

    :param name: Command discriminator (``'drag'``).
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`DragCommandSuccess`).
    """

    name: str
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | DragCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> DragCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), DragCommandSuccess.from_dict),
        )


@dataclass
class GotoCommand:
    """A ``goto`` browser command executed during a step.

    :param name: Command discriminator (``'goto'``).
    :param url: URL to reach.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param response: Command outcome (:class:`ErrorResponse` or :class:`GotoCommandSuccess`).
    """

    name: str
    url: str | None = None
    html_element: str | None = None
    screenshot: str | None = None
    response: ErrorResponse | GotoCommandSuccess | None = None

    @classmethod
    def from_dict(cls, d: dict) -> GotoCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d["name"],
            url=d.get("url"),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            response=_parse_command_response(d.get("response"), GotoCommandSuccess.from_dict),
        )


@dataclass
class GenericCommand:
    """Fallback command used when the ``name`` discriminator is not recognised.

    Preserves forward compatibility with command types introduced after this client was released.

    :param name: Raw command name.
    :param html_element: Plain-text description of the targeted element, if any.
    :param screenshot: Screenshot UUID captured after the command, if any.
    :param raw: The unparsed command dict as received from the API.
    """

    name: str
    html_element: str | None = None
    screenshot: str | None = None
    raw: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> GenericCommand:
        """Build from a JSON-decoded command dict."""
        return cls(
            name=d.get("name", ""),
            html_element=d.get("htmlElement"),
            screenshot=d.get("screenshot"),
            raw=d,
        )


if TYPE_CHECKING:
    Command = (
        ClickCommand
        | DoubleClickCommand
        | FillCommand
        | SelectCommand
        | PressKeyCommand
        | ScrollCommand
        | HoverCommand
        | TypeCommand
        | DragCommand
        | GotoCommand
        | GenericCommand
    )

_COMMAND_CLASSES: dict[str, type] = {
    "click": ClickCommand,
    "doubleClick": DoubleClickCommand,
    "fill": FillCommand,
    "select": SelectCommand,
    "pressKey": PressKeyCommand,
    "scroll": ScrollCommand,
    "hover": HoverCommand,
    "type": TypeCommand,
    "drag": DragCommand,
    "goto": GotoCommand,
}


def parse_command(d: dict) -> Command:
    """Parse a single command dict into the matching typed command object.

    Dispatches on the ``name`` discriminator. Unknown names fall back to :class:`GenericCommand`.

    :param d: JSON-decoded command dict.

    :returns: A typed command object.
    """
    command_cls: Any = _COMMAND_CLASSES.get(d.get("name", ""), GenericCommand)
    return command_cls.from_dict(d)


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
