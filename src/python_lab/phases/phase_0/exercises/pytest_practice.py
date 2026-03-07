

# ─────────────────────────────────────────────────────────────────
# Simple Pure Functions
# ─────────────────────────────────────────────────────────────────

def absolute_value(n: int | float) -> int | float:
    """Return the absolute value of n.
    
    Examples:
        absolute_value(5)   → 5
        absolute_value(-3)  → 3
        absolute_value(0)   → 0
    """
    if n < 0:
        return -n
    return n


def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise.
    
    Examples:
        is_even(4)  → True
        is_even(7)  → False
        is_even(0)  → True
    """
    return n % 2 == 0


def clamp(value: int, low: int, high: int) -> int:
    """Clamp value between low and high (inclusive).
    
    If value < low, return low.
    If value > high, return high.
    Otherwise return value.
    
    Examples:
        clamp(5, 0, 10)   → 5   (within range)
        clamp(-3, 0, 10)  → 0   (below range)
        clamp(15, 0, 10)  → 10  (above range)
    """
    if value < low:
        return low
    if value > high:
        return high
    return value


# ─────────────────────────────────────────────────────────────────
# Working with Strings and Lists
# ─────────────────────────────────────────────────────────────────

def reverse_string(s: str) -> str:
    """Return the string reversed.
    
    Examples:
        reverse_string("hello") → "olleh"
        reverse_string("")      → ""
        reverse_string("a")     → "a"
    """
    return s[::-1]


def count_vowels(text: str) -> int:
    """Count the number of vowels (a, e, i, o, u) in text.
    Case-insensitive.
    
    Examples:
        count_vowels("hello")  → 2
        count_vowels("AEIOU")  → 5
        count_vowels("rhythm") → 0
        count_vowels("")       → 0
    """
    return sum(1 for c in text if c.lower() in "aeiou")


def filter_positive(numbers: list[int]) -> list[int]:
    """Return a new list containing only positive numbers.
    Zero is NOT positive.
    
    Examples:
        filter_positive([1, -2, 3, 0, -5]) → [1, 3]
        filter_positive([-1, -2])           → []
        filter_positive([])                 → []
    """
    return [n for n in numbers if n > 0]


def find_longest(words: list[str]) -> str | None:
    """Return the longest word in the list.
    If the list is empty, return None.
    If there's a tie, return the first one found.
    
    Examples:
        find_longest(["hi", "hello", "hey"]) → "hello"
        find_longest(["a", "b", "c"])        → "a"
        find_longest([])                     → None
    """
    if not words:
        return None
    longest = words[0]
    for word in words[1:]:
        if len(word) > len(longest):
            longest = word
    return longest


# ─────────────────────────────────────────────────────────────────
# Error Handling and Edge Cases
# ─────────────────────────────────────────────────────────────────

def safe_divide(a: float, b: float) -> float:
    """Divide a by b. Raises ValueError if b is zero.
    
    Examples:
        safe_divide(10, 2)   → 5.0
        safe_divide(7, 2)    → 3.5
        safe_divide(0, 5)    → 0.0
        safe_divide(10, 0)   → raises ValueError("cannot divide by zero")
    """
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


def create_user(name: str, age: int) -> dict:
    """Create a user dictionary.
    
    Raises ValueError if:
        - name is empty
        - age is negative
    
    Examples:
        create_user("Ada", 36)  → {"name": "Ada", "age": 36}
        create_user("", 25)     → raises ValueError("name cannot be empty")
        create_user("Ada", -1)  → raises ValueError("age cannot be negative")
    """
    if not name:
        raise ValueError("name cannot be empty")
    if age < 0:
        raise ValueError("age cannot be negative")
    return {"name": name, "age": age}


def grade_score(score: int) -> str:
    """Convert a numerical score (0-100) to a letter grade.
    
    Raises ValueError if score is outside 0-100.
    
    Grading scale:
        90-100 → "A"
        80-89  → "B"
        70-79  → "C"
        60-69  → "D"
        0-59   → "F"
    
    Examples:
        grade_score(95) → "A"
        grade_score(85) → "B"
        grade_score(42) → "F"
        grade_score(-1) → raises ValueError
        grade_score(101) → raises ValueError
    """
    if score < 0 or score > 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
