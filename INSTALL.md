# Installation Guide

## Install from Source

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Option 1: Install in Development Mode (Recommended for Development)

```bash
# Clone or navigate to the repository
cd filerenamer

# Install in editable mode
pip install -e .
```

This allows you to make changes to the code and see them reflected immediately.

### Option 2: Install from Wheel (Recommended for Users)

```bash
# Install from the built wheel file
pip install dist/filerenamer-0.2.0-py3-none-any.whl
```

### Option 3: Install from Source Distribution

```bash
# Install from the source tarball
pip install dist/filerenamer-0.2.0.tar.gz
```

## Building from Source

If you want to build the package yourself:

```bash
# Install build tool
pip install build

# Build the package
python -m build
```

This creates both:
- `dist/filerenamer-0.2.0-py3-none-any.whl` (wheel)
- `dist/filerenamer-0.2.0.tar.gz` (source distribution)

## Verify Installation

After installation, verify it works:

```bash
# Check version
pip show filerenamer

# Run the application
filerenamer

# Or run as module
python -m filerenamer
```

## Test Math Operations Feature

Quick test to verify the new math operations feature:

```bash
python -c "from filerenamer.utils.renamer import apply_pattern; \
result = apply_pattern('S02E01', r'S02E([0-9]+)', r'S01E\{1+10}'); \
print(f'Result: {result}'); \
assert result == 'S01E11', 'Failed!'"
```

Expected output: `Result: S01E11`

## Upgrading

To upgrade from version 0.1.0 to 0.2.0:

```bash
# Uninstall old version
pip uninstall filerenamer

# Install new version
pip install dist/filerenamer-0.2.0-py3-none-any.whl
```

## Dependencies

The package will automatically install required dependencies:
- `textual >= 0.30.0` - Terminal UI framework

## Platform Support

File Renamer works on:
- macOS
- Linux
- Windows

## Troubleshooting

### Command not found: filerenamer

Make sure pip's script directory is in your PATH:
- Linux/macOS: Usually `~/.local/bin` or venv's `bin/`
- Windows: Usually `%APPDATA%\Python\Scripts`

### ModuleNotFoundError

If you get import errors, try reinstalling:
```bash
pip uninstall filerenamer
pip install --force-reinstall dist/filerenamer-0.2.0-py3-none-any.whl
```

### Permission Errors

On some systems you may need to use `--user` flag:
```bash
pip install --user dist/filerenamer-0.2.0-py3-none-any.whl
```

## Uninstallation

To remove File Renamer:

```bash
pip uninstall filerenamer
```

## What's New in v0.2.0

- **Mathematical Operations**: Apply math to captured regex groups
  - Syntax: `\{N+expr}` 
  - Example: `S02E01` → `S01E11` using `\{1+10}`
  - Supports: `+`, `-`, `*`, `/`, `//`, `%`, `**`
  - See `MATH_OPERATIONS.md` for details
