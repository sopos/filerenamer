# Mathematical Operations in Regex Replacements

## Overview

The File Renamer now supports mathematical operations on captured regex groups using the `\{expr}` syntax.

## Syntax

```
\{N op value}
```

Where:
- `N` is the capture group number (1, 2, 3, ...)
- `op` is a mathematical operator
- `value` is a number or another expression

## Supported Operations

- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (with decimals)
- `//` Floor division (integer result)
- `%` Modulo
- `**` Exponentiation
- `()` Parentheses for grouping

## Examples

### Basic Addition
- **Search**: `S02E([0-9]+)`
- **Replace**: `S01E\{1+10}`
- **Input**: `S02E01.mkv`
- **Output**: `S01E11.mkv`

### Subtraction
- **Search**: `Chapter_([0-9]+)`  
- **Replace**: `Chapter_\{1-5}`
- **Input**: `Chapter_10.pdf`
- **Output**: `Chapter_5.pdf`

### Multiplication
- **Search**: `video_([0-9]+)`
- **Replace**: `video_\{1*2}`
- **Input**: `video_3.mp4`
- **Output**: `video_6.mp4`

### Complex Expressions
- **Search**: `Track_([0-9]+)`
- **Replace**: `Track_\{1*2+5}`
- **Input**: `Track_3.mp3`
- **Output**: `Track_11.mp3`

### Multiple Capture Groups
- **Search**: `S([0-9]+)E([0-9]+)`
- **Replace**: `S\{1-1}E\{2+10}`
- **Input**: `S02E05.avi`
- **Output**: `S1E15.avi`

### Keeping Some Groups Unchanged
- **Search**: `Track_([0-9]+)_of_([0-9]+)`
- **Replace**: `Track_\{1+5}_of_\{2+0}`
- **Input**: `Track_10_of_20.mp3`
- **Output**: `Track_15_of_20.mp3`

## How It Works

1. The `\{...}` syntax indicates a mathematical expression
2. Single digits (1-9) at the start of tokens are treated as capture group references
3. Each capture group is substituted only once (first occurrence)
4. The expression is evaluated using Python's `eval()` in a safe context
5. Integer results are formatted without decimals (e.g., `10.0` becomes `10`)

## Mixing with Standard Backreferences

You can mix mathematical operations with standard `\1`, `\2` backreferences:

- **Search**: `S([0-9]+)E([0-9]+)_(\w+)`
- **Replace**: `S\{1-1}E\{2+10}_\3`
- **Input**: `S02E05_title.avi`
- **Output**: `S1E15_title.avi`

Here, `\{1-1}` and `\{2+10}` use math operations, while `\3` is a standard backreference.

## Edge Cases

- **Division by zero**: Returns the original expression unchanged
- **Non-numeric captures**: Returns the original expression unchanged  
- **Float results**: Preserved (e.g., `7/2` = `3.5`)
- **Negative results**: Supported (e.g., `5-10` = `-5`)
- **Parentheses**: Supported for complex expressions (e.g., `(1+5)*2`)

## Testing

Run the test suite:
```bash
python3 test_math_operations.py
python3 test_edge_cases.py
```

Run the demo:
```bash
python3 demo_math_operations.py
```
