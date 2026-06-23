# File Renamer - Quick Start Guide

## Installation (30 seconds)

```bash
cd /Users/dapospis/claude/filerenamer
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Launch

```bash
filerenamer                    # Current directory
filerenamer /path/to/files     # Specific directory
python -m filerenamer          # Alternative launch
```

## Interface Overview

```
┌──────────────────────────────────────────────────────┐
│                    File Renamer                      │
├──────────────────────────────────────────────────────┤
│ Search: [pattern]    Replace: [replacement]          │
│ [x] Case Sensitive   [Apply] [Exit]                  │
├──────────────────────────────────────────────────────┤
│ Original Name        │ New Name                      │
│ ✓ file1.txt          │ doc1.txt                      │
│ □ file2.js           │ file2.js                      │
├──────────────────────────────────────────────────────┤
│ Files: 7 | Selected: 5 | Will rename: 3              │
└──────────────────────────────────────────────────────┘
```

## Essential Keys

| Key | Action |
|-----|--------|
| `Tab` | Move between fields |
| `Space` | Toggle selection (✓/□) |
| `Enter` | Edit filename OR activate button |
| `Ctrl+A` | Select/deselect all |
| `Ctrl+C` | Quit |

## 3 Quick Examples

### 1. Simple Replace
```
Search:  file
Replace: doc
Result:  file1.txt → doc1.txt
```

### 2. Extract Numbers
```
Search:  file(\d+)
Replace: doc\1
Result:  file123.txt → doc123.txt
```

### 3. Swap Parts
```
Search:  (\w+)_(\w+)
Replace: \2_\1
Result:  first_second.txt → second_first.txt
```

## Workflow

1. **Type search pattern** → preview updates
2. **Type replace pattern** → preview updates  
3. **Use Space** to deselect files you don't want to rename
4. **Use Enter** on a file to edit it manually (optional)
5. **Click Apply** → files renamed!

## Tips

- ✓ = Selected (will be renamed)
- □ = Not selected (will be skipped)
- Green = Name will change
- ✏ = Custom edit (won't change with pattern)

## Test It

```bash
# Create test files
mkdir test && cd test
touch file1.txt file2.js file3.py
filerenamer
# Try: Search "file" → Replace "doc"
```

## Help

- Full guide: `cat USAGE.md`
- Test checklist: `cat TESTING_CHECKLIST.md`
- Project details: `cat PROJECT_SUMMARY.md`

---

**That's it!** Start typing and watch the magic happen. 🪄
