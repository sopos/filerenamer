# File Renamer

A cross-platform TUI (Terminal User Interface) file renaming tool with regex pattern matching and live preview.

## Features

- 🔍 **Regex Pattern Matching** - Use powerful regular expressions to match and transform filenames
- 🧮 **Mathematical Operations** - Apply math operations to captured numbers (e.g., `\{1+10}` to add 10)
- 👀 **Live Preview** - See renamed files in real-time as you type
- ✅ **Selective Rename** - Choose which files to rename with space bar
- ✏️ **Individual Overrides** - Edit specific filenames manually with Enter
- 🎯 **Case Sensitivity** - Toggle case-sensitive matching
- 🌳 **Tree View** - Display files in a hierarchical directory structure
- ⌨️ **Keyboard Driven** - Full keyboard navigation with intuitive shortcuts

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Run in current directory
filerenamer

# Or run as Python module
python -m filerenamer
```

## Keyboard Shortcuts

### Navigation
- `Tab` - Switch between control panel and file list
- `↑/↓` - Navigate file list
- `PgUp/PgDn` - Jump by page
- `Home/End` - Jump to first/last file

### File Operations
- `Space` - Toggle file selection
- `Enter` - Edit individual filename
- `Ctrl+A` - Select/deselect all files

### Actions
- `Apply button` or focus and press Enter - Rename selected files
- `Exit button` or `Ctrl+C` - Quit application

## License

MIT
