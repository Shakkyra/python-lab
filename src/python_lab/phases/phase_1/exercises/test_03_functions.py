import pytest

# Phase 1 — Functions
# Run: pytest phases/phase_1/test_03_functions.py -v
#
# Functions as first-class values: closures, higher-order functions,
# decorators, memoization, composition.
# These patterns appear directly inside Strategy and other design patterns.


def make_counter(start=0):
    """Return a counter function. Each call increments and returns the count.
    State lives in the closure — no class, no global variable.

    counter = make_counter()
    counter()  -> 1
    counter()  -> 2

    counter_from_10 = make_counter(start=10)
    counter_from_10()  -> 11
    """

    count = start
    def counter():
        nonlocal count 
        count += 1
        return count

    return counter


def memoize(fn):
    """Decorator: cache results by argument. Re-use on cache hit.
    Implement from scratch — no functools.lru_cache.

    @memoize
    def square(n):
        return n * n

    square(5)  -> 25  (computed)
    square(5)  -> 25  (from cache, fn not called again)
    """
    cache = {}

    def wrapper(*args):
        if args in cache: 
            return cache[args]

        result = fn(*args)
        cache[args] = result
        return result
    
    return wrapper


def compose(*fns):
    """Return a function that applies fns right-to-left.

    f = compose(double, add_one, square)  # double(add_one(square(x)))
    f(3) -> double(add_one(9)) -> double(10) -> 20

    compose() with no args -> identity function.
    """
    def composed(value):
        for fn in reversed(fns):
            value = fn(value)
        
        return value 
    
    return composed


def retry(fn, times, exceptions=(Exception,)):
    """Return a wrapper that retries fn up to `times` times on exception.
    Re-raises last exception if all attempts fail.
    Only retries exceptions listed in `exceptions`.

    retry(flaky_fn, 3)()  -> succeeds on 3rd attempt
    retry(always_fails, 3)()  -> raises after 3 attempts
    """
    def wrapper(*args, **kwargs):
        last_error = None 
        for attempt in range(1, times + 1):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                last_error = e
                print(f"  attempt {attempt} failed: {e}")
        raise last_error
    return wrapper




def partial(fn, *partial_args, **partial_kwargs):
    """Return fn with some arguments pre-filled.
    Implement from scratch — no functools.partial.

    add5 = partial(lambda a, b, c: a+b+c, 5)
    add5(3, 2)  -> 10
    """
    def wrapper(*args, **kwargs):
        all_args = partial_args + args
        all_kwargs = {**partial_kwargs, **kwargs}
        return fn(*all_args, **all_kwargs)
    return wrapper


def pipe(value, *fns):
    """Apply fns left-to-right to value (opposite of compose).

    pipe(3, square, add_one, double)  -> double(add_one(square(3)))
                                      -> double(add_one(9))
                                      -> double(10)
                                      -> 20

    pipe(5)  -> 5   (no functions = identity)
    """
    for fn in fns:
        value = fn(value)
    return value


# ── tests ─────────────────────────────────────────────────────────

class TestMakeCounter:
    def test_counts_from_one(self):
        c = make_counter()
        assert c() == 1
        assert c() == 2
        assert c() == 3

    def test_custom_start(self):
        c = make_counter(start=10)
        assert c() == 11
        assert c() == 12

    def test_independent_counters(self):
        a = make_counter()
        b = make_counter()
        a(); a(); a()
        assert b() == 1


class TestMemoize:
    def test_correct_result(self):
        @memoize
        def square(n): return n * n
        assert square(5) == 25

    def test_caches_on_repeated_call(self):
        calls = {"n": 0}

        @memoize
        def fn(x):
            calls["n"] += 1
            return x * 2

        fn(4); fn(4); fn(4)
        assert calls["n"] == 1

    def test_different_args_not_shared(self):
        calls = {"n": 0}

        @memoize
        def fn(x):
            calls["n"] += 1
            return x

        fn(1); fn(2); fn(3)
        assert calls["n"] == 3

    def test_result_consistent(self):
        @memoize
        def fn(n): return n ** 2
        assert fn(7) == fn(7) == 49


class TestCompose:
    def setup_method(self):
        self.double  = lambda x: x * 2
        self.add_one = lambda x: x + 1
        self.square  = lambda x: x ** 2

    def test_three_functions(self):
        f = compose(self.double, self.add_one, self.square)
        assert f(3) == 20  

    def test_two_functions(self):
        f = compose(str, lambda x: x + 1)
        assert f(4) == "5"

    def test_single_function(self):
        f = compose(self.double)
        assert f(4) == 8

    def test_no_functions_is_identity(self):
        f = compose()
        assert f(42) == 42


class TestRetry:
    def test_succeeds_first_try(self):
        assert retry(lambda: "ok", 3)() == "ok"

    def test_succeeds_after_failures(self):
        state = {"n": 0}

        def flaky():
            state["n"] += 1
            if state["n"] < 3:
                raise ValueError("not yet")
            return "ok"

        assert retry(flaky, 3)() == "ok"

    def test_reraises_after_exhausting(self):
        with pytest.raises(ValueError, match="nope"):
            retry(lambda: (_ for _ in ()).throw(ValueError("nope")), 3)()

    def test_only_catches_specified_exceptions(self):
        def raises_type_error():
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            retry(raises_type_error, 5, exceptions=(ValueError,))()


class TestPartial:
    def test_pre_fill_first_arg(self):
        add = lambda a, b, c: a + b + c
        add5 = partial(add, 5)
        assert add5(3, 2) == 10

    def test_keyword_args(self):
        greet = lambda name, greeting="Hello": f"{greeting}, {name}!"
        hi = partial(greet, greeting="Hi")
        assert hi("Ada") == "Hi, Ada!"

    def test_no_partial_args(self):
        fn = partial(lambda x: x * 2)
        assert fn(5) == 10


class TestPipe:
    def setup_method(self):
        self.double  = lambda x: x * 2
        self.add_one = lambda x: x + 1
        self.square  = lambda x: x ** 2

    def test_left_to_right(self):
        result = pipe(3, self.square, self.add_one, self.double)
        assert result == 20  

    def test_no_functions_is_identity(self):
        assert pipe(42) == 42

    def test_single_function(self):
        assert pipe(5, self.double) == 10

    def test_string_pipeline(self):
        result = pipe("  hello world  ", str.strip, str.title, str.split)
        assert result == ["Hello", "World"]

