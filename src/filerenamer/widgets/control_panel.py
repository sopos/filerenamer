"""Control panel widget with search/replace inputs and action buttons."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Checkbox, Input, Label, Static

from ..models import RenameOperation


class PatternChanged(Message):
    """Message sent when search/replace pattern changes."""

    def __init__(self, operation: RenameOperation) -> None:
        self.operation = operation
        super().__init__()


class ApplyRename(Message):
    """Message sent when Apply button is clicked."""
    pass


class ControlPanel(Container):
    """Control panel for search/replace inputs and buttons."""

    DEFAULT_CSS = """
    ControlPanel {
        height: auto;
        background: $surface;
        border: solid $primary;
        padding: 1;
    }

    #search-container, #replace-container {
        height: auto;
        margin-bottom: 1;
    }

    #search-label, #replace-label {
        width: 10;
        content-align: right middle;
    }

    #search-input, #replace-input {
        width: 1fr;
    }

    #options-container {
        height: auto;
        margin-top: 1;
    }

    #case-checkbox {
        width: 22;
    }

    #whole-path-checkbox {
        width: 22;
    }

    #button-container {
        width: auto;
        height: auto;
    }

    Button {
        margin-left: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.search_pattern = ""
        self.replace_pattern = ""
        self.case_sensitive = True
        self.whole_path = True

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Horizontal(id="search-container"):
            yield Label("Search:", id="search-label")
            yield Input(placeholder="regex pattern or text", id="search-input")

        with Horizontal(id="replace-container"):
            yield Label("Replace:", id="replace-label")
            yield Input(placeholder="replacement text", id="replace-input")

        with Horizontal(id="options-container"):
            yield Checkbox("Case Sensitive", value=True, id="case-checkbox")
            yield Checkbox("Whole Path", value=True, id="whole-path-checkbox")
            with Horizontal(id="button-container"):
                yield Button("Apply", variant="primary", id="apply-button")
                yield Button("Exit", variant="error", id="exit-button")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input field changes."""
        if event.input.id == "search-input":
            self.search_pattern = event.value
        elif event.input.id == "replace-input":
            self.replace_pattern = event.value

        # Emit pattern changed message
        self._emit_pattern_changed()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if event.checkbox.id == "case-checkbox":
            self.case_sensitive = event.value
            self._emit_pattern_changed()
        elif event.checkbox.id == "whole-path-checkbox":
            self.whole_path = event.value
            self._emit_pattern_changed()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "apply-button":
            self.post_message(ApplyRename())
        elif event.button.id == "exit-button":
            self.app.exit()

    def _emit_pattern_changed(self) -> None:
        """Emit a pattern changed message with current operation."""
        operation = RenameOperation(
            search_pattern=self.search_pattern,
            replace_pattern=self.replace_pattern,
            case_sensitive=self.case_sensitive,
            use_regex=True
        )
        self.post_message(PatternChanged(operation))

    def get_current_operation(self) -> RenameOperation:
        """Get the current rename operation."""
        return RenameOperation(
            search_pattern=self.search_pattern,
            replace_pattern=self.replace_pattern,
            case_sensitive=self.case_sensitive,
            use_regex=True,
            whole_path=self.whole_path
        )
