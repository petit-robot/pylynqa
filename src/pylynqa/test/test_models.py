"""Unit tests for :mod:`pylynqa.models`."""
# ruff: file-ignore[undocumented-public-class,no-self-use]

from pylynqa.models import (
    AssertionsReport,
    ClickCommand,
    ClickCommandSuccess,
    CreateAttachment,
    CreateGherkinTest,
    CreateTest,
    CreateTestStep,
    DragCommand,
    DragCommandSuccess,
    ErrorResponse,
    FillCommand,
    GenericCommand,
    GotoCommand,
    GotoCommandSuccess,
    HoverCommand,
    ScrollCommand,
    ScrollCommandSuccess,
    SelectCommand,
    SelectCommandSuccess,
    StepReport,
    TestData,
    TestRunContext,
    TextualData,
    parse_command,
)


class TestCreateTest:
    def test_required_fields_only(self):
        """Only url and steps are serialised when optionals are unset."""
        test = CreateTest(url="https://example.com", steps=[CreateTestStep(action="Click login")])

        assert test.to_dict() == {
            "url": "https://example.com",
            "steps": [{"action": "Click login"}],
        }

    def test_all_optional_fields(self):
        """Optional fields are serialised with their API (camelCase) keys."""
        test = CreateTest(
            url="https://example.com",
            steps=[CreateTestStep(action="Click login")],
            name="My test",
            context=TestRunContext(client_language="en-US", secrets=[TestData(name="pwd", value="s3cr3t")]),
            guidance=[TextualData(text="hint")],
            attachments=[CreateAttachment(name="f.txt", data="data:text/plain;base64,SmFuZQo=")],
            webhooks=["https://hook.example.com"],
        )

        assert test.to_dict() == {
            "url": "https://example.com",
            "steps": [{"action": "Click login"}],
            "name": "My test",
            "context": {"clientLanguage": "en-US", "secrets": [{"name": "pwd", "value": "s3cr3t"}]},
            "guidance": [{"text": "hint"}],
            "attachments": [{"name": "f.txt", "data": "data:text/plain;base64,SmFuZQo="}],
            "webhooks": ["https://hook.example.com"],
        }


class TestCreateGherkinTest:
    def test_required_fields_only(self):
        """Only url and scenario are serialised when optionals are unset."""
        test = CreateGherkinTest(url="https://example.com", scenario="Given I am logged in")

        assert test.to_dict() == {"url": "https://example.com", "scenario": "Given I am logged in"}

    def test_all_optional_fields(self):
        """Optional fields are serialised with their API (camelCase) keys."""
        test = CreateGherkinTest(
            url="https://example.com",
            scenario="Given I am logged in",
            name="My gherkin",
            guidance=[TextualData(text="hint")],
            webhooks=["https://hook.example.com"],
        )

        assert test.to_dict() == {
            "url": "https://example.com",
            "scenario": "Given I am logged in",
            "name": "My gherkin",
            "guidance": [{"text": "hint"}],
            "webhooks": ["https://hook.example.com"],
        }


class TestParseCommand:
    def test_click_success(self):
        """A click command resolves to a ClickCommand with a typed success response."""
        command = parse_command(
            {
                "name": "click",
                "button": "left",
                "htmlElement": "The button",
                "screenshot": "uuid-1",
                "response": {"success": [{"newUrl": "https://example.com/next"}]},
            }
        )

        assert isinstance(command, ClickCommand)
        assert command.button == "left"
        assert command.screenshot == "uuid-1"
        assert isinstance(command.response, ClickCommandSuccess)
        assert command.response.success[0].new_url == "https://example.com/next"

    def test_error_response(self):
        """A command with an error payload resolves to an ErrorResponse."""
        command = parse_command({"name": "fill", "value": "x", "response": {"error": "not_visible_element"}})

        assert isinstance(command, FillCommand)
        assert isinstance(command.response, ErrorResponse)
        assert command.response.error == "not_visible_element"

    def test_missing_response_is_none(self):
        """A command that has not resolved yet has a None response."""
        command = parse_command({"name": "hover", "htmlElement": "The menu"})

        assert isinstance(command, HoverCommand)
        assert command.response is None

    def test_boolean_success(self):
        """Drag/hover/type expose a boolean success flag."""
        command = parse_command({"name": "drag", "response": {"success": True}})

        assert isinstance(command, DragCommand)
        assert isinstance(command.response, DragCommandSuccess)
        assert command.response.success is True

    def test_select_options(self):
        """A select command keeps both the concatenated value and the option list."""
        command = parse_command(
            {
                "name": "select",
                "value": "apple,lemon",
                "options": ["apple", "lemon"],
                "response": {"success": [{"selectedOptions": ["apple", "lemon"]}]},
            }
        )

        assert isinstance(command, SelectCommand)
        assert command.options == ["apple", "lemon"]
        assert isinstance(command.response, SelectCommandSuccess)
        assert command.response.success[0].selected_options == ["apple", "lemon"]

    def test_scroll_response(self):
        """A scroll command exposes direction and delta."""
        delta = 500
        command = parse_command({"name": "scroll", "response": {"success": [{"direction": "down", "delta": delta}]}})

        assert isinstance(command, ScrollCommand)
        assert isinstance(command.response, ScrollCommandSuccess)
        assert command.response.success[0].direction == "down"
        assert command.response.success[0].delta == delta

    def test_goto_response(self):
        """A goto command exposes the reached url."""
        command = parse_command(
            {"name": "goto", "url": "https://example.com", "response": {"success": [{"url": "https://example.com/x"}]}}
        )

        assert isinstance(command, GotoCommand)
        assert command.url == "https://example.com"
        assert isinstance(command.response, GotoCommandSuccess)
        assert command.response.success[0].url == "https://example.com/x"

    def test_unknown_command_falls_back_to_generic(self):
        """An unrecognised command name is preserved as a GenericCommand."""
        raw = {"name": "teleport", "htmlElement": "Somewhere", "screenshot": "uuid-2"}
        command = parse_command(raw)

        assert isinstance(command, GenericCommand)
        assert command.name == "teleport"
        assert command.screenshot == "uuid-2"
        assert command.raw == raw


class TestStepReport:
    def test_from_dict_full(self):
        """A full step report parses commands and the assertions report."""
        report = StepReport.from_dict(
            {
                "commands": [{"name": "fill", "value": "x", "response": {"success": [{"newValue": "x"}]}}],
                "status": "failed",
                "start": "2025-09-18T09:01:02.000Z",
                "end": "2025-09-18T09:01:05.500Z",
                "assertionsReport": {
                    "assertions": [{"checked": False, "assertion": "The first search result concerns 'Page Login'"}],
                    "screenshot": "1ff7d9a2-9608-4bca-b94a-ee8fef6d6335",
                },
                "testVerdictCause": "Expected URL to contain /dashboard",
                "error": "internal"
            }
        )

        assert report.status == "failed"
        assert isinstance(report.commands[0], FillCommand)
        assert isinstance(report.assertions_report, AssertionsReport)
        assert report.assertions_report.assertions[0].checked is False
        assert report.assertions_report.screenshot == "1ff7d9a2-9608-4bca-b94a-ee8fef6d6335"
        assert report.test_verdict_cause == "Expected URL to contain /dashboard"
        assert report.error == "internal"

    def test_from_dict_minimal(self):
        """Missing optional sections leave defaults in place."""
        report = StepReport.from_dict({"status": "running"})

        assert report.status == "running"
        assert report.commands == []
        assert report.assertions_report is None
        assert report.start is None
