"""Browser command read models and the discriminator-based command parser."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


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
