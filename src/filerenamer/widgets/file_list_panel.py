"""File list panel widget displaying files in a two-column table."""

from pathlib import Path
from typing import List, Optional

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import DataTable, Input, Label
from textual.widgets.data_table import RowKey

from ..models import FileItem


class FileSelectionChanged(Message):
    """Message sent when file selection changes."""

    def __init__(self, files: List[FileItem]) -> None:
        self.files = files
        super().__init__()


class FileListPanel(Container):
    """Panel displaying the list of files with original and new names."""

    DEFAULT_CSS = """
    FileListPanel {
        height: 1fr;
        background: $surface;
        border: solid $primary;
    }

    DataTable {
        height: 1fr;
    }

    #edit-container {
        display: none;
        height: 3;
        background: $panel;
        border: solid $accent;
        padding: 1;
    }

    #edit-label {
        width: 15;
    }

    #edit-input {
        width: 1fr;
    }
    """

    BINDINGS = [
        ("space", "toggle_selection", "Toggle Selection"),
        ("enter", "edit_name", "Edit Name"),
        ("ctrl+a", "toggle_all", "Toggle All"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.files: List[FileItem] = []
        self.row_to_index: dict[RowKey, int] = {}
        self.editing_row: Optional[int] = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield DataTable(id="file-table", cursor_type="row")

    def on_mount(self) -> None:
        """Initialize the data table."""
        table = self.query_one(DataTable)
        table.add_column("Original Name", key="original", width=None)
        table.add_column("New Name", key="new", width=None)

    def populate_files(self, files: List[FileItem]) -> None:
        """
        Populate the table with file items.

        Args:
            files: List of FileItem objects to display
        """
        self.files = files
        table = self.query_one(DataTable)
        table.clear()
        self.row_to_index.clear()

        for idx, file_item in enumerate(files):
            original_col = self._format_original_name(file_item)
            new_col = self._format_new_name(file_item)

            row_key = table.add_row(original_col, new_col)
            self.row_to_index[row_key] = idx

    def update_preview(self, files: List[FileItem]) -> None:
        """
        Update the preview column with new names.

        Args:
            files: Updated list of FileItem objects
        """
        self.files = files
        table = self.query_one(DataTable)

        for row_key, idx in self.row_to_index.items():
            if idx < len(files):
                file_item = files[idx]
                original_col = self._format_original_name(file_item)
                new_col = self._format_new_name(file_item)

                table.update_cell(row_key, "original", original_col)
                table.update_cell(row_key, "new", new_col)

    def _format_original_name(self, file_item: FileItem) -> Text:
        """Format the original name column with selection indicator and indentation."""
        indent = "  " * file_item.depth
        indicator = "✓" if file_item.is_selected else "□"
        name = file_item.original_name

        if file_item.is_directory:
            name += "/"

        text = Text()
        text.append(indent)
        text.append(f"{indicator} ", style="bold cyan" if file_item.is_selected else "dim")
        text.append(name, style="bold blue" if file_item.is_directory else "")

        return text

    def _format_new_name(self, file_item: FileItem) -> Text:
        """Format the new name column with highlighting for changes."""
        text = Text()

        if file_item.is_directory:
            # Don't show new name for directories (not renaming them in this version)
            text.append("")
        elif file_item.is_changed:
            # Highlight changed names
            style = "bold green" if file_item.is_selected else "green"
            text.append(file_item.new_name, style=style)
            if file_item.is_custom_override:
                text.append(" ✏", style="yellow")
        else:
            # No change
            text.append(file_item.new_name, style="dim")

        return text

    def action_toggle_selection(self) -> None:
        """Toggle selection of the current row."""
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return

        # Use cursor row index directly
        idx = table.cursor_row
        if idx < len(self.files):
            current_file = self.files[idx]
            new_state = not current_file.is_selected
            current_file.is_selected = new_state

            # If this is a directory, also toggle all contained files
            if current_file.is_directory:
                dir_depth = current_file.depth
                # Find all files that are children of this directory
                for i in range(idx + 1, len(self.files)):
                    # Stop when we reach a file at the same or lower depth
                    if self.files[i].depth <= dir_depth:
                        break
                    # Toggle all children to match the directory's new state
                    self.files[i].is_selected = new_state

            self.update_preview(self.files)
            self.post_message(FileSelectionChanged(self.files))

    def action_toggle_all(self) -> None:
        """Toggle selection of all files."""
        if not self.files:
            return

        # Check if all are selected
        all_selected = all(f.is_selected for f in self.files)

        # Toggle all to opposite state
        for file_item in self.files:
            file_item.is_selected = not all_selected

        self.update_preview(self.files)
        self.post_message(FileSelectionChanged(self.files))

    def action_edit_name(self) -> None:
        """Open inline editor for the current row."""
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return

        # Use cursor row index directly
        idx = table.cursor_row
        if idx < len(self.files):
            file_item = self.files[idx]

            # Don't edit directories
            if file_item.is_directory:
                return

            self.editing_row = idx
            self._show_edit_dialog(file_item)

    def _show_edit_dialog(self, file_item: FileItem) -> None:
        """Show an edit dialog for a specific file."""
        from textual.containers import Horizontal

        # Create edit container if it doesn't exist
        try:
            edit_container = self.query_one("#edit-container")
        except:
            edit_container = Container(id="edit-container")
            with edit_container:
                Horizontal(
                    Label(f"Edit name:", id="edit-label"),
                    Input(value=file_item.new_name, id="edit-input")
                )
            self.mount(edit_container)

        # Show the container and populate with current value
        edit_container.styles.display = "block"
        edit_input = self.query_one("#edit-input", Input)
        edit_input.value = file_item.new_name
        edit_input.focus()

    @on(Input.Submitted, "#edit-input")
    def on_edit_submitted(self, event: Input.Submitted) -> None:
        """Handle edit input submission."""
        if self.editing_row is not None:
            idx = self.editing_row
            if idx < len(self.files):
                self.files[idx].new_name = event.value
                self.files[idx].is_custom_override = True
                self.update_preview(self.files)
                self.post_message(FileSelectionChanged(self.files))

        self._hide_edit_dialog()

    def _hide_edit_dialog(self) -> None:
        """Hide the edit dialog."""
        try:
            edit_container = self.query_one("#edit-container")
            edit_container.styles.display = "none"
            self.query_one(DataTable).focus()
        except:
            pass

        self.editing_row = None

    def get_selected_count(self) -> int:
        """Get the number of selected files."""
        return sum(1 for f in self.files if f.is_selected)

    def get_changed_count(self) -> int:
        """Get the number of files with changed names."""
        return sum(1 for f in self.files if f.is_changed and f.is_selected)
