"""Tests for rename utility functions."""

import pytest
from pathlib import Path

from filerenamer.models import FileItem, RenameOperation
from filerenamer.utils.renamer import (
    apply_pattern,
    validate_pattern,
    preview_renames,
    get_file_extension
)


class TestValidatePattern:
    """Tests for validate_pattern function."""

    def test_valid_pattern(self):
        is_valid, error = validate_pattern(r"file(\d+)")
        assert is_valid
        assert error is None

    def test_invalid_pattern(self):
        is_valid, error = validate_pattern(r"file(")
        assert not is_valid
        assert error is not None

    def test_empty_pattern(self):
        is_valid, error = validate_pattern("")
        assert is_valid
        assert error is None


class TestApplyPattern:
    """Tests for apply_pattern function."""

    def test_simple_replacement(self):
        result = apply_pattern("file.txt", "file", "document", case_sensitive=True)
        assert result == "document.txt"

    def test_case_sensitive(self):
        result = apply_pattern("File.txt", "file", "document", case_sensitive=True)
        assert result == "File.txt"  # No match due to case

    def test_case_insensitive(self):
        result = apply_pattern("File.txt", "file", "document", case_sensitive=False)
        assert result == "document.txt"

    def test_regex_pattern(self):
        result = apply_pattern("file123.txt", r"file(\d+)", r"doc\1", use_regex=True)
        assert result == "doc123.txt"

    def test_regex_capture_groups(self):
        result = apply_pattern("test_file.txt", r"(\w+)_(\w+)", r"\2_\1", use_regex=True)
        assert result == "file_test.txt"

    def test_plain_text_mode(self):
        result = apply_pattern("file.txt", "file", "doc", use_regex=False)
        assert result == "doc.txt"

    def test_empty_search(self):
        result = apply_pattern("file.txt", "", "doc")
        assert result == "file.txt"


class TestPreviewRenames:
    """Tests for preview_renames function."""

    def test_preview_simple_rename(self):
        files = [
            FileItem(
                original_path=Path("file1.txt"),
                original_name="file1.txt",
                new_name="file1.txt",
                is_selected=True
            ),
            FileItem(
                original_path=Path("file2.txt"),
                original_name="file2.txt",
                new_name="file2.txt",
                is_selected=True
            ),
        ]

        operation = RenameOperation(
            search_pattern="file",
            replace_pattern="doc",
            case_sensitive=True,
            use_regex=False
        )

        result = preview_renames(files, operation)

        assert result[0].new_name == "doc1.txt"
        assert result[1].new_name == "doc2.txt"

    def test_preview_custom_override_preserved(self):
        files = [
            FileItem(
                original_path=Path("file1.txt"),
                original_name="file1.txt",
                new_name="custom.txt",
                is_selected=True,
                is_custom_override=True
            ),
        ]

        operation = RenameOperation(
            search_pattern="file",
            replace_pattern="doc",
            case_sensitive=True,
            use_regex=False
        )

        result = preview_renames(files, operation)

        # Custom override should be preserved
        assert result[0].new_name == "custom.txt"


class TestGetFileExtension:
    """Tests for get_file_extension function."""

    def test_simple_extension(self):
        name, ext = get_file_extension("file.txt")
        assert name == "file"
        assert ext == ".txt"

    def test_multiple_dots(self):
        name, ext = get_file_extension("my.file.txt")
        assert name == "my.file"
        assert ext == ".txt"

    def test_no_extension(self):
        name, ext = get_file_extension("README")
        assert name == "README"
        assert ext == ""

    def test_hidden_file(self):
        name, ext = get_file_extension(".gitignore")
        assert name == ".gitignore"
        assert ext == ""
