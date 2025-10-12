import pytest
from streak import longest_positive_streak

def test_empty_list():
    """Test that an empty list returns a streak of 0."""
    assert longest_positive_streak([]) == 0

def test_multiple_streaks():
    """Test that the longest streak is returned when there are multiple streaks."""
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_all_positive():
    """Test a list with all positive numbers."""
    assert longest_positive_streak([1, 1, 1]) == 3

def test_zeros_and_negatives():
    """Test a list containing only zeros and negative numbers."""
    assert longest_positive_streak([-1, -2, 0, -5]) == 0

def test_single_element_streaks():
    """Test with single element positive streaks."""
    assert longest_positive_streak([1, -1, 2, -2, 3, 0, 4]) == 1

def test_streak_at_end():
    """Test when the longest streak is at the end of the list."""
    assert longest_positive_streak([1, 2, 0, 4, 5, 6]) == 3

def test_streak_at_beginning():
    """Test when the longest streak is at the beginning of the list."""
    assert longest_positive_streak([4, 5, 6, 0, 1, 2]) == 3

def test_no_positive_numbers():
    """Test a list with no positive numbers."""
    assert longest_positive_streak([-1, -2, -3]) == 0

def test_single_positive_number():
    """Test a list with a single positive number."""
    assert longest_positive_streak([5]) == 1