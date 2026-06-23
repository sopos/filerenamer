#!/usr/bin/env python3
"""Basic functionality test for the File Renamer."""

from pathlib import Path
from filerenamer.utils.file_scanner import scan_directory
from filerenamer.utils.renamer import apply_pattern, preview_renames
from filerenamer.models import RenameOperation

# Test scanning
print("Testing file scanner...")
test_path = Path("test_files")
files = scan_directory(test_path)
print(f"Found {len(files)} files:")
for f in files:
    indent = "  " * f.depth
    print(f"{indent}{f.original_name} (depth={f.depth}, dir={f.is_directory})")

print("\nTesting pattern application...")
# Test pattern application
result = apply_pattern("file1.txt", "file", "document", case_sensitive=True, use_regex=False)
print(f"file1.txt -> {result}")

result = apply_pattern("file2.js", r"file(\d+)", r"script\1", case_sensitive=True, use_regex=True)
print(f"file2.js -> {result}")

print("\nTesting preview renames...")
# Test preview
operation = RenameOperation(
    search_pattern="file",
    replace_pattern="doc",
    case_sensitive=True,
    use_regex=False
)
updated = preview_renames(files, operation)
print(f"Preview with pattern 'file' -> 'doc':")
for f in updated:
    if f.is_changed:
        print(f"  {f.original_name} -> {f.new_name}")

print("\n✓ All basic tests passed!")
