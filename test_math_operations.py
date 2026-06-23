"""Test mathematical operations in replacement patterns."""

from src.filerenamer.utils.renamer import apply_pattern


def test_basic_math_addition():
    """Test S02E01 -> S01E11 with \1+10"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{1+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E11", f"Expected 'S01E11', got '{result}'"


def test_math_subtraction():
    """Test S05E20 -> S04E10 with \1-10"""
    result = apply_pattern(
        filename="S05E20",
        search=r'S05E([0-9]+)',
        replace=r'S04E\{1-10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S04E10", f"Expected 'S04E10', got '{result}'"


def test_math_multiplication():
    """Test Episode_3 -> Episode_6 with \1*2"""
    result = apply_pattern(
        filename="Episode_3",
        search=r'Episode_([0-9]+)',
        replace=r'Episode_\{1*2}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Episode_6", f"Expected 'Episode_6', got '{result}'"


def test_math_division():
    """Test Chapter_10 -> Chapter_5 with \1/2"""
    result = apply_pattern(
        filename="Chapter_10",
        search=r'Chapter_([0-9]+)',
        replace=r'Chapter_\{1/2}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "Chapter_5", f"Expected 'Chapter_5', got '{result}'"


def test_complex_expression():
    """Test complex math expression (\1*2+5)"""
    result = apply_pattern(
        filename="video_3.mp4",
        search=r'video_([0-9]+)\.mp4',
        replace=r'video_\{1*2+5}.mp4',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "video_11.mp4", f"Expected 'video_11.mp4', got '{result}'"


def test_multiple_groups():
    """Test multiple capture groups with math"""
    result = apply_pattern(
        filename="S02E05",
        search=r'S([0-9]+)E([0-9]+)',
        replace=r'S\{1-1}E\{2+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S1E15", f"Expected 'S1E15', got '{result}'"


def test_no_math_operations():
    """Test standard replacement still works"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\1',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E01", f"Expected 'S01E01', got '{result}'"


def test_zero_padding():
    """Test that single digit results maintain format"""
    result = apply_pattern(
        filename="S02E01",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{1+0}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S01E1", f"Expected 'S01E1', got '{result}'"


if __name__ == "__main__":
    # Run all tests
    test_basic_math_addition()
    print("✓ Basic math addition")

    test_math_subtraction()
    print("✓ Math subtraction")

    test_math_multiplication()
    print("✓ Math multiplication")

    test_math_division()
    print("✓ Math division")

    test_complex_expression()
    print("✓ Complex expression")

    test_multiple_groups()
    print("✓ Multiple capture groups")

    test_no_math_operations()
    print("✓ Standard replacement (no math)")

    test_zero_padding()
    print("✓ Zero padding test")

    print("\n✅ All tests passed!")
