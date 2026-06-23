"""Test edge cases for mathematical operations."""

from src.filerenamer.utils.renamer import apply_pattern


def test_no_match():
    """Test when pattern doesn't match"""
    result = apply_pattern(
        filename="NoMatch.txt",
        search=r'S02E([0-9]+)',
        replace=r'S01E\{1+10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "NoMatch.txt", f"Expected 'NoMatch.txt', got '{result}'"


def test_non_numeric_capture():
    """Test math operation on non-numeric capture (should fail gracefully)"""
    result = apply_pattern(
        filename="Season_Two_Episode_One",
        search=r'Season_(\w+)_Episode',
        replace=r'Season_\{1+10}_Episode',
        case_sensitive=True,
        use_regex=True
    )
    # Should not crash, returns original or best-effort result
    assert result is not None


def test_division_by_zero():
    """Test division by zero (should fail gracefully)"""
    result = apply_pattern(
        filename="value_10",
        search=r'value_([0-9]+)',
        replace=r'value_\{1/0}',
        case_sensitive=True,
        use_regex=True
    )
    # Should not crash
    assert result is not None


def test_parentheses_in_expression():
    """Test parentheses in math expression"""
    result = apply_pattern(
        filename="num_5",
        search=r'num_([0-9]+)',
        replace=r'num_\{(1+5)*2}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "num_20", f"Expected 'num_20', got '{result}'"


def test_float_result():
    """Test float division"""
    result = apply_pattern(
        filename="value_7",
        search=r'value_([0-9]+)',
        replace=r'value_\{1/2}',
        case_sensitive=True,
        use_regex=True
    )
    # 7/2 = 3.5
    assert result == "value_3.5", f"Expected 'value_3.5', got '{result}'"


def test_floor_division():
    """Test floor division"""
    result = apply_pattern(
        filename="value_7",
        search=r'value_([0-9]+)',
        replace=r'value_\{1//2}',
        case_sensitive=True,
        use_regex=True
    )
    # 7//2 = 3
    assert result == "value_3", f"Expected 'value_3', got '{result}'"


def test_modulo():
    """Test modulo operation"""
    result = apply_pattern(
        filename="value_17",
        search=r'value_([0-9]+)',
        replace=r'value_\{1%5}',
        case_sensitive=True,
        use_regex=True
    )
    # 17 % 5 = 2
    assert result == "value_2", f"Expected 'value_2', got '{result}'"


def test_power():
    """Test power/exponent operation"""
    result = apply_pattern(
        filename="value_3",
        search=r'value_([0-9]+)',
        replace=r'value_\{1**2}',
        case_sensitive=True,
        use_regex=True
    )
    # 3^2 = 9
    assert result == "value_9", f"Expected 'value_9', got '{result}'"


def test_negative_result():
    """Test negative result"""
    result = apply_pattern(
        filename="value_5",
        search=r'value_([0-9]+)',
        replace=r'value_\{1-10}',
        case_sensitive=True,
        use_regex=True
    )
    # 5-10 = -5
    assert result == "value_-5", f"Expected 'value_-5', got '{result}'"


def test_mixed_math_and_backrefs():
    """Test mixing math expressions with regular backreferences"""
    result = apply_pattern(
        filename="S02E05_title",
        search=r'S([0-9]+)E([0-9]+)_(\w+)',
        replace=r'S\{1-1}E\{2+10}_\3',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "S1E15_title", f"Expected 'S1E15_title', got '{result}'"


def test_zero_result():
    """Test that zero is formatted correctly"""
    result = apply_pattern(
        filename="value_10",
        search=r'value_([0-9]+)',
        replace=r'value_\{1-10}',
        case_sensitive=True,
        use_regex=True
    )
    assert result == "value_0", f"Expected 'value_0', got '{result}'"


if __name__ == "__main__":
    test_no_match()
    print("✓ No match case")

    test_non_numeric_capture()
    print("✓ Non-numeric capture (graceful failure)")

    test_division_by_zero()
    print("✓ Division by zero (graceful failure)")

    test_parentheses_in_expression()
    print("✓ Parentheses in expression")

    test_float_result()
    print("✓ Float result")

    test_floor_division()
    print("✓ Floor division")

    test_modulo()
    print("✓ Modulo operation")

    test_power()
    print("✓ Power/exponent operation")

    test_negative_result()
    print("✓ Negative result")

    test_mixed_math_and_backrefs()
    print("✓ Mixed math and regular backrefs")

    test_zero_result()
    print("✓ Zero result")

    print("\n✅ All edge case tests passed!")
