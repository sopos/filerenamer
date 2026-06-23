# File Renamer - Usage Guide

## Installation

From the project directory:

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Running the Application

```bash
# Run in the current directory
filerenamer

# Or specify a directory
filerenamer /path/to/directory

# Or run as a module
python -m filerenamer
```

## User Interface

The application has a two-panel layout:

```
┌─────────────────────────────────────────────────────────────┐
│ File Renamer                                                │
├─────────────────────────────────────────────────────────────┤
│ Search: [____________] Replace: [___________]               │
│ [x] Case Sensitive    [Apply] [Exit]                        │
├─────────────────────────────────────────────────────────────┤
│ Original Name           │ New Name                          │
├─────────────────────────┼───────────────────────────────────┤
│ ✓ file1.txt             │ doc1.txt                          │
│ ✓ file2.js              │ doc2.js                           │
│ □ file3.py              │ file3.py                          │
│ ✓ subfolder/                                                │
│   ✓ nested1.txt         │ nested1.txt                       │
├─────────────────────────────────────────────────────────────┤
│ Files: 5 | Selected: 4 | Will rename: 2                     │
├─────────────────────────────────────────────────────────────┤
│ space: Toggle Selection │ enter: Edit Name │ ctrl+q: Quit   │
└─────────────────────────────────────────────────────────────┘
```

## Keyboard Shortcuts

### Navigation
- **Tab** - Move between search input, replace input, checkbox, buttons, and file list
- **Shift+Tab** - Move backwards
- **↑/↓** - Navigate up/down in the file list
- **PgUp/PgDn** - Jump by page in the file list
- **Home/End** - Jump to first/last file

### File Operations
- **Space** - Toggle selection for the current file (selected files shown with ✓)
- **Enter** - Edit the new name for the current file (custom override)
- **Esc** - Cancel editing
- **Ctrl+A** - Select/deselect all files

### Actions
- **Apply button** (or focus and press Enter) - Rename all selected files with changes
- **Exit button** (or Ctrl+C, Ctrl+Q) - Quit the application

## Pattern Matching

### Plain Text Replacement
Simply type text in the Search and Replace fields:
- Search: `file`
- Replace: `document`
- Result: `file1.txt` → `document1.txt`

### Regex Patterns
The tool supports full regex patterns with capture groups:

**Example 1: Extract numbers**
- Search: `file(\d+)`
- Replace: `doc\1`
- Result: `file123.txt` → `doc123.txt`

**Example 2: Swap parts**
- Search: `(\w+)_(\w+)`
- Replace: `\2_\1`
- Result: `test_file.txt` → `file_test.txt`

**Example 3: Date formatting**
- Search: `(\d{4})-(\d{2})-(\d{2})`
- Replace: `\1\2\3`
- Result: `2024-06-04-report.pdf` → `20240604-report.pdf`

### Mathematical Operations on Capture Groups
You can perform mathematical operations on captured numbers using `\{N+expr}` syntax:

**Example 1: Add to episode numbers**
- Search: `S02E([0-9]+)`
- Replace: `S01E\{1+10}`
- Result: `S02E01.mkv` → `S01E11.mkv`

**Example 2: Subtract from numbers**
- Search: `Chapter_([0-9]+)`
- Replace: `Chapter_\{1-5}`
- Result: `Chapter_10.pdf` → `Chapter_5.pdf`

**Example 3: Multiply numbers**
- Search: `video_([0-9]+)`
- Replace: `video_\{1*2}`
- Result: `video_3.mp4` → `video_6.mp4`

**Example 4: Complex expressions**
- Search: `Track_([0-9]+)`
- Replace: `Track_\{1*2+5}`
- Result: `Track_3.mp3` → `Track_11.mp3`

**Example 5: Multiple capture groups**
- Search: `S([0-9]+)E([0-9]+)`
- Replace: `S\{1-1}E\{2+10}`
- Result: `S02E05.avi` → `S1E15.avi`

**Supported operations**: `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulo), `**` (exponent)

### Case Sensitivity
- ✓ **Checked**: `file` will only match `file`, not `File` or `FILE`
- □ **Unchecked**: `file` will match `file`, `File`, `FILE`, etc.

## Workflow

1. **Start the application** in your target directory
2. **Review the file list** - all files are selected by default
3. **Enter search pattern** - watch the preview update in real-time
4. **Enter replace pattern** - see the new names immediately
5. **Adjust selections**:
   - Use Space to deselect files you don't want to rename
   - Use Enter to manually edit specific filenames
6. **Verify the changes** - check the "New Name" column
7. **Click Apply** (or navigate to it and press Enter) to execute the renames
8. **Check the status bar** for success/error messages

## Tips

- **Live Preview**: The "New Name" column updates in real-time as you type
- **Custom Overrides**: Files edited with Enter (shown with ✏) won't be affected by pattern changes
- **Selection**: Only selected files (✓) will be renamed
- **Changed Files**: Green highlighting shows files that will be renamed
- **Validation**: The app checks for duplicate names and permission errors before renaming
- **Directories**: Currently, subdirectories are shown but not renamed (files only)

## Examples

### Example 1: Remove prefix
Files: `IMG_001.jpg`, `IMG_002.jpg`, `IMG_003.jpg`

- Search: `IMG_`
- Replace: `` (empty)
- Result: `001.jpg`, `002.jpg`, `003.jpg`

### Example 2: Add suffix before extension
Files: `report.pdf`, `data.csv`

- Search: `(.+)\.(.+)`
- Replace: `\1_final.\2`
- Result: `report_final.pdf`, `data_final.csv`

### Example 3: Change case and spacing
Files: `My Document.txt`, `Another File.doc`

- Search: ` `
- Replace: `_`
- Uncheck "Case Sensitive"
- Result: `My_Document.txt`, `Another_File.doc`

## Troubleshooting

**Pattern not matching?**
- Check if "Case Sensitive" should be toggled
- Verify your regex syntax (the status bar will show errors)
- Remember to escape special regex characters: `. * + ? [ ] ( ) { } | \`

**Can't rename a file?**
- Check file permissions
- Make sure the file isn't open in another program
- Ensure the new name doesn't conflict with an existing file

**Application won't start?**
- Make sure Textual is installed: `pip install textual`
- Check Python version: requires Python 3.8+
- Try running with: `python -m filerenamer`

## Safety Features

- **Preview before rename**: See exactly what will change before applying
- **Selective rename**: Choose which files to rename
- **Duplicate detection**: Warns if renames would create duplicate names
- **Error handling**: Shows detailed error messages for permission issues
- **Validation**: Checks regex patterns and shows errors immediately

## Limitations

- Directory renaming is not currently supported (only files)
- No undo functionality (use with caution!)
- Hidden files (starting with `.`) are excluded from listing

## Support

For issues and feature requests, visit:
https://github.com/yourusername/filerenamer/issues
