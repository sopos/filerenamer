"""Regex pattern matching and rename logic."""

import re
from typing import List, Optional, Tuple, Match

from ..models import FileItem, RenameOperation


def _evaluate_math_expression(expr: str, match_groups: tuple) -> str:
    """
    Evaluate a mathematical expression with capture group references.

    Args:
        expr: Expression like "1+10" or "2*2-1" where leading numbers are group refs
              Can include padding: "01+10" (zero-pad to 2), " 1+10" (space-pad to 2)
        match_groups: Tuple of captured groups from regex match

    Returns:
        Result of the expression as a string, with optional padding
    """
    # Check for padding specification at the start of the expression
    # Format: 0N, 00N, 000N for zero-padding or space + N for space-padding
    padding_width = 0
    padding_char = ''

    # Check for zero-padding (e.g., "01", "001")
    zero_pad_match = re.match(r'^(0+)(\d)', expr)
    if zero_pad_match:
        padding_char = '0'
        padding_width = len(zero_pad_match.group(1)) + 1  # +1 for the digit itself
    else:
        # Check for space-padding (e.g., " 1", "  1")
        space_pad_match = re.match(r'^( +)(\d)', expr)
        if space_pad_match:
            padding_char = ' '
            padding_width = len(space_pad_match.group(1)) + 1  # +1 for the digit itself

    # Strategy: Replace group references that appear as operands (not part of literals)
    # We'll parse tokens and replace only bare number tokens that match group indices

    # Tokenize the expression (numbers, operators, parens, spaces)
    tokens = re.findall(r'\d+\.?\d*|[+\-*/%()]| +', expr)

    # Track which group numbers we've already substituted
    substituted = set()

    # Replace tokens that are group references (process in order)
    result_tokens = []
    for token in tokens:
        # Skip space tokens in tokenization (they were only for padding detection)
        if token.strip() == '':
            continue

        if token.isdigit() and 1 <= int(token) <= len(match_groups) and int(token) not in substituted:
            # This looks like a group reference (groups are 1-indexed)
            group_idx = int(token)
            group_val = match_groups[group_idx - 1]
            if group_val is not None:
                try:
                    num_val = int(group_val) if group_val.isdigit() else float(group_val)
                    result_tokens.append(str(num_val))
                    substituted.add(group_idx)
                except ValueError:
                    # Not a number, keep as string (will fail eval later)
                    result_tokens.append(group_val)
                    substituted.add(group_idx)
            else:
                result_tokens.append(token)
        else:
            result_tokens.append(token)

    final_expr = ''.join(result_tokens)

    # Evaluate the expression
    try:
        result = eval(final_expr, {"__builtins__": {}}, {})
        # Format result - remove decimal if it's a whole number
        if isinstance(result, float) and result.is_integer():
            result_str = str(int(result))
        else:
            result_str = str(result)

        # Apply padding if specified
        if padding_width > 0 and padding_char:
            # Handle negative numbers specially
            if result_str.startswith('-'):
                # Pad after the minus sign
                result_str = '-' + result_str[1:].rjust(padding_width - 1, padding_char)
            else:
                result_str = result_str.rjust(padding_width, padding_char)

        return result_str
    except Exception:
        # If evaluation fails, return the expression as-is
        return expr


def _process_replacement(replacement: str, match_obj: Match) -> str:
    """
    Process replacement string, handling \\{expr} for math operations.

    Args:
        replacement: Replacement pattern with optional \\{expr} blocks
        match_obj: The regex match object

    Returns:
        Processed replacement string
    """
    def replace_math_expr(m):
        expr = m.group(1)
        return _evaluate_math_expression(expr, match_obj.groups())

    # Find all \{expr} patterns and replace them with evaluated results
    # Look for escaped brace: \{...}
    result = re.sub(r'\\{([^}]+)}', replace_math_expr, replacement)

    # Now handle standard backreferences (\1, \2, etc.) that weren't in \{...}
    result = match_obj.expand(result)

    return result


def validate_pattern(pattern: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a regex pattern is valid.

    Args:
        pattern: The regex pattern to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pattern:
        return True, None

    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, str(e)


def apply_pattern(
    filename: str,
    search: str,
    replace: str,
    case_sensitive: bool = True,
    use_regex: bool = True
) -> str:
    """
    Apply a search/replace pattern to a filename.

    Supports mathematical operations in replacement patterns using \\{expr} syntax.
    Example: search='S02E([0-9]+)', replace='S01E\\{1+10}' transforms 'S02E01' to 'S01E11'

    Args:
        filename: The original filename
        search: The search pattern
        replace: The replacement pattern (supports \\{expr} for math operations)
        case_sensitive: Whether to use case-sensitive matching
        use_regex: Whether to treat search as a regex pattern

    Returns:
        The transformed filename
    """
    if not search:
        return filename

    try:
        if use_regex:
            # Use regex replacement with support for \{expr} math operations
            flags = 0 if case_sensitive else re.IGNORECASE
            pattern = re.compile(search, flags)

            # Check if replacement contains \{expr} patterns
            if '\\{' in replace and '}' in replace:
                # Use custom replacement function for math expressions
                return pattern.sub(lambda m: _process_replacement(replace, m), filename)
            else:
                # Standard regex replacement
                return pattern.sub(replace, filename)
        else:
            # Use plain text replacement
            if case_sensitive:
                return filename.replace(search, replace)
            else:
                # Case-insensitive plain text replacement
                pattern = re.compile(re.escape(search), re.IGNORECASE)
                return pattern.sub(replace, filename)
    except re.error:
        # If regex is invalid, return original filename
        return filename
    except Exception:
        return filename


def preview_renames(
    files: List[FileItem],
    operation: RenameOperation
) -> List[FileItem]:
    """
    Apply the rename operation to all files and update their new_name field.

    Args:
        files: List of FileItem objects
        operation: The RenameOperation to apply

    Returns:
        Updated list of FileItem objects with new_name populated
    """
    updated_files = []

    for file_item in files:
        # Skip if this file has a custom override
        if file_item.is_custom_override:
            updated_files.append(file_item)
            continue

        # When whole-path mode is enabled, match/replace against the file's
        # path relative to the scan root (e.g. "S01/01.txt") instead of just
        # its name, so patterns can collapse directories into the filename
        # (e.g. "S01/01.txt" -> "S01E01.txt").
        if operation.whole_path and file_item.relative_path is not None:
            source = file_item.relative_path.as_posix()
        else:
            source = file_item.original_name

        # Apply the pattern to get the new name
        new_name = apply_pattern(
            source,
            operation.search_pattern,
            operation.replace_pattern,
            operation.case_sensitive,
            operation.use_regex
        )

        # Create updated FileItem
        updated_item = FileItem(
            original_path=file_item.original_path,
            original_name=file_item.original_name,
            new_name=new_name,
            is_selected=file_item.is_selected,
            is_custom_override=file_item.is_custom_override,
            is_directory=file_item.is_directory,
            depth=file_item.depth,
            parent_path=file_item.parent_path,
            relative_path=file_item.relative_path,
            root_path=file_item.root_path,
            is_whole_path=operation.whole_path
        )
        updated_files.append(updated_item)

    return updated_files


def get_file_extension(filename: str) -> Tuple[str, str]:
    """
    Split a filename into name and extension.

    Args:
        filename: The filename to split

    Returns:
        Tuple of (name, extension)
    """
    if '.' not in filename or filename.startswith('.'):
        return filename, ''

    parts = filename.rsplit('.', 1)
    return parts[0], '.' + parts[1]
