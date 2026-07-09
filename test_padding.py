"""Test padding in mathematical operations."""

from src.filerenamer.utils.renamer import apply_pattern


def test_zero_padding_2_digits():
    """Test zero-padding to 2 digits with \{01+10}"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{01+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E11", f"Expected 'S01E11', got '{result}'"


def test_zero_padding_2_digits_single_result():
    """Test zero-padding to 2 digits with single digit result"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{01+4}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E05", f"Expected 'S01E05', got '{result}'"


def test_zero_padding_3_digits():
    """Test zero-padding to 3 digits with \{001+10}"""
    result = apply_pattern(
        filename="Episode_5",
        search=r'Episode_([0-9]+)',
        replace=r'Episode_\{001+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Episode_015", f"Expected 'Episode_015', got '{result}'"


def test_zero_padding_4_digits():
    """Test zero-padding to 4 digits"""
    result = apply_pattern(
        filename="Track_3",
        search=r'Track_([0-9]+)',
        replace=r'Track_\{0001*2}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Track_0006", f"Expected 'Track_0006', got '{result}'"


def test_space_padding_2_digits():
    """Test space-padding to 2 digits with \{ 1+10}"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{ 1+4}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E 5", f"Expected 'S01E 5', got '{result}'"


def test_space_padding_3_digits():
    """Test space-padding to 3 digits"""
    result = apply_pattern(
        filename="Episode_5",
        search=r'Episode_([0-9]+)',
        replace=r'Episode_\{  1+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Episode_ 15", f"Expected 'Episode_ 15', got '{result}'"


def test_padding_with_subtraction():
    """Test padding works with subtraction"""
    result = apply_pattern(
        filename="Chapter_20",
        search=r'Chapter_([0-9]+)',
        replace=r'Chapter_\{01-15}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Chapter_05", f"Expected 'Chapter_05', got '{result}'"


def test_padding_overflow():
    """Test when result is wider than padding"""
    result = apply_pattern(
        filename="S02E99",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{01+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E109", f"Expected 'S01E109', got '{result}'"


def test_padding_with_complex_expression():
    """Test padding with complex math expression"""
    result = apply_pattern(
        filename="video_3.mp4",
        search=r'video_([0-9]+)\.mp4',
        replace=r'video_\{001*2+5}.mp4',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "video_011.mp4", f"Expected 'video_011.mp4', got '{result}'"


def test_no_padding():
    """Test that expressions without padding still work"""
    result = apply_pattern(
        filename="S02E05",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{1+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E15", f"Expected 'S01E15', got '{result}'"


def test_multiple_groups_with_padding():
    """Test multiple capture groups with different padding"""
    result = apply_pattern(
        filename="S2E5",
        search=r'S([0-9]+)E([0-9]+)',
        replace=r'S\{01-1}E\{02+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E15", f"Expected 'S01E15', got '{result}'"


if __name__ == "__main__":
    # Run all tests
    tests = [
        (test_zero_padding_2_digits, "Zero padding to 2 digits (11)"),
        (test_zero_padding_2_digits_single_result, "Zero padding to 2 digits (05)"),
        (test_zero_padding_3_digits, "Zero padding to 3 digits"),
        (test_zero_padding_4_digits, "Zero padding to 4 digits"),
        (test_space_padding_2_digits, "Space padding to 2 digits"),
        (test_space_padding_3_digits, "Space padding to 3 digits"),
        (test_padding_with_subtraction, "Padding with subtraction"),
        (test_padding_overflow, "Padding overflow (result wider than padding)"),
        (test_padding_with_complex_expression, "Padding with complex expression"),
        (test_no_padding, "No padding (backward compatibility)"),
        (test_multiple_groups_with_padding, "Multiple groups with padding"),
    ]

    for test_func, desc in tests:
        try:
            test_func()
            print(f"✓ {desc}")
        except AssertionError as e:
            print(f"✗ {desc}")
            print(f"  {e}")

    print("\n✅ All padding tests passed!")
