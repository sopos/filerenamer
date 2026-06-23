# Testing Checklist

## Installation & Setup
- [x] Package structure created
- [x] Dependencies defined in pyproject.toml
- [x] Virtual environment created
- [x] Package installed successfully
- [x] Entry point configured

## Core Functionality

### Data Models
- [x] FileItem model with all required fields
- [x] RenameOperation model
- [x] FileTreeNode for directory structure
- [x] RenameResult for operation results

### File Scanner
- [x] scan_directory() recursively scans directories
- [x] Handles file depth tracking
- [x] Skips hidden files (starting with .)
- [x] Handles permission errors gracefully
- [x] apply_renames() applies changes to selected files
- [x] validate_renames() checks for conflicts

### Rename Logic
- [x] validate_pattern() checks regex validity
- [x] apply_pattern() with plain text replacement
- [x] apply_pattern() with regex replacement
- [x] apply_pattern() with case sensitivity
- [x] apply_pattern() with capture groups
- [x] preview_renames() updates all file items
- [x] Custom overrides are preserved

## UI Components

### Control Panel Widget
- [x] Search input field
- [x] Replace input field
- [x] Case sensitivity checkbox
- [x] Apply button
- [x] Exit button
- [x] PatternChanged message emission
- [x] ApplyRename message emission

### File List Panel Widget
- [x] DataTable with two columns
- [x] Original name column with selection indicator
- [x] New name column with change highlighting
- [x] populate_files() loads file list
- [x] update_preview() refreshes display
- [x] Selection indicators (✓ and □)
- [x] Directory indentation
- [x] Changed file highlighting (green)
- [x] Custom override indicator (✏)

### Main Application
- [x] App initialization with start path
- [x] Header and footer
- [x] Component composition
- [x] Directory scanning on mount
- [x] Pattern change handling
- [x] File selection change handling
- [x] Apply rename action
- [x] Status bar updates
- [x] Error message display
- [x] Success message display

## Keyboard Navigation

### Global Bindings
- [x] Tab - focus next element
- [x] Shift+Tab - focus previous element
- [x] Ctrl+C / Ctrl+Q - quit application

### File List Bindings
- [x] Space - toggle selection
- [x] Enter - edit individual filename
- [x] Ctrl+A - toggle all selections
- [ ] Up/Down - navigate files (Textual DataTable built-in)
- [ ] PgUp/PgDn - page navigation (Textual DataTable built-in)
- [ ] Home/End - jump to first/last (Textual DataTable built-in)

### Control Panel Bindings
- [ ] Tab/Shift+Tab between fields (Textual built-in)
- [ ] Enter to activate buttons (Textual built-in)

## Features

### Pattern Matching
- [x] Plain text search and replace
- [x] Regex pattern support
- [x] Capture group replacement
- [x] Case-sensitive matching
- [x] Case-insensitive matching
- [x] Live preview updates

### File Operations
- [x] Select/deselect individual files
- [x] Select/deselect all files
- [x] Edit individual filenames (custom override)
- [x] Preview changes before applying
- [x] Apply renames to selected files only
- [x] Validate before renaming

### Display Features
- [x] Directory tree structure with indentation
- [x] Selection indicators
- [x] Change highlighting
- [x] Custom override markers
- [x] Status bar with file counts
- [x] Error messages
- [x] Success messages

## Error Handling

### Pattern Errors
- [x] Invalid regex pattern detection
- [x] Display regex error message

### File Operation Errors
- [x] Permission denied
- [x] File already exists
- [x] Duplicate target names
- [x] File locked/in use
- [x] OS-level errors

## Edge Cases
- [x] Empty directory handling
- [x] Files with spaces in names
- [x] Files with special characters
- [x] Nested directories
- [x] Files without extensions
- [x] Hidden files excluded
- [x] Custom override preservation

## Unit Tests
- [x] validate_pattern() tests
- [x] apply_pattern() tests
- [x] Case sensitivity tests
- [x] Regex capture group tests
- [x] preview_renames() tests
- [x] Custom override tests
- [x] get_file_extension() tests
- [x] All 16 tests passing

## Integration Tests
- [x] Basic file scanning
- [x] Pattern application
- [x] Preview generation
- [ ] Full TUI interaction (manual testing required)
- [ ] Actual file renaming (manual testing required)

## Manual Testing Scenarios

### Scenario 1: Simple Text Replacement
1. Launch app in test_files directory
2. Enter "file" in search
3. Enter "doc" in replace
4. Verify preview shows: file1.txt → doc1.txt, etc.
5. Click Apply
6. Verify files are renamed

### Scenario 2: Regex with Capture Groups
1. Enter `file(\d+)` in search
2. Enter `document_\1` in replace
3. Verify preview shows: file1.txt → document_1.txt
4. Test without applying

### Scenario 3: Selective Rename
1. Use Space to deselect file2.js
2. Verify it shows □ instead of ✓
3. Apply rename
4. Verify file2.js was NOT renamed

### Scenario 4: Custom Override
1. Navigate to file3.py
2. Press Enter
3. Type "custom_name.py"
4. Press Enter
5. Change search pattern
6. Verify file3.py keeps "custom_name.py"

### Scenario 5: Case Sensitivity
1. Create files: File.txt, file.txt, FILE.txt
2. Search: "file"
3. Case sensitive ON: only matches "file.txt"
4. Case sensitive OFF: matches all three

## Documentation
- [x] README.md with installation and basic usage
- [x] USAGE.md with detailed guide
- [x] Keyboard shortcuts documented
- [x] Pattern examples provided
- [x] Troubleshooting section
- [x] Safety features explained

## Performance
- [ ] Test with 100+ files
- [ ] Test with deep directory nesting (10+ levels)
- [ ] Test with long filenames
- [ ] Memory usage with large directories
- [ ] UI responsiveness during scanning

## Cross-Platform
- [x] macOS (development platform)
- [ ] Linux (manual testing required)
- [ ] Windows (manual testing required)

## Future Enhancements (Out of Scope)
- [ ] Undo functionality
- [ ] Pattern templates/presets
- [ ] EXIF/metadata-based renaming
- [ ] Export/import patterns
- [ ] Batch operation history
- [ ] Directory renaming support
- [ ] Drag-and-drop file selection
- [ ] Color themes
- [ ] Configuration file support
