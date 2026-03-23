import pytest
import time
import functools

# Phase 2 — Exercise 03: Decorators
# Run: pytest src/python_lab/phases/phase_2/exercises/test_03_decorators.py -v


def timer(fn):
    """Decorator: measure and print execution time.
    Must use @functools.wraps. Must return the original function's return value.

    @timer
    def slow():
        time.sleep(0.01)
        return 42

    slow()  -> prints "slow took X.XXXXs", returns 42
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def validate_positive(fn):
    """Decorator: raise ValueError if any numeric argument is <= 0.
    Only check arguments that are int or float. Ignore others.
    Must use @functools.wraps.

    @validate_positive
    def area(width: float, height: float) -> float:
        return width * height

    area(3, 4)   -> 12
    area(-1, 4)  -> ValueError
    area(0, 4)   -> ValueError
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if any(isinstance(x, (int, float)) and x <= 0 for x in args) or \
            any(isinstance(x, (int, float)) and x <= 0 for x in kwargs.values()):
            raise ValueError
        result = fn(*args, **kwargs)
        return result
    return wrapper


def repeat(n: int):
    """Decorator FACTORY: call the function n times, return the last result.
    Must use @functools.wraps.

    @repeat(3)
    def greet(name):
        print(f"Hello, {name}!")
        return name

    greet("Ada")  -> prints 3 times, returns "Ada"
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator


def once(fn):
    """Decorator: the function runs at most once. Subsequent calls return
    the cached result without calling fn again.
    Must use @functools.wraps.

    call_count = 0

    @once
    def setup():
        nonlocal call_count
        call_count += 1
        return "initialized"

    setup()  -> "initialized"  (runs)
    setup()  -> "initialized"  (cached, fn NOT called again)
    setup()  -> "initialized"  (cached)
    call_count == 1  ← only called once
    """
    has_run = False
    result = None
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal has_run, result
        if not has_run:
            result = fn(*args, **kwargs)
            has_run = True
        
        return result
    return wrapper


def add_method(method_name: str, method_fn):
    """Class decorator factory: add a method to the decorated class.

    def shout(self):
        return str(self).upper()

    @add_method("shout", shout)
    class Greeting:
        def __init__(self, text):
            self.text = text
        def __str__(self):
            return self.text

    Greeting("hello").shout()  -> "HELLO"
    """
    def decorator(cls):
        setattr(cls, method_name, method_fn)
        return cls
    return decorator


# ── tests ─────────────────────────────────────────────────────────

class TestTimer:
    def test_returns_value(self):
        @timer
        def fn():
            return 42
        assert fn() == 42

    def test_preserves_name(self):
        @timer
        def my_function():
            pass
        assert my_function.__name__ == "my_function"

    def test_preserves_docstring(self):
        @timer
        def documented():
            """My docstring."""
            pass
        assert documented.__doc__ == "My docstring."

    def test_prints_timing(self, capsys):
        @timer
        def fn():
            return 1
        fn()
        captured = capsys.readouterr()
        assert "fn" in captured.out
        assert "s" in captured.out   # some time measurement printed


class TestValidatePositive:
    def test_valid_args(self):
        @validate_positive
        def area(w, h):
            return w * h
        assert area(3, 4) == 12

    def test_negative_raises(self):
        @validate_positive
        def area(w, h):
            return w * h
        with pytest.raises(ValueError):
            area(-1, 4)

    def test_zero_raises(self):
        @validate_positive
        def fn(x):
            return x
        with pytest.raises(ValueError):
            fn(0)

    def test_preserves_name(self):
        @validate_positive
        def my_fn(x):
            pass
        assert my_fn.__name__ == "my_fn"

    def test_ignores_non_numeric(self):
        @validate_positive
        def fn(name, value):
            return f"{name}:{value}"
        assert fn("test", 5) == "test:5"


class TestRepeat:
    def test_calls_n_times(self):
        count = {"n": 0}

        @repeat(3)
        def fn():
            count["n"] += 1

        fn()
        assert count["n"] == 3

    def test_returns_last_result(self):
        @repeat(3)
        def fn():
            return 42
        assert fn() == 42

    def test_repeat_once(self):
        count = {"n": 0}

        @repeat(1)
        def fn():
            count["n"] += 1

        fn()
        assert count["n"] == 1

    def test_preserves_name(self):
        @repeat(2)
        def my_fn():
            pass
        assert my_fn.__name__ == "my_fn"

    def test_passes_args(self):
        results = []

        @repeat(3)
        def fn(x):
            results.append(x)

        fn(99)
        assert results == [99, 99, 99]


class TestOnce:
    def test_runs_once(self):
        count = {"n": 0}

        @once
        def fn():
            count["n"] += 1
            return "done"

        fn(); fn(); fn()
        assert count["n"] == 1

    def test_returns_cached_result(self):
        @once
        def fn():
            return 42

        assert fn() == 42
        assert fn() == 42

    def test_preserves_name(self):
        @once
        def my_fn():
            pass
        assert my_fn.__name__ == "my_fn"


class TestAddMethod:
    def test_adds_method(self):
        @add_method("shout", lambda self: str(self).upper())
        class Greeting:
            def __init__(self, text):
                self.text = text
            def __str__(self):
                return self.text

        g = Greeting("hello")
        assert g.shout() == "HELLO"

    def test_original_methods_intact(self):
        @add_method("double", lambda self: self.value * 2)
        class Box:
            def __init__(self, value):
                self.value = value
            def original(self):
                return self.value

        b = Box(10)
        assert b.original() == 10
        assert b.double() == 20

    def test_multiple_instances(self):
        @add_method("tag", lambda self: f"<{self.name}>")
        class Element:
            def __init__(self, name):
                self.name = name

        assert Element("div").tag() == "<div>"
        assert Element("span").tag() == "<span>"
