"""Main application for the File Renamer TUI."""

from pathlib import Path
from typing import List

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Footer, Header, Label

from .models import FileItem, RenameOperation
from .utils.file_scanner import scan_directory, apply_renames, validate_renames
from .utils.renamer import preview_renames, validate_pattern
from .widgets.control_panel import ControlPanel, PatternChanged, ApplyRename
from .widgets.file_list_panel import FileListPanel, FileSelectionChanged


class FileRenamerApp(App):
    """A TUI application for batch file renaming with regex support."""

    CSS = """
    Screen {
        background: $background;
    }

    #main-container {
        height: 1fr;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $panel;
        color: $text;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "quit", "Quit", priority=True),
        ("tab", "focus_next", "Next"),
        ("shift+tab", "focus_previous", "Previous"),
    ]

    def __init__(self, start_path: Path = None):
        super().__init__()
        self.start_path = start_path or Path.cwd()
        self.files: List[FileItem] = []
        self.current_operation = RenameOperation()

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        with Vertical(id="main-container"):
            yield ControlPanel()
            yield FileListPanel()
        yield Label("", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application on mount."""
        self.title = "File Renamer"
        self.sub_title = str(self.start_path)

        # Scan the directory and populate files
        self._scan_and_populate()

        # Set initial focus to search input
        search_input = self.query_one("#search-input")
        search_input.focus()

    def _scan_and_populate(self) -> None:
        """Scan the directory and populate the file list."""
        try:
            self.files = scan_directory(self.start_path)
            file_list = self.query_one(FileListPanel)
            file_list.populate_files(self.files)
            self._update_status()
        except Exception as e:
            self._show_error(f"Error scanning directory: {str(e)}")

    def on_pattern_changed(self, message: PatternChanged) -> None:
        """Handle pattern change from control panel."""
        self.current_operation = message.operation

        # Validate the pattern
        is_valid, error = validate_pattern(message.operation.search_pattern)
        if not is_valid:
            self._show_error(f"Invalid regex: {error}")
            return

        # Update preview
        self._update_preview()

    def on_file_selection_changed(self, message: FileSelectionChanged) -> None:
        """Handle file selection changes from file list panel."""
        self.files = message.files
        self._update_status()

    def on_apply_rename(self, message: ApplyRename) -> None:
        """Handle apply rename action."""
        # Validate renames
        errors = validate_renames(self.files)
        if errors:
            error_msg = "\\n".join(errors[:3])
            self._show_error(f"Validation errors: {error_msg}")
            return

        # Count files to be renamed
        files_to_rename = [f for f in self.files if f.is_selected and f.is_changed]
        if not files_to_rename:
            self._show_error("No files to rename")
            return

        # Apply renames
        try:
            results = apply_renames(self.files)

            # Count successes and failures
            successes = sum(1 for r in results.values() if r.success)
            failures = sum(1 for r in results.values() if not r.success)

            if failures > 0:
                # Show first error
                first_error = next((r.error for r in results.values() if not r.success), "Unknown error")
                self._show_error(f"Renamed {successes} files, {failures} failed: {first_error}")
            else:
                self._show_success(f"Successfully renamed {successes} files")

            # Rescan directory to reflect changes
            self._scan_and_populate()

        except Exception as e:
            self._show_error(f"Error applying renames: {str(e)}")

    def _update_preview(self) -> None:
        """Update the preview of renamed files."""
        if not self.current_operation.search_pattern:
            # Reset to original names if no pattern
            for file_item in self.files:
                if not file_item.is_custom_override:
                    file_item.new_name = file_item.original_name
                    file_item.is_whole_path = False
        else:
            # Apply the pattern
            self.files = preview_renames(self.files, self.current_operation)

        # Update the file list display
        file_list = self.query_one(FileListPanel)
        file_list.update_preview(self.files)
        self._update_status()

    def _update_status(self) -> None:
        """Update the status bar."""
        file_list = self.query_one(FileListPanel)
        selected = file_list.get_selected_count()
        changed = file_list.get_changed_count()
        total = len(self.files)

        status_bar = self.query_one("#status-bar", Label)
        status_bar.update(
            f"Files: {total} | Selected: {selected} | Will rename: {changed}"
        )

    def _show_error(self, message: str) -> None:
        """Show an error message in the status bar."""
        status_bar = self.query_one("#status-bar", Label)
        status_bar.update(f"[bold red]Error:[/bold red] {message}")
        status_bar.styles.background = "red 30%"

        # Reset after a delay
        self.set_timer(3.0, self._update_status)

    def _show_success(self, message: str) -> None:
        """Show a success message in the status bar."""
        status_bar = self.query_one("#status-bar", Label)
        status_bar.update(f"[bold green]Success:[/bold green] {message}")
        status_bar.styles.background = "green 30%"

        # Reset after a delay
        self.set_timer(3.0, self._update_status)

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
