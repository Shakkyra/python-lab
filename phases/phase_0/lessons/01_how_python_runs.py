"""
Lesson 01 — How Python Runs Your Code
======================================
Run this file:
    python phase_0/lessons/01_how_python_runs.py

Python executes files top-to-bottom, one line at a time.
This file is both a lesson and a live demo — reading it *and* running it
will teach you more than just reading alone.
"""

# ─────────────────────────────────────────────
# 1. SCRIPTS vs THE REPL
# ─────────────────────────────────────────────
#
# You can run Python in two ways:
#
#   A) Script mode — run a file:
#      $ python my_file.py
#      Python reads the whole file and executes it.
#
#   B) REPL (Read-Eval-Print Loop) — interactive shell:
#      $ python
#      >>> 2 + 2
#      4
#      Great for quick experiments. Terrible for saving work.
#
# In this course, we always work in script mode.


# ─────────────────────────────────────────────
# 2. PRINT — YOUR BEST DEBUGGING FRIEND
# ─────────────────────────────────────────────

print("=" * 50)
print("Lesson 01: How Python Runs")
print("=" * 50)

# print() sends output to your terminal.
# You'll use this constantly for debugging.
print("\n--- Section 1: print() ---")
print("Hello, Python.")
print("You can print", "multiple", "things", "with commas")
print("Or with f-strings:", f"1 + 1 = {1 + 1}")


# ─────────────────────────────────────────────
# 3. COMMENTS
# ─────────────────────────────────────────────

print("\n--- Section 2: Comments ---")

# This is a single-line comment. Python ignores everything after #.
# Use comments to explain WHY, not WHAT (the code shows what).

"""
This is a docstring — a string that documents a module, class, or function.
It's not ignored like comments; Python stores it as metadata.
You'll see these on every function in this course.
"""

print("Comments are invisible to Python. Only you can see them.")


# ─────────────────────────────────────────────
# 4. THE __name__ TRICK — THE MOST IMPORTANT PYTHON IDIOM
# ─────────────────────────────────────────────

print("\n--- Section 3: __name__ ---")

# When Python runs a file, it sets a special variable: __name__
# If you ran THIS file directly:  __name__ == "__main__"
# If another file imported THIS file: __name__ == "phase_0.lessons.01_how_python_runs"

print(f"This file's __name__ is: {__name__!r}")

# The pattern you'll see EVERYWHERE:
#
#   if __name__ == "__main__":
#       main()
#
# This means: "only run this code if the file was executed directly,
# not if it was imported by something else."
# This lets every file be both a runnable script AND an importable module.


# ─────────────────────────────────────────────
# 5. EXECUTION ORDER — TOP TO BOTTOM
# ─────────────────────────────────────────────

print("\n--- Section 4: Execution order ---")


def greet(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"


# Python read the function definition above but didn't run it yet.
# Only NOW do we call it:
result = greet("engineer")
print(result)

# Key rule: you must DEFINE before you USE.
# Calling greet() before the def would crash with NameError.


# ─────────────────────────────────────────────
# 6. ERRORS — READ THEM, DON'T FEAR THEM
# ─────────────────────────────────────────────

print("\n--- Section 5: Reading errors ---")

# Uncomment the line below to see a real error (then re-comment it):
# print(undefined_variable)

# The error you'd see:
#   NameError: name 'undefined_variable' is not defined
#
# Python errors always tell you:
#   1. The ERROR TYPE  (NameError, TypeError, ValueError, ...)
#   2. The LINE NUMBER where it happened
#   3. A MESSAGE explaining what went wrong
#
# Read errors top-to-bottom. The bottom line is the most useful.

print("Errors are information. Read them carefully.")


# ─────────────────────────────────────────────
# WRAP UP
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("✅ Lesson 01 complete.")
print("   Next: python phase_0/lessons/02_variables_and_types.py")
print("=" * 50)


# ─────────────────────────────────────────────
# QUICK KNOWLEDGE CHECK (answer mentally before moving on)
# ─────────────────────────────────────────────
#
# Q1: What is __name__ equal to when you run a file directly?
# Q2: If you define a function at line 80 and call it at line 10, what happens?
# Q3: What are the two ways to run Python code?
#
# Answers: Q1: "__main__"  Q2: NameError — must define before use  Q3: script / REPL