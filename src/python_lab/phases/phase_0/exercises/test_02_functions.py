import pytest

def clamp(value, minimum, maximum):
    """Keep value within [minimum, maximum].

    clamp(5,  0, 10) -> 5
    clamp(-3, 0, 10) -> 0
    clamp(15, 0, 10) -> 10
    """
    return max(min(value, maximum), minimum)


def count_vowels(text):
    """Count vowels (a e i o u) in text. Case-insensitive.

    count_vowels("hello")  -> 2
    count_vowels("AEIOU")  -> 5
    count_vowels("rhythm") -> 0
    count_vowels("")       -> 0
    """
    return sum(1 for char in text.lower() if char in "aeiou")


def fizzbuzz(n):
    """Classic fizzbuzz for a single number. Return a string.

    fizzbuzz(1)  -> "1"
    fizzbuzz(3)  -> "Fizz"
    fizzbuzz(5)  -> "Buzz"
    fizzbuzz(15) -> "FizzBuzz"
    """
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    else: 
        return str(n)


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit. Formula: F = (C * 9/5) + 32

    celsius_to_fahrenheit(0)   -> 32.0
    celsius_to_fahrenheit(100) -> 212.0
    celsius_to_fahrenheit(-40) -> -40.0
    """
    return (c*9/5)+32


def first_and_last(items):
    """Return (first, last) item. Return None if list is empty.
    If one item, return (item, item).

    first_and_last([1, 2, 3]) -> (1, 3)
    first_and_last([7])       -> (7, 7)
    first_and_last([])        -> None
    """
    if not items:
        return None
    else:
        return items[0], items[-1]


def make_greeting(name, greeting="Hello"):
    """Return a greeting string using a default argument.

    make_greeting("Ada")               -> "Hello, Ada!"
    make_greeting("Grace", "Hi")       -> "Hi, Grace!"
    make_greeting("Alan", greeting="Hey") -> "Hey, Alan!"
    """
    return f"{greeting}, {name}!"


# ── tests ─────────────────────────────────────────────────────────

class TestClamp:
    @pytest.mark.parametrize("value, lo, hi, expected", [
        (5,   0, 10, 5),
        (-3,  0, 10, 0),
        (15,  0, 10, 10),
        (0,   0, 10, 0),
        (10,  0, 10, 10),
        (5.5, 0.0, 5.0, 5.0),
    ])
    def test_cases(self, value, lo, hi, expected):
        assert clamp(value, lo, hi) == expected


class TestCountVowels:
    @pytest.mark.parametrize("text, expected", [
        ("hello",    2),
        ("AEIOU",    5),
        ("rhythm",   0),
        ("",         0),
        ("Engineer", 4),
    ])
    def test_cases(self, text, expected):
        assert count_vowels(text) == expected


class TestFizzbuzz:
    @pytest.mark.parametrize("n, expected", [
        (1,  "1"), (3, "Fizz"), (5, "Buzz"),
        (9,  "Fizz"), (10, "Buzz"), (15, "FizzBuzz"), (30, "FizzBuzz"),
    ])
    def test_cases(self, n, expected):
        assert fizzbuzz(n) == expected

    def test_returns_string(self):
        assert isinstance(fizzbuzz(7), str)


class TestCelsiusToFahrenheit:
    def test_freezing(self):
        assert celsius_to_fahrenheit(0) == pytest.approx(32.0)

    def test_boiling(self):
        assert celsius_to_fahrenheit(100) == pytest.approx(212.0)

    def test_equal_point(self):
        assert celsius_to_fahrenheit(-40) == pytest.approx(-40.0)


class TestFirstAndLast:
    def test_multiple(self):
        assert first_and_last([1, 2, 3]) == (1, 3)

    def test_single(self):
        assert first_and_last([7]) == (7, 7)

    def test_empty(self):
        assert first_and_last([]) is None


class TestMakeGreeting:
    def test_default(self):
        assert make_greeting("Ada") == "Hello, Ada!"

    def test_custom_positional(self):
        assert make_greeting("Grace", "Hi") == "Hi, Grace!"

    def test_custom_keyword(self):
        assert make_greeting("Alan", greeting="Hey") == "Hey, Alan!"