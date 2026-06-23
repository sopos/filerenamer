# File Renamer - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              FileRenamerApp (app.py)                   │ │
│  │  - Main application controller                         │ │
│  │  - Event routing and state management                  │ │
│  │  - Message passing coordination                        │ │
│  └──────────────┬─────────────────┬───────────────────────┘ │
│                 │                 │                          │
│      ┌──────────▼────────┐  ┌────▼──────────────┐           │
│      │  ControlPanel     │  │  FileListPanel    │           │
│      │  - Search input   │  │  - DataTable      │           │
│      │  - Replace input  │  │  - Selection UI   │           │
│      │  - Checkbox       │  │  - Inline editing │           │
│      │  - Buttons        │  │  - Navigation     │           │
│      └───────────────────┘  └───────────────────┘           │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Messages (PatternChanged, 
                          │           ApplyRename, etc.)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  Models (models.py)                    │ │
│  │  - FileItem: File representation                      │ │
│  │  - RenameOperation: Pattern parameters                │ │
│  │  - FileTreeNode: Directory structure                  │ │
│  │  - RenameResult: Operation results                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────┐  ┌──────────────────────────┐   │
│  │  Renamer Utils        │  │  File Scanner Utils      │   │
│  │  (renamer.py)         │  │  (file_scanner.py)       │   │
│  │                       │  │                          │   │
│  │  - validate_pattern   │  │  - scan_directory        │   │
│  │  - apply_pattern      │  │  - apply_renames         │   │
│  │  - preview_renames    │  │  - validate_renames      │   │
│  │  - get_file_extension │  │                          │   │
│  └───────────────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ File system operations
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   File System Layer                          │
│  - pathlib.Path for file operations                          │
│  - os.walk() for directory traversal                         │
│  - Path.rename() for file renaming                          │
└─────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

### 1. Application Startup
```
User launches app
    │
    ▼
FileRenamerApp.__init__()
    │
    ▼
on_mount()
    │
    ▼
scan_directory(start_path) ───► Returns List[FileItem]
    │
    ▼
FileListPanel.populate_files() ───► Display files in table
```

### 2. Pattern Input Flow
```
User types in Search field
    │
    ▼
Input.Changed event
    │
    ▼
ControlPanel.on_input_changed()
    │
    ▼
PatternChanged message posted
    │
    ▼
FileRenamerApp.on_pattern_changed()
    │
    ├─► validate_pattern() ───► Check regex validity
    │
    └─► preview_renames() ───► Update FileItem.new_name
            │
            ▼
        FileListPanel.update_preview() ───► Refresh display
```

### 3. File Selection Flow
```
User presses Space on file
    │
    ▼
FileListPanel.action_toggle_selection()
    │
    ▼
FileItem.is_selected toggled
    │
    ▼
FileSelectionChanged message posted
    │
    ▼
FileRenamerApp.on_file_selection_changed()
    │
    ▼
Update status bar counts
```

### 4. Apply Rename Flow
```
User clicks Apply button
    │
    ▼
Button.Pressed event
    │
    ▼
ControlPanel.on_button_pressed()
    │
    ▼
ApplyRename message posted
    │
    ▼
FileRenamerApp.on_apply_rename()
    │
    ├─► validate_renames() ───► Check for conflicts
    │
    ├─► apply_renames() ───► Execute file system operations
    │       │
    │       └─► Path.rename() for each file
    │
    └─► scan_directory() ───► Refresh file list
```

## Data Flow

### FileItem State Transitions
```
1. Initial Scan:
   FileItem(original_name="file.txt", new_name="file.txt", is_selected=True)

2. Pattern Applied:
   FileItem(original_name="file.txt", new_name="doc.txt", is_selected=True)

3. User Deselects:
   FileItem(original_name="file.txt", new_name="doc.txt", is_selected=False)

4. User Custom Edit:
   FileItem(original_name="file.txt", new_name="custom.txt", 
            is_selected=True, is_custom_override=True)

5. New Pattern Applied (custom preserved):
   FileItem(original_name="file.txt", new_name="custom.txt",
            is_selected=True, is_custom_override=True)
```

## Message Passing Architecture

### Messages
```python
# Control Panel → App
class PatternChanged(Message):
    operation: RenameOperation

class ApplyRename(Message):
    pass

# File List Panel → App  
class FileSelectionChanged(Message):
    files: List[FileItem]
```

### Event Flow
```
ControlPanel ──PatternChanged──► FileRenamerApp
                                      │
                                      ▼
                                 Update Preview
                                      │
                                      ▼
FileListPanel ◄─────update_preview()───┘

FileListPanel ──FileSelectionChanged──► FileRenamerApp
                                             │
                                             ▼
                                        Update Status

ControlPanel ──ApplyRename──► FileRenamerApp
                                    │
                                    ▼
                              Execute Renames
                                    │
                                    ▼
                              Rescan Directory
```

## Widget Hierarchy

```
FileRenamerApp (App)
├── Header (Textual built-in)
├── Vertical Container (#main-container)
│   ├── ControlPanel (Container)
│   │   ├── Horizontal (#search-container)
│   │   │   ├── Label ("Search:")
│   │   │   └── Input (#search-input)
│   │   ├── Horizontal (#replace-container)
│   │   │   ├── Label ("Replace:")
│   │   │   └── Input (#replace-input)
│   │   └── Horizontal (#options-container)
│   │       ├── Checkbox (#case-checkbox)
│   │       └── Horizontal (#button-container)
│   │           ├── Button ("Apply", #apply-button)
│   │           └── Button ("Exit", #exit-button)
│   └── FileListPanel (Container)
│       ├── DataTable (#file-table)
│       │   ├── Column: "Original Name"
│       │   └── Column: "New Name"
│       └── Container (#edit-container, hidden by default)
│           └── Horizontal
│               ├── Label ("Edit name:")
│               └── Input (#edit-input)
├── Label (#status-bar)
└── Footer (Textual built-in)
```

## State Management

### Application State
```python
class FileRenamerApp:
    start_path: Path              # Directory being scanned
    files: List[FileItem]         # Current file list
    current_operation: RenameOperation  # Current pattern/settings
```

### Component State
```python
class ControlPanel:
    search_pattern: str
    replace_pattern: str
    case_sensitive: bool

class FileListPanel:
    files: List[FileItem]
    row_to_index: dict[RowKey, int]
    editing_row: Optional[RowKey]
```

## Error Handling Strategy

### Layers of Protection

1. **Input Validation**
   - Regex pattern validation before applying
   - Error messages shown in status bar

2. **Pre-Rename Validation**
   - Check for duplicate target names
   - Validate file permissions
   - Detect conflicts

3. **Rename Execution**
   - Try/except around each rename operation
   - Continue on error (don't fail entire batch)
   - Collect RenameResult for each operation

4. **User Feedback**
   - Success count displayed
   - First error message shown
   - Status bar updates with results

## Performance Considerations

### Directory Scanning
- Recursive traversal with depth limit (max 10)
- Skip hidden files (starting with .)
- Graceful handling of permission errors
- Sort entries (directories first, then by name)

### Preview Updates
- Only update when pattern actually changes
- Preserve custom overrides (skip pattern application)
- Batch update the DataTable

### File Renaming
- Sort by depth (deepest first) to avoid parent/child conflicts
- Only rename selected files with changes
- Check for existing files before renaming

## Testing Strategy

### Unit Tests (tests/test_renamer.py)
- Isolated function testing
- Mock file system operations
- Test edge cases and error conditions

### Integration Tests (test_basic.py)
- End-to-end workflow verification
- Real file system operations in test directory
- Pattern application and preview generation

### Manual Testing
- Full TUI interaction
- Keyboard navigation
- Visual verification
- Cross-platform compatibility

## Dependencies

### External
- **textual** (>=0.30.0): TUI framework
  - Provides widgets, layout, event handling
  - Cross-platform terminal support
  - Reactive architecture

### Standard Library
- **pathlib**: Modern file path handling
- **re**: Regular expression operations
- **dataclasses**: Data model definitions
- **typing**: Type hints for better IDE support

## File Organization

```
src/filerenamer/
├── __init__.py           # Package metadata
├── __main__.py           # Entry point (35 lines)
├── app.py                # Main application (252 lines)
├── models.py             # Data models (64 lines)
├── widgets/
│   ├── __init__.py
│   ├── control_panel.py  # Search/replace UI (114 lines)
│   └── file_list_panel.py # File list UI (213 lines)
└── utils/
    ├── __init__.py
    ├── file_scanner.py   # Directory operations (127 lines)
    └── renamer.py        # Pattern matching (113 lines)
```

## Extension Points

### Adding New Features

**1. New Rename Pattern Types**
- Add function to `renamer.py`
- Update `RenameOperation` model
- Add UI element in `ControlPanel`

**2. New File List Features**
- Extend `FileListPanel` widget
- Add new bindings in `BINDINGS`
- Update `FileItem` model if needed

**3. New Validation Rules**
- Add function to `file_scanner.py`
- Call in `validate_renames()`
- Show errors in status bar

**4. Persistent Configuration**
- Add config file loading in `__init__.py`
- Extend `FileRenamerApp.__init__()`
- Save settings on exit

## Design Patterns Used

1. **Model-View-Controller (MVC)**
   - Models: `models.py`
   - Views: Widget classes
   - Controller: `FileRenamerApp`

2. **Observer Pattern**
   - Textual message system
   - Components post messages
   - App handles messages

3. **Factory Pattern**
   - Widget composition in `compose()`
   - Dynamic UI generation

4. **Strategy Pattern**
   - Different rename strategies (regex, plain text, case sensitive)
   - Encapsulated in `apply_pattern()`

## Security Considerations

1. **Input Validation**
   - Regex pattern compilation in try/except
   - No arbitrary code execution

2. **File System Safety**
   - Only operates on specified directory
   - Checks for existing files before renaming
   - Permission error handling

3. **Data Validation**
   - Type hints throughout
   - Dataclass validation
   - Path validation

## Future Architecture Improvements

1. **Undo/Redo**
   - Command pattern for reversible operations
   - History stack in app state
   - Inverse operations for each rename

2. **Batch Operations**
   - Queue pattern for large operations
   - Progress reporting
   - Cancellation support

3. **Plugin System**
   - Plugin interface definition
   - Dynamic plugin loading
   - Custom rename strategies

4. **Configuration**
   - TOML/JSON config file
   - User preferences persistence
   - Per-directory settings
