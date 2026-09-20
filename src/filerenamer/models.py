"""Data models for file renaming operations."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class FileItem:
    """Represents a single file or directory to be renamed."""

    original_path: Path
    original_name: str
    new_name: str
    is_selected: bool = True
    is_custom_override: bool = False
    is_directory: bool = False
    depth: int = 0
    parent_path: Optional[Path] = None
    relative_path: Optional[Path] = None
    root_path: Optional[Path] = None
    is_whole_path: bool = False

    @property
    def is_changed(self) -> bool:
        """Check if the new name differs from the original."""
        if self.is_whole_path and self.relative_path is not None:
            return self.relative_path.as_posix() != self.new_name
        return self.original_name != self.new_name

    @property
    def full_new_path(self) -> Path:
        """Get the full path with the new name."""
        # In whole-path mode the new name represents a full path relative to
        # the scan root (it may collapse or add directory segments), so
        # resolve it against the root rather than the original parent dir.
        if self.is_whole_path and self.root_path is not None:
            return self.root_path / self.new_name
        if self.parent_path:
            return self.parent_path / self.new_name
        return self.original_path.parent / self.new_name


@dataclass
class RenameOperation:
    """Holds the parameters for a rename operation."""

    search_pattern: str = ""
    replace_pattern: str = ""
    case_sensitive: bool = True
    use_regex: bool = True
    whole_path: bool = False

    def is_valid(self) -> bool:
        """Check if the operation has valid parameters."""
        return len(self.search_pattern) > 0


@dataclass
class FileTreeNode:
    """Represents a node in the directory tree structure."""

    path: Path
    name: str
    is_directory: bool
    children: List['FileTreeNode'] = field(default_factory=list)
    depth: int = 0
    is_expanded: bool = True

    def add_child(self, node: 'FileTreeNode') -> None:
        """Add a child node to this directory."""
        self.children.append(node)
        node.depth = self.depth + 1


@dataclass
class RenameResult:
    """Result of a rename operation."""

    success: bool
    old_path: Path
    new_path: Optional[Path] = None
    error: Optional[str] = None
