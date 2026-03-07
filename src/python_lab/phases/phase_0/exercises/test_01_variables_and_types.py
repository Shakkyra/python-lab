import pytest

# Phase 0 — Exercise 01: Variables & Types
# Run: pytest phases/phase_0/exercises/test_01_variables.py -v


def get_type_name(value):
    """Return the type name of value as a string.

    get_type_name(42)   -> "int"
    get_type_name("hi") -> "str"
    get_type_name(None) -> "NoneType"
    """
    return type(value).__name__


def is_falsy(value):
    """Return True if value is falsy, False otherwise.

    is_falsy(0)    -> True
    is_falsy("")   -> True
    is_falsy([])   -> True
    is_falsy(1)    -> False
    is_falsy("hi") -> False
    """
    return not bool(value)


def safe_to_int(value):
    """Convert a string to int. Return None if it can't be converted.

    safe_to_int("42")   -> 42
    safe_to_int("abc")  -> None
    safe_to_int("3.14") -> None
    """
    try:
        return int(value)
    except ValueError:
        return None

def describe_number(n):
    """Return "positive", "negative", or "zero".

    describe_number(5)   -> "positive"
    describe_number(-3)  -> "negative"
    describe_number(0)   -> "zero"
    """
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else: 
        return "zero"


def swap(a, b):
    """Return a tuple (b, a) — the two values swapped.

    swap(1, 2)     -> (2, 1)
    swap("x", "y") -> ("y", "x")
    """
    return b, a


# ── tests ─────────────────────────────────────────────────────────

class TestGetTypeName:
    @pytest.mark.parametrize("value, expected", [
        (42,    "int"),
        ("hi",  "str"),
        (3.14,  "float"),
        (True,  "bool"),
        (None,  "NoneType"),
        ([],    "list"),
    ])
    def test_types(self, value, expected):
        assert get_type_name(value) == expected


class TestIsFalsy:
    @pytest.mark.parametrize("value", [0, 0.0, "", [], {}, set(), None, False])
    def test_falsy(self, value):
        assert is_falsy(value) is True

    @pytest.mark.parametrize("value", [1, -1, "hi", [0], {"a": 1}, True])
    def test_truthy(self, value):
        assert is_falsy(value) is False


class TestSafeToInt:
    @pytest.mark.parametrize("value, expected", [
        ("42",  42),
        ("0",   0),
        ("-10", -10),
    ])
    def test_valid(self, value, expected):
        assert safe_to_int(value) == expected

    @pytest.mark.parametrize("value", ["abc", "3.14", "", " "])
    def test_invalid(self, value):
        assert safe_to_int(value) is None


class TestDescribeNumber:
    @pytest.mark.parametrize("n, expected", [
        (5,    "positive"),
        (0.1,  "positive"),
        (-3,   "negative"),
        (-0.1, "negative"),
        (0,    "zero"),
        (0.0,  "zero"),
    ])
    def test_cases(self, n, expected):
        assert describe_number(n) == expected


class TestSwap:
    def test_integers(self):
        assert swap(1, 2) == (2, 1)

    def test_strings(self):
        assert swap("x", "y") == ("y", "x")

    def test_same_value(self):
        assert swap(5, 5) == (5, 5)