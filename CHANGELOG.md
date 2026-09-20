# Changelog

All notable changes to the File Renamer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-09-20

### Fixed
- **Whole Path checkbox had no effect** - `ControlPanel._emit_pattern_changed()` (fired on every keystroke/checkbox toggle) built its `RenameOperation` without passing `whole_path`, so live typing always matched against the filename only regardless of the checkbox state

## [0.4.0] - 2026-09-20

### Added
- **Whole Path Processing** - New "Whole Path" checkbox (enabled by default) lets search/replace patterns match against a file's path relative to the scanned root instead of just its filename
  - Enables patterns that collapse directory structure into the filename, e.g. `S(\d+)/(\d+)\.txt` → `S\1E\2.txt` transforms `S01/01.txt` into `S01E01.txt`
  - Renaming can move files across directories, creating destination directories as needed

### Technical
- `FileItem` now tracks `relative_path`, `root_path`, and `is_whole_path` to resolve rename targets relative to the scan root
- `validate_renames()` now detects duplicate conflicts by resolved target path instead of assuming same-directory renames

## [0.1.0] - 2026-06-04

### Initial Release

#### Added
- Two-panel TUI layout with control panel and file list
- Regex pattern matching with full capture group support
- Plain text search and replace mode
- Case-sensitive and case-insensitive matching
- Live preview of rename operations
- File selection/deselection with visual indicators (✓/□)
- Individual filename editing with custom override capability
- Directory tree scanning with depth tracking
- Keyboard navigation:
  - Tab/Shift+Tab for focus navigation
  - Space for selection toggle
  - Enter for inline editing
  - Ctrl+A for select/deselect all
  - Ctrl+C/Ctrl+Q for quit
- Status bar with file counts (total, selected, will rename)
- Error and success message display
- Validation for duplicate names and conflicts
- Permission error handling
- Unit tests for core functionality (16 tests)
- Comprehensive documentation:
  - README.md for basic usage
  - USAGE.md for detailed guide
  - QUICK_START.md for quick reference
  - TESTING_CHECKLIST.md for testing
  - PROJECT_SUMMARY.md for overview
  - ARCHITECTURE.md for technical details

#### Technical Details
- Built with Textual 0.30.0+
- Python 3.8+ compatibility
- Cross-platform support (macOS, Linux, Windows)
- Message-based reactive architecture
- DataTable widget for file list display
- Real-time preview updates
- Custom override preservation across pattern changes

#### File Structure
- `src/filerenamer/` - Main package
  - `app.py` - Main application (252 lines)
  - `models.py` - Data models (64 lines)
  - `widgets/control_panel.py` - Control panel UI (114 lines)
  - `widgets/file_list_panel.py` - File list UI (213 lines)
  - `utils/file_scanner.py` - Directory operations (127 lines)
  - `utils/renamer.py` - Pattern matching (113 lines)
- `tests/` - Unit tests (16 tests, all passing)
- Documentation files (5 comprehensive guides)

### Known Limitations
- Directory renaming not supported (files only)
- Hidden files (starting with .) are excluded
- No undo functionality
- Requires manual testing for full TUI interaction

### Dependencies
- textual >= 0.30.0

## [0.2.0] - 2026-06-23

### Added
- **Mathematical Operations on Capture Groups** - Apply arithmetic to captured numbers using `\{expr}` syntax
  - Syntax: `\{N+expr}` where N is the capture group number
  - Supported operators: `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulo), `**` (exponent)
  - Example: `S02E([0-9]+)` with replace `S01E\{1+10}` transforms `S02E01` → `S01E11`
  - Multiple capture groups: `S\{1-1}E\{2+10}` for complex transformations
  - Complex expressions: `\{1*2+5}`, `\{(1+10)/2}` with parentheses support
  - Smart substitution: Only first occurrence of each group number is replaced
  - Safe evaluation: Expressions evaluated in restricted context
  - Graceful error handling: Division by zero, non-numeric captures handled safely

### Technical
- New `_evaluate_math_expression()` function for expression parsing and evaluation
- New `_process_replacement()` function for handling `\{expr}` patterns
- Token-based substitution algorithm prevents incorrect literal replacement
- Comprehensive test suite:
  - `test_math_operations.py` - 8 tests covering basic operations
  - `test_edge_cases.py` - 11 tests for edge cases and error handling
  - `demo_math_operations.py` - Interactive demonstration script
  - `MATH_OPERATIONS.md` - Complete feature documentation

### Updated
- `USAGE.md` - Added mathematical operations section with examples
- `README.md` - Added math operations to feature list

## [0.3.0] - 2026-07-10

### Added
- **Number Padding in Mathematical Operations** - Pad results with zeros or spaces
  - Zero-padding: `\{01+10}` pads to 2 digits, `\{001+10}` pads to 3 digits, etc.
  - Space-padding: `\{ 1+10}` pads with spaces to 2 digits, `\{  1+10}` pads to 3 digits
  - Example: `Episode_([0-9]+)` with `Episode_\{01+5}` transforms `Episode_3` → `Episode_08`
  - Works with all mathematical operations: addition, subtraction, multiplication, etc.
  - Overflow handling: Result wider than padding width displays full number
  - Multiple groups: Each group can have its own padding specification
  - Negative numbers: Padding applied after the minus sign (e.g., `-05`)

### Technical
- Enhanced `_evaluate_math_expression()` to detect and apply padding specifications
- Padding detection via regex pattern matching for leading zeros or spaces
- Comprehensive test suite:
  - `test_padding.py` - 11 tests covering all padding scenarios
  - `demo_padding.py` - Interactive demonstration script
  - All existing tests continue to pass (backward compatibility maintained)

### Updated
- `MATH_OPERATIONS.md` - Added complete padding documentation with examples
- `USAGE.md` - Added number padding section with use cases
- `README.md` - Added padding to feature list

## [Unreleased]

### Planned Features
- Undo/redo functionality
- Pattern templates and presets
- EXIF/metadata-based renaming
- Directory renaming support
- Export/import rename patterns
- Batch operation history
- Configuration file support
- Color themes
- Performance optimizations for large directories

---

[0.1.0]: https://github.com/yourusername/filerenamer/releases/tag/v0.1.0
