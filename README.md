# File Renamer

A cross-platform TUI (Terminal User Interface) file renaming tool with regex pattern matching and live preview.

## Features

- 🔍 **Regex Pattern Matching** - Use powerful regular expressions to match and transform filenames
- 🧮 **Mathematical Operations** - Apply math operations to captured numbers (e.g., `\{1+10}` to add 10)
- 📐 **Number Padding** - Zero-pad or space-pad results (e.g., `\{01+5}` for 2-digit zero-padding)
- 👀 **Live Preview** - See renamed files in real-time as you type
- ✅ **Selective Rename** - Choose which files to rename with space bar
- ✏️ **Individual Overrides** - Edit specific filenames manually with Enter
- 🎯 **Case Sensitivity** - Toggle case-sensitive matching
- 🌳 **Tree View** - Display files in a hierarchical directory structure
- ⌨️ **Keyboard Driven** - Full keyboard navigation with intuitive shortcuts

## Installation

### Using pipx (recommended)

[pipx](https://pypa.github.io/pipx/) installs the tool into an isolated environment and puts the `filerenamer` command on your PATH.

```bash
# Install directly from GitHub
pipx install git+https://github.com/sopos/filerenamer.git

# Or install from a local clone
git clone https://github.com/sopos/filerenamer.git
cd filerenamer
pipx install .
```

To upgrade later:

```bash
pipx upgrade filerenamer
```

### Using pip

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
