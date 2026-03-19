import pytest
from itertools import islice

# Phase 2 — Exercise 02: Generators & Iterators
# Run: pytest src/python_lab/phases/phase_2/exercises/test_02_generators.py -v


def infinite_counter(start: int = 0, step: int = 1):
    """Yield integers forever starting at `start`, incrementing by `step`.

    list(islice(infinite_counter(), 5))         -> [0, 1, 2, 3, 4]
    list(islice(infinite_counter(10, 5), 4))    -> [10, 15, 20, 25]
    list(islice(infinite_counter(0, -1), 4))    -> [0, -1, -2, -3]
    """
    
    current = start
    while True:
        yield current
        current += step


def chunked(iterable, size: int):
    """Yield successive non-overlapping chunks of `size`.
    Last chunk may be smaller if items don't divide evenly.

    list(chunked([1,2,3,4,5], 2)) -> [[1,2], [3,4], [5]]
    list(chunked([1,2,3], 3))     -> [[1,2,3]]
    list(chunked([], 2))          -> []
    list(chunked([1], 5))         -> [[1]]
    """


    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    
    if chunk:
        yield chunk


def flatten_lazy(nested):
    """Lazily yield all items from an arbitrarily nested list.
    Uses yield from for the recursive case.

    list(flatten_lazy([1, [2, [3, 4]], 5])) -> [1, 2, 3, 4, 5]
    list(flatten_lazy([]))                  -> []
    list(flatten_lazy([[[42]]]))            -> [42]

    The difference from Phase 1 flatten(): this is a generator —
    it produces one item at a time without building intermediate lists.
    """
    
    for item in nested:
        if isinstance(item, list):
            yield from flatten_lazy(item)
        else:
            yield item


def take(n: int, iterable):
    """Yield the first n items from any iterable (including infinite generators).

    list(take(3, [10, 20, 30, 40, 50])) -> [10, 20, 30]
    list(take(3, infinite_counter()))   -> [0, 1, 2]
    list(take(0, [1, 2, 3]))           -> []
    """

    yield from islice(iterable, n)


def running_average(numbers):
    """Yield the running average after each new number.

    list(running_average([10, 20, 30])) -> [10.0, 15.0, 20.0]
    list(running_average([5]))          -> [5.0]
    list(running_average([]))           -> []
    """

    total = 0
    count = 0

    for number in numbers:
        count += 1
        total += number
        yield total / count


def pipeline(source, *transforms):
    """Apply a sequence of generator-based transforms to a source iterable.
    Each transform is a function: iterable -> iterable.

    double  = lambda it: (x * 2 for x in it)
    add_one = lambda it: (x + 1 for x in it)

    list(pipeline([1, 2, 3], double, add_one)) -> [3, 5, 7]
    list(pipeline([1, 2, 3]))                  -> [1, 2, 3]  (no transforms)
    """
    
    current = source

    for transform in transforms:
        current = transform(current)

    yield from current


# ── tests ─────────────────────────────────────────────────────────

class TestInfiniteCounter:
    def test_default_start(self):
        assert list(islice(infinite_counter(), 5)) == [0, 1, 2, 3, 4]

    def test_custom_start(self):
        assert list(islice(infinite_counter(10), 3)) == [10, 11, 12]

    def test_custom_step(self):
        assert list(islice(infinite_counter(0, 5), 4)) == [0, 5, 10, 15]

    def test_negative_step(self):
        assert list(islice(infinite_counter(0, -1), 4)) == [0, -1, -2, -3]

    def test_is_generator(self):
        import types
        assert isinstance(infinite_counter(), types.GeneratorType)


class TestChunked:
    def test_even_split(self):
        assert list(chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_leftover(self):
        assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_chunk_larger_than_list(self):
        assert list(chunked([1], 5)) == [[1]]

    def test_empty(self):
        assert list(chunked([], 3)) == []

    def test_exact_fit(self):
        assert list(chunked([1, 2, 3], 3)) == [[1, 2, 3]]

    def test_size_one(self):
        assert list(chunked([1, 2, 3], 1)) == [[1], [2], [3]]

    def test_works_on_generator_input(self):
        result = list(chunked(range(6), 2))
        assert result == [[0, 1], [2, 3], [4, 5]]


class TestFlattenLazy:
    def test_nested(self):
        assert list(flatten_lazy([1, [2, [3, 4]], 5])) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert list(flatten_lazy([])) == []

    def test_deeply_nested(self):
        assert list(flatten_lazy([[[42]]])) == [42]

    def test_already_flat(self):
        assert list(flatten_lazy([1, 2, 3])) == [1, 2, 3]

    def test_is_generator(self):
        import types
        assert isinstance(flatten_lazy([1, 2]), types.GeneratorType)


class TestTake:
    def test_basic(self):
        assert list(take(3, [10, 20, 30, 40, 50])) == [10, 20, 30]

    def test_from_infinite(self):
        assert list(take(4, infinite_counter())) == [0, 1, 2, 3]

    def test_zero(self):
        assert list(take(0, [1, 2, 3])) == []

    def test_more_than_available(self):
        assert list(take(10, [1, 2])) == [1, 2]


class TestRunningAverage:
    def test_basic(self):
        assert list(running_average([10, 20, 30])) == [10.0, 15.0, 20.0]

    def test_single(self):
        assert list(running_average([5])) == [5.0]

    def test_empty(self):
        assert list(running_average([])) == []

    def test_precision(self):
        result = list(running_average([1, 2, 3]))
        assert result == pytest.approx([1.0, 1.5, 2.0])


class TestPipeline:
    def test_single_transform(self):
        double = lambda it: (x * 2 for x in it)
        assert list(pipeline([1, 2, 3], double)) == [2, 4, 6]

    def test_chained_transforms(self):
        double  = lambda it: (x * 2 for x in it)
        add_one = lambda it: (x + 1 for x in it)
        assert list(pipeline([1, 2, 3], double, add_one)) == [3, 5, 7]

    def test_no_transforms(self):
        assert list(pipeline([1, 2, 3])) == [1, 2, 3]

    def test_with_filter_transform(self):
        evens = lambda it: (x for x in it if x % 2 == 0)
        assert list(pipeline([1, 2, 3, 4, 5], evens)) == [2, 4]

    def test_empty_source(self):
        double = lambda it: (x * 2 for x in it)
        assert list(pipeline([], double)) == []
