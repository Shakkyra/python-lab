"""
Lesson 03 — Your First Functions
==================================
Run this file:
    python phase_0/lessons/03_your_first_functions.py

Functions are the single most important unit in Python.
Everything — classes, patterns, modules — is built on top of them.
Understand functions deeply and everything else becomes easier.
"""

print("=" * 50)
print("Lesson 03: Your First Functions")
print("=" * 50)


# ─────────────────────────────────────────────
# 1. DEFINING A FUNCTION
# ─────────────────────────────────────────────

print("\n--- Section 1: Defining functions ---")

# Anatomy of a function:
#
#   def <name>(<parameters>) -> <return type>:
#       """Docstring: what this function does."""
#       <body>
#       return <value>

def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b


result = add(3, 4)
print(f"add(3, 4) = {result}")

# If a function has no return statement, it returns None implicitly.
def say_hello(name: str) -> None:
    """Print a greeting. Returns nothing."""
    print(f"Hello, {name}!")

say_hello("engineer")
returned = say_hello("world")
print(f"say_hello returned: {returned!r}")   # None


# ─────────────────────────────────────────────
# 2. PARAMETERS AND ARGUMENTS
# ─────────────────────────────────────────────

print("\n--- Section 2: Parameters ---")

# Positional arguments — order matters
def subtract(a: int, b: int) -> int:
    """Return a minus b."""
    return a - b

print(f"subtract(10, 3) = {subtract(10, 3)}")  # 7
print(f"subtract(3, 10) = {subtract(3, 10)}")  # -7

# Default arguments — used when caller doesn't provide a value
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting string."""
    return f"{greeting}, {name}!"

print(greet("Ada"))                         # uses default
print(greet("Grace", greeting="Hi"))       # overrides default
print(greet("Grace", "Hey"))               # positional override

# Keyword arguments — explicitly name the argument
def describe(name: str, age: int, city: str) -> str:
    return f"{name}, {age}, from {city}"

# Both calls below are identical:
print(describe("Ada", 36, "London"))
print(describe(age=36, city="London", name="Ada"))   # order doesn't matter with keywords


# ─────────────────────────────────────────────
# 3. RETURN VALUES
# ─────────────────────────────────────────────

print("\n--- Section 3: Return values ---")

# A function can return any type — including multiple values (as a tuple)
def min_max(numbers: list[int]) -> tuple[int, int]:
    """Return (minimum, maximum) of a list."""
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"min={low}, max={high}")

# IMPORTANT: return exits the function immediately.
# Code after return is never executed.
def first_positive(numbers: list[int]) -> int | None:
    """Return the first positive number, or None if none found."""
    for n in numbers:
        if n > 0:
            return n    # ← exits here as soon as we find one
    return None         # ← only reached if loop finishes without returning

print(first_positive([-1, -2, 5, 3]))   # 5
print(first_positive([-1, -2, -3]))     # None


# ─────────────────────────────────────────────
# 4. TYPE HINTS — WRITE THEM ALWAYS
# ─────────────────────────────────────────────

print("\n--- Section 4: Type hints ---")

# Type hints don't change how Python runs your code.
# They are a contract — documentation that tools (mypy, your IDE) can check.

# WITHOUT type hints — what does this take? What does it return?
def process(x, y):
    return x * y

# WITH type hints — crystal clear
def multiply(x: int, y: int) -> int:
    """Return x multiplied by y."""
    return x * y

# Run mypy to catch type errors before they become runtime bugs:
#   mypy phase_0/lessons/03_your_first_functions.py

print(f"multiply(4, 5) = {multiply(4, 5)}")


# ─────────────────────────────────────────────
# 5. PURE FUNCTIONS — THE GOLDEN STANDARD
# ─────────────────────────────────────────────

print("\n--- Section 5: Pure functions ---")

# A PURE function:
#   1. Always returns the same output for the same input
#   2. Has no side effects (doesn't modify anything outside itself)

# ✅ Pure — predictable, testable, reusable
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32

# ❌ Impure — result depends on external state
total = 0

def add_to_total(n: int) -> int:
    """Add n to the running total and return it."""
    global total            # modifies something outside the function
    total += n
    return total

print(f"celsius_to_fahrenheit(100) = {celsius_to_fahrenheit(100)}")
print(f"add_to_total(5) = {add_to_total(5)}")
print(f"add_to_total(5) = {add_to_total(5)}")  # same input, different result!

# Write pure functions whenever possible.
# They're easier to test, debug, and reason about.
# Design patterns (phase 4) are much easier with a pure-function mindset.


# ─────────────────────────────────────────────
# WRAP UP
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("✅ Lesson 03 complete.")
print("   Now go do the exercises:")
print("   → phase_0/exercises/exercise_01.py")
print("   → phase_0/exercises/exercise_02.py")
print("=" * 50)

# QUICK KNOWLEDGE CHECK
#
# Q1: What does a function return if it has no return statement?
# Q2: What is a pure function? Why prefer it?
# Q3: What is the difference between a parameter and an argument?
# Q4: If I call greet("Ada") and the function is def greet(name, greeting="Hello"),
#     what does greeting equal inside the function?
#
# Answers:
# Q1: None
# Q2: Same input → same output, no side effects. Easier to test + reason about.
# Q3: Parameter = the variable in the def. Argument = the value you pass when calling.
# Q4: "Hello" (the default)