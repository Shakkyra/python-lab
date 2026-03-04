# Exercise 02 — Functions
# Run: python phases/phase_0/exercises/02_functions.py
#
# Fill in each function. Run the file to see which pass and which don't.
# All functions must be PURE — no global variables, no print() inside them.


def clamp(value, minimum, maximum) -> int:
    """Keep value within [minimum, maximum].

    clamp(5,  0, 10) -> 5
    clamp(-3, 0, 10) -> 0
    clamp(15, 0, 10) -> 10
    """
    return max(min(value, maximum), minimum)


def count_vowels(text) -> int:
    """Count vowels (a e i o u) in text. Case-insensitive.

    count_vowels("hello")  -> 2
    count_vowels("AEIOU")  -> 5
    count_vowels("rhythm") -> 0
    count_vowels("")       -> 0
    """
    return sum(1 for char in text.lower() if char in "aeiou")


def fizzbuzz(n) -> str:
    """Classic fizzbuzz for a single number. Return a string.

    fizzbuzz(1)  -> "1"
    fizzbuzz(3)  -> "Fizz"
    fizzbuzz(5)  -> "Buzz"
    fizzbuzz(15) -> "FizzBuzz"

    Hint: check 15 before 3 and 5.
    """
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def celsius_to_fahrenheit(c) -> float:
    """Convert Celsius to Fahrenheit. Formula: F = (C * 9/5) + 32

    celsius_to_fahrenheit(0)   -> 32.0
    celsius_to_fahrenheit(100) -> 212.0
    celsius_to_fahrenheit(-40) -> -40.0
    """
    return (c * 9/5) + 32


def first_and_last(items) -> tuple | None:
    """Return (first, last) item. Return None if list is empty.
    If one item, return (item, item).

    first_and_last([1, 2, 3]) -> (1, 3)
    first_and_last([7])       -> (7, 7)
    first_and_last([])        -> None
    """
    if not items:
        return None
    return items[0], items[-1]


def make_greeting(name, greeting="Hello") -> str:
    """Return a greeting string using a default argument.

    make_greeting("Ada")               -> "Hello, Ada!"
    make_greeting("Grace", "Hi")       -> "Hi, Grace!"
    make_greeting("Alan", greeting="Hey") -> "Hey, Alan!"
    """
    return f"{greeting}, {name}!"


# ── checks ────────────────────────────────────────────────────────────────────

def check(label, got, expected):
    if got == expected:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")

def approx_check(label, got, expected, tol=0.01):
    if got is not None and abs(got - expected) < tol:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label}")
        print(f"       expected: ~{expected!r}")
        print(f"       got:       {got!r}")


print("\n── Exercise 02: Functions ───────────────────────────────")

print("\nclamp")
check('clamp(5,  0, 10)', clamp(5,  0, 10), 5)
check('clamp(-3, 0, 10)', clamp(-3, 0, 10), 0)
check('clamp(15, 0, 10)', clamp(15, 0, 10), 10)
check('clamp(0,  0, 10)', clamp(0,  0, 10), 0)
check('clamp(10, 0, 10)', clamp(10, 0, 10), 10)

print("\ncount_vowels")
check('count_vowels("hello")',  count_vowels("hello"),  2)
check('count_vowels("AEIOU")',  count_vowels("AEIOU"),  5)
check('count_vowels("rhythm")', count_vowels("rhythm"), 0)
check('count_vowels("")',       count_vowels(""),       0)
check('count_vowels("Engineer")', count_vowels("Engineer"), 4)

print("\nfizzbuzz")
check('fizzbuzz(1)',  fizzbuzz(1),  "1")
check('fizzbuzz(3)',  fizzbuzz(3),  "Fizz")
check('fizzbuzz(5)',  fizzbuzz(5),  "Buzz")
check('fizzbuzz(15)', fizzbuzz(15), "FizzBuzz")
check('fizzbuzz(30)', fizzbuzz(30), "FizzBuzz")
check('fizzbuzz(7)',  fizzbuzz(7),  "7")

print("\ncelsius_to_fahrenheit")
approx_check('celsius_to_fahrenheit(0)',    celsius_to_fahrenheit(0),    32.0)
approx_check('celsius_to_fahrenheit(100)',  celsius_to_fahrenheit(100),  212.0)
approx_check('celsius_to_fahrenheit(-40)',  celsius_to_fahrenheit(-40),  -40.0)
approx_check('celsius_to_fahrenheit(37)',   celsius_to_fahrenheit(37),   98.6)

print("\nfirst_and_last")
check('first_and_last([1,2,3])', first_and_last([1, 2, 3]), (1, 3))
check('first_and_last([7])',     first_and_last([7]),       (7, 7))
check('first_and_last([])',      first_and_last([]),        None)
check('first_and_last([10,20])', first_and_last([10, 20]), (10, 20))

print("\nmake_greeting")
check('make_greeting("Ada")',                make_greeting("Ada"),                "Hello, Ada!")
check('make_greeting("Grace", "Hi")',        make_greeting("Grace", "Hi"),        "Hi, Grace!")
check('make_greeting("Alan", greeting="Hey")', make_greeting("Alan", greeting="Hey"), "Hey, Alan!")

print()