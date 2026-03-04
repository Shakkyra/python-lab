# Phase 0: Knowledge Check 🧠

Test your understanding of the foundational Python concepts covered in Phase 0. Try answering these mentally or on paper before clicking to reveal the answers at the bottom!

---

## Part 1: How Python Runs
**Q1.** What is the difference between running code as a script versus the REPL?

**Q2.** If you execute `python my_file.py`, what is the value of the special variable `__name__` inside that file?

**Q3.** Why does Python throw a `NameError` if you call a function on line 5 but define it on line 20?

## Part 2: Variables and Types
**Q4.** What is the core difference between the `=` and `==` operators?

**Q5.** Name at least two *mutable* data types and two *immutable* data types in Python.

**Q6.** What does `bool("")` (an empty string) evaluate to, and why?

**Q7.** Consider this code:
```python
list_a = [1, 2]
list_b = list_a
list_a.append(3)
```
What is the current value of `list_b`? Why did this happen?

## Part 3: Functions
**Q8.** If a Python function completes without hitting a `return` statement, what value does it implicitly return?

**Q9.** What is the exact difference between an *argument* and a *parameter*?

**Q10.** What makes a function "pure"? Why are pure functions considered the golden standard?

---

<details>
<summary><b>Click to show answers</b></summary>

### Answers

**A1.** Script mode executes a saved file top-to-bottom. The REPL is an interactive shell (started by typing `python`) for quick experiments, and it does not save your work.

**A2.** `__name__` will equal `"__main__"`. This is often used (`if __name__ == "__main__":`) to determine if a file is being run directly or imported elsewhere.

**A3.** Because Python executes top-to-bottom. You must define a function or variable *before* you try to use it.

**A4.** `=` is used for **assignment** (e.g., tying a name to a value). `==` is used for **comparison** (e.g., checking if two values are equal).

**A5.** 
*   **Mutable** (can be changed in-place): `list`, `dict`, `set`.
*   **Immutable** (cannot be changed once created): `int`, `float`, `str`, `bool`, `tuple`.

**A6.** `False`. In Python, empty sequences like empty strings (`""`), empty lists (`[]`), and `0` are considered "falsy" values.

**A7.** `[1, 2, 3]`. Because `list_b = list_a` does not create a copy of the list. Instead, both variable names point to the exact same mutable list object in memory.

**A8.** `None`

**A9.** A **parameter** is the variable you define in the function signature (e.g., `def greet(name):` -> `name` is the parameter). An **argument** is the actual value you pass when calling it (e.g., `greet("Ada")` -> `"Ada"` is the argument).

**A10.** A pure function always returns the exact same output for the same input, and it has absolutely no side effects (it does not modify any variables or state outside of its own scope). They are predictable, easy to test, and prevent sneaky state-mutation bugs.

</details>
