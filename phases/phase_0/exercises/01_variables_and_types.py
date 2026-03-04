# Exercise 01 — Variables & Types
# Run: python phases/phase_0/exercises/01_variables_and_types.py
#
# Fill in each function body. When you run the file, it checks your answers.
# A passing function prints ✅. A failing one prints ❌ and shows you what went wrong.


def get_type_name(value) -> str:
    """Return the type name of value as a string.

    get_type_name(42)    -> "int"
    get_type_name("hi")  -> "str"
    get_type_name(3.14)  -> "float"
    get_type_name(None)  -> "NoneType"
    """
    return type(value).__name__


def is_falsy(value) -> bool:
    """Return True if value is falsy, False otherwise.

    is_falsy(0)    -> True
    is_falsy("")   -> True
    is_falsy([])   -> True
    is_falsy(1)    -> False
    is_falsy("hi") -> False
    """
    return not bool(value)


def safe_to_int(value) -> int | None:
    """Convert a string to int. Return None if it can't be converted.

    safe_to_int("42")   -> 42
    safe_to_int("abc")  -> None
    safe_to_int("3.14") -> None
    """
    try:
        return int(value)
    except ValueError:
        return None


def describe_number(n) -> str:
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


def swap(a, b) -> tuple:
    """Return a tuple (b, a) — the two values swapped.

    swap(1, 2)     -> (2, 1)
    swap("x", "y") -> ("y", "x")
    """
    return b, a


# ── checks ────────────────────────────────────────────────────────────────────

def check(label, got, expected):
    if got == expected:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")


print("\n── Exercise 01: Variables & Types ──────────────────────")

print("\nget_type_name")
check('get_type_name(42)',    get_type_name(42),    "int")
check('get_type_name("hi")',  get_type_name("hi"),  "str")
check('get_type_name(3.14)',  get_type_name(3.14),  "float")
check('get_type_name(True)',  get_type_name(True),  "bool")
check('get_type_name(None)',  get_type_name(None),  "NoneType")

print("\nis_falsy")
check('is_falsy(0)',    is_falsy(0),    True)
check('is_falsy("")',   is_falsy(""),   True)
check('is_falsy([])',   is_falsy([]),   True)
check('is_falsy(None)', is_falsy(None), True)
check('is_falsy(1)',    is_falsy(1),    False)
check('is_falsy("hi")', is_falsy("hi"), False)

print("\nsafe_to_int")
check('safe_to_int("42")',   safe_to_int("42"),   42)
check('safe_to_int("0")',    safe_to_int("0"),    0)
check('safe_to_int("abc")',  safe_to_int("abc"),  None)
check('safe_to_int("3.14")', safe_to_int("3.14"), None)
check('safe_to_int("")',     safe_to_int(""),     None)

print("\ndescribe_number")
check('describe_number(5)',    describe_number(5),    "positive")
check('describe_number(-3)',   describe_number(-3),   "negative")
check('describe_number(0)',    describe_number(0),    "zero")
check('describe_number(0.0)',  describe_number(0.0),  "zero")
check('describe_number(-0.1)', describe_number(-0.1), "negative")

print("\nswap")
check('swap(1, 2)',       swap(1, 2),       (2, 1))
check('swap("x", "y")',   swap("x", "y"),   ("y", "x"))
check('swap(True, None)', swap(True, None), (None, True))

print()