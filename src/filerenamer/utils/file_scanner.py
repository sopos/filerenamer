"""File system scanning and rename application utilities."""

import os
from pathlib import Path
from typing import List, Dict

from ..models import FileItem, RenameResult


def scan_directory(path: Path, max_depth: int = 10) -> List[FileItem]:
    """
    Recursively scan a directory and return a list of FileItem objects.

    Args:
        path: The directory path to scan
        max_depth: Maximum depth to traverse (prevents infinite recursion)

    Returns:
        List of FileItem objects representing all files and directories
    """
    items = []

    def _scan(current_path: Path, depth: int = 0) -> None:
        if depth > max_depth:
            return

        try:
            entries = sorted(current_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))

            for entry in entries:
                # Skip hidden files and directories starting with .
                if entry.name.startswith('.'):
                    continue

                is_dir = entry.is_dir()
                relative_path = entry.relative_to(path)

                item = FileItem(
                    original_path=entry,
                    original_name=entry.name,
                    new_name=entry.name,
                    is_directory=is_dir,
                    depth=depth,
                    parent_path=entry.parent
                )
                items.append(item)

                # Recursively scan subdirectories
                if is_dir:
                    _scan(entry, depth + 1)

        except PermissionError:
            pass
        except Exception:
            pass

    _scan(path)
    return items


def apply_renames(items: List[FileItem]) -> Dict[Path, RenameResult]:
    """
    Apply the rename operations to selected files.

    Args:
        items: List of FileItem objects to rename

    Returns:
        Dictionary mapping original paths to RenameResult objects
    """
    results = {}

    # Sort by depth (deepest first) to avoid renaming parent directories
    # before their children
    sorted_items = sorted(
        [item for item in items if item.is_selected and item.is_changed],
        key=lambda x: x.depth,
        reverse=True
    )

    for item in sorted_items:
        try:
            new_path = item.full_new_path

            # Check if target already exists
            if new_path.exists() and new_path != item.original_path:
                results[item.original_path] = RenameResult(
                    success=False,
                    old_path=item.original_path,
                    error=f"Target already exists: {new_path}"
                )
                continue

            # Perform the rename
            item.original_path.rename(new_path)

            results[item.original_path] = RenameResult(
                success=True,
                old_path=item.original_path,
                new_path=new_path
            )

        except PermissionError as e:
            results[item.original_path] = RenameResult(
                success=False,
                old_path=item.original_path,
                error=f"Permission denied: {str(e)}"
            )
        except OSError as e:
            results[item.original_path] = RenameResult(
                success=False,
                old_path=item.original_path,
                error=f"OS error: {str(e)}"
            )
        except Exception as e:
            results[item.original_path] = RenameResult(
                success=False,
                old_path=item.original_path,
                error=f"Unexpected error: {str(e)}"
            )

    return results


def validate_renames(items: List[FileItem]) -> List[str]:
    """
    Validate that the rename operations won't cause conflicts.

    Args:
        items: List of FileItem objects to validate

    Returns:
        List of error messages (empty if no conflicts)
    """
    errors = []
    selected_items = [item for item in items if item.is_selected and item.is_changed]

    # Check for duplicate new names in the same directory
    new_names_by_dir: Dict[Path, List[str]] = {}

    for item in selected_items:
        parent = item.original_path.parent
        new_name = item.new_name

        if parent not in new_names_by_dir:
            new_names_by_dir[parent] = []

        if new_name in new_names_by_dir[parent]:
            errors.append(f"Duplicate name in {parent}: {new_name}")
        else:
            new_names_by_dir[parent].append(new_name)

    return errors
