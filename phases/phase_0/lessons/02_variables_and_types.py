"""
Lesson 02 — Variables and Types
=================================
Run this file:
    python phase_0/lessons/02_variables_and_types.py

Python is dynamically typed — you don't declare types, Python infers them.
But types still exist, still matter, and still cause bugs when you ignore them.
"""

print("=" * 50)
print("Lesson 02: Variables and Types")
print("=" * 50)


# ─────────────────────────────────────────────
# 1. VARIABLES
# ─────────────────────────────────────────────

print("\n--- Section 1: Variables ---")

# A variable is a name that points to a value in memory.
# Assignment uses =  (not ==, which is comparison)
name = "Ada"
age = 36
height = 1.75
is_engineer = True

print(f"name={name!r}  age={age!r}  height={height!r}  is_engineer={is_engineer!r}")

# Variables can be reassigned to a completely different type:
x = 10
print(f"x is {x!r}, type: {type(x).__name__}")
x = "now I'm a string"
print(f"x is {x!r}, type: {type(x).__name__}")
# Python doesn't stop you — this is both flexible and a source of bugs.


# ─────────────────────────────────────────────
# 2. THE CORE TYPES
# ─────────────────────────────────────────────

print("\n--- Section 2: Core types ---")

# int — whole numbers, no size limit
population = 8_100_000_000       # underscores for readability
print(f"int:   {population}")

# float — decimal numbers (IEEE 754 — has precision limits)
pi = 3.14159
print(f"float: {pi}")
print(f"float gotcha: 0.1 + 0.2 = {0.1 + 0.2}")   # not 0.3!

# str — text, immutable, Unicode
greeting = "Hello"
also_valid = 'single quotes work too'
multiline = """
    Triple quotes for
    multi-line strings
"""
print(f"str: {greeting!r}")
print(f"str length: {len(greeting)}")
print(f"str indexing: greeting[0] = {greeting[0]!r}")
print(f"str slicing:  greeting[1:4] = {greeting[1:4]!r}")

# bool — True or False (note: capital first letter)
flag = True
print(f"bool: {flag}, type: {type(flag).__name__}")
print(f"bool math: True + True = {True + True}")   # bools are ints under the hood

# NoneType — the absence of a value (Python's null)
result = None
print(f"None: {result!r}, type: {type(result).__name__}")


# ─────────────────────────────────────────────
# 3. TYPE CONVERSION (CASTING)
# ─────────────────────────────────────────────

print("\n--- Section 3: Type conversion ---")

# Explicit conversion with built-in functions
s = "42"
n = int(s)         # str → int
f = float(s)       # str → float
b = bool(n)        # int → bool

print(f"int('42')   = {n!r}")
print(f"float('42') = {f!r}")
print(f"bool(42)    = {b!r}")

# "Truthy" and "Falsy" — every value has a boolean interpretation
falsy_values = [0, 0.0, "", [], {}, set(), None, False]
print("\nFalsy values:")
for v in falsy_values:
    print(f"  bool({v!r}) = {bool(v)}")

# This matters in conditionals:
user_input = ""
if user_input:
    print("Got input")
else:
    print("Empty string is falsy → no input")


# ─────────────────────────────────────────────
# 4. MUTABILITY — THE CONCEPT THAT TRIPS EVERYONE
# ─────────────────────────────────────────────

print("\n--- Section 4: Mutability ---")

# Immutable types: int, float, str, bool, tuple
# Once created, their VALUE cannot change in memory.

a = "hello"
b = a               # b points to the same string object
a = a + " world"    # this creates a NEW string, a now points to it
print(f"a = {a!r}")
print(f"b = {b!r}")  # b still points to the original — it did NOT change

# Mutable types: list, dict, set
# Their contents CAN change in place.

list_a = [1, 2, 3]
list_b = list_a         # list_b points to the SAME list object
list_a.append(4)        # modifies the list in place
print(f"\nlist_a = {list_a}")
print(f"list_b = {list_b}")  # ⚠️ list_b also changed! Same object.

# To get an independent copy:
list_c = list_a.copy()
list_a.append(5)
print(f"\nlist_a = {list_a}")
print(f"list_c = {list_c}")  # ✅ list_c unaffected


# ─────────────────────────────────────────────
# 5. CHECKING TYPES
# ─────────────────────────────────────────────

print("\n--- Section 5: Checking types ---")

value = 42
print(f"type(42)          → {type(value)}")
print(f"isinstance(42, int) → {isinstance(value, int)}")
print(f"isinstance(42, (int, float)) → {isinstance(value, (int, float))}")

# Prefer isinstance() over type() — it handles inheritance correctly.


# ─────────────────────────────────────────────
# WRAP UP
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("✅ Lesson 02 complete.")
print("   Next: python phase_0/lessons/03_your_first_functions.py")
print("=" * 50)

# QUICK KNOWLEDGE CHECK
#
# Q1: What is the difference between = and ==?
# Q2: Name two mutable and two immutable types.
# Q3: What does bool("") return? Why?
# Q4: If list_b = list_a and you append to list_a, does list_b change?
#
# Answers:
# Q1: = assigns, == compares
# Q2: mutable: list, dict | immutable: str, int
# Q3: False — empty string is falsy
# Q4: Yes — both names point to the same list object