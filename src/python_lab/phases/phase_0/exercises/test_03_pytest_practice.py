"""
Functions to test:
    src/python_lab/phases/phase_0/exercises/pytest_practice.py

Run tests:
    pytest src/python_lab/phases/phase_0/exercises/test_03_pytest_practice.py -v
"""

import pytest
from python_lab.phases.phase_0.exercises.pytest_practice import (
    absolute_value,
    is_even,
    clamp,
    reverse_string,
    count_vowels,
    filter_positive,
    find_longest,
    safe_divide,
    create_user,
    grade_score,
)


# ══════════════════════════════════════════════════════════════════
# Basic assertions
# ══════════════════════════════════════════════════════════════════

class TestAbsoluteValue:
  """Test the absolute_value function"""
  def test_absolute_value_positive(self):
    """Test that positive numbers return positive"""
    assert absolute_value(5) == 5
  
  def test_absolute_value_negative(self):
    """Test that negative numbers return positive"""
    assert absolute_value(-5) == 5
  
  def test_absolute_value_zero(self):
    """Test that zero returns zero"""
    assert absolute_value(0) == 0

class TestIsEven:
    """Test the is_even function"""
    def test_is_even_true(self):
        """Test that even numbers return True"""
        assert is_even(4) == True
    
    def test_is_even_false(self):
        """Test that odd numbers return False"""
        assert is_even(7) == False
    
    def test_is_even_zero(self):
        """Test that zero is even"""
        assert is_even(0) == True

class TestClamp:
    """Test the clamp function"""
    def test_clamp_same(self):
        """Test that values within range stay the same"""
        assert clamp(5, 0, 10) == 5
    
    def test_clamp_return_low(self):
        """Test that values below range return low"""
        assert clamp(-3, 0, 10) == 0
    
    def test_clamp_return_high(self):
        """Test that values above range return high"""
        assert clamp(15, 0, 10) == 10


# ══════════════════════════════════════════════════════════════════
# Parametrize
# ══════════════════════════════════════════════════════════════════
class TestParametrize:
    """Test the parametrize functions"""
    @pytest.mark.parametrize("input_val, expected", [
        ("hello", "olleh"),
        ("", ""),
        ("a", "a"),
    ])
    def test_reverse_string(self, input_val, expected):
        """Test the reverse_string function"""
        assert reverse_string(input_val) == expected

    @pytest.mark.parametrize("text, expected", [
        ("hello", 2),
        ("AEIOU", 5),
        ("rhythm", 0),
        ("", 0),
    ])
    def test_count_vowels(self, text, expected):
        """Test the count_vowels function"""
        assert count_vowels(text) == expected

    @pytest.mark.parametrize("numbers, expected", [
        ([1, -2, 3, 0, -5], [1, 3]),
        ([-1, -2], []),
        ([], []),
    ])
    def test_filter_positive(self, numbers, expected):
        """Test the filter_positive function"""
        assert filter_positive(numbers) == expected



# ══════════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════════
class TestFixtures:
    """Test the fixtures"""
    @pytest.fixture
    def word_list(self):
        return ["python", "is", "awesome", "and", "fun"]

    def test_find_longest(self, word_list):
        """Test the find_longest function"""
        assert find_longest(word_list) == "awesome"

    def test_find_longest_empty(self):
        """Test the find_longest function with an empty list"""
    assert find_longest([]) is None


# ══════════════════════════════════════════════════════════════════
# Testing exceptions
# ══════════════════════════════════════════════════════════════════

class TestSafeDivide:
    """Test the safe_divide function"""
    def test_safe_divide_positive(self):
        """Test that safe_divide(10, 2) returns 5.0"""
        assert safe_divide(10, 2) == 5.0

    def test_safe_divide_zero(self):
        """Test that safe_divide(10, 0) raises ValueError"""
        with pytest.raises(ValueError):
            safe_divide(10, 0)

    def test_safe_divide_zero_message(self):
        """Test that safe_divide(10, 0) raises ValueError with the message "cannot divide by zero" (use match=)"""
        with pytest.raises(ValueError, match="cannot divide by zero"):
            safe_divide(10, 0)

class TestCreateUser:
    """Test the create_user function"""
    def test_create_user_positive(self):
        """Test that create_user("Ada", 36) returns the correct dictionary"""
        assert create_user("Ada", 36) == {"name": "Ada", "age": 36}

    def test_create_user_empty(self):
        """Test that create_user("", 25) raises ValueError"""
        with pytest.raises(ValueError):
            create_user("", 25)

    def test_create_user_negative(self):
        """Test that create_user("Ada", -1) raises ValueError"""
        with pytest.raises(ValueError):
            create_user("Ada", -1)

# ══════════════════════════════════════════════════════════════════
# Parametrize + Exceptions
# ══════════════════════════════════════════════════════════════════
class TestGradeScore:
    """Test the grade_score function"""
    @pytest.mark.parametrize("score, expected", [
        (95, "A"),
        (90, "A"),
        (85, "B"),
        (80, "B"),
        (75, "C"),
        (70, "C"),
        (65, "D"),
        (60, "D"),
        (55, "F"),
        (0, "F"),
        (100, "A"),
    ])
    def test_grade_score(self, score, expected):
        """Test the grade_score function"""
        assert grade_score(score) == expected

    @pytest.mark.parametrize("score", [-1, 101, -100, 200])
    def test_grade_score_invalid(self, score):
        """Test that grade_score raises ValueError for invalid scores"""
        with pytest.raises(ValueError, match=f"score must be between 0 and 100, got {score}"):
            grade_score(score)
