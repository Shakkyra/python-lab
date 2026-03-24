import pytest
from typing import TypeVar, Generic, Protocol, runtime_checkable, Callable

# Phase 2 — Exercise 05: Protocols & Type Hints
# Run: pytest src/python_lab/phases/phase_2/exercises/test_05_protocols.py -v

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


# ── 1. Pair[T] — generic container ────────────────────────────────

class Pair(Generic[T]):
    """A pair of two values of the same type.

    p = Pair(1, 2)
    p.first    -> 1
    p.second   -> 2
    p.swap()   -> Pair(2, 1)
    p.map(fn)  -> Pair(fn(first), fn(second))
    p.to_list()-> [1, 2]

    Pair("a", "b").map(str.upper) -> Pair("A", "B")
    """
    
    def __init__(self, first: T, second: T):
        self.first = first
        self.second = second

    def swap(self) -> "Pair[T]":
        return Pair(self.second, self.first)

    def map(self, fn: Callable[[T], K]) -> "Pair[K]":
        return Pair(fn(self.first), fn(self.second))

    def to_list(self) -> list[T]:
        return [self.first, self.second]

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Pair) and 
            self.first == other.first and 
            self.second == other.second
        )

    def __repr__(self) -> str:
        return f"Pair({self.first!r}, {self.second!r})"


# ── 2. Drawable Protocol ──────────────────────────────────────────

@runtime_checkable
class Drawable(Protocol):
    """Any object with draw() and bounding_box() is Drawable.
    No inheritance required.
    """

    def draw(self) -> str: ...
    def bounding_box(self) -> tuple[int, int, int, int]: ...


def render_all(shapes: list['Drawable']) -> list[str]:
    """Call .draw() on each shape. Return list of draw() results.
    Works for ANY object that satisfies the Drawable protocol.

    render_all([Circle(0,0,5), Square(1,1,4)]) -> ["Circle...", "Square..."]
    """

    return [shape.draw() for shape in shapes]


# ── 3. Comparable Protocol ────────────────────────────────────────

@runtime_checkable
class Comparable(Protocol):
    """Any object with __lt__ and __eq__ is Comparable."""

    def __lt__(self, other) -> bool: ...
    def __eq__(self, other) -> bool: ...


def find_min(items: list['Comparable']) -> 'Comparable':
    """Return the minimum item using only __lt__ comparisons.
    Works for any list of Comparable objects.
    Raise ValueError if items is empty.

    find_min([3, 1, 4, 1, 5]) -> 1
    find_min(["banana", "apple", "cherry"]) -> "apple"
    find_min([]) -> ValueError
    """

    if not items:
        raise ValueError
    current_min = items[0]
    for item in items[1:]:
        if  item < current_min: 
            current_min = item
    return current_min 


# ── 4. InMemoryRepository[T] — generic storage ─────────────────

class InMemoryRepository(Generic[T]):
    """A generic key-value store.

    repo = InMemoryRepository()
    id1 = repo.save("Alice")     -> 1
    id2 = repo.save("Bob")       -> 2
    repo.get(1)                  -> "Alice"
    repo.get(99)                 -> None
    repo.delete(1)               -> True
    repo.get(1)                  -> None
    repo.list_all()              -> ["Bob"]
    repo.count()                 -> 1
    """

    def __init__(self):
        self._store: dict[int, T] = {}
        self._next_id = 1

    def save(self, item: T) -> int:
        """Store item, return its auto-assigned integer id."""

        id = self._next_id
        self._store[id] = item
        self._next_id += 1
        return id

    def get(self, id: int) -> "T | None":
        """Return item by id, or None if not found."""

        return self._store.get(id)

    def delete(self, id: int) -> bool:
        """Delete item by id. Return True if it existed, False if not."""

        if id in self._store:
            del self._store[id]
            return True
        return False

    def list_all(self) -> list[T]:
        """Return all stored items in insertion order."""

        return list(self._store.values())

    def count(self) -> int:
        """Return number of stored items."""

        return len(self._store)


# ── 5. Strategy via Protocol — preview of Phase 3 ─────────────────

class Formatter(Protocol):
    """Any object with a format(data) method is a Formatter."""

    def format(self, data: dict) -> str: ...


class JSONFormatter:
    """Format data as a JSON-like string."""

    def format(self, data: dict) -> str:
        # produce: {"key": "value", ...}
        pairs = [f'"{k}": "{v}"' for k, v in data.items()]
        joined = ", ".join(pairs)
        result = "{" + joined + "}"
        return result
            
class PlainFormatter:
    """Format data as plain key=value pairs separated by newlines."""

    def format(self, data: dict) -> str:
        # produce: "key=value\nkey2=value2"
        pairs = [f'{k}={v}' for k, v in data.items()]
        result = "\n".join(pairs)
        return result


def generate_report(data: dict, formatter: Formatter) -> str:
    """Generate a report using the provided formatter.
    Works with ANY formatter that satisfies the Formatter protocol.
    This is Strategy Pattern.
    """
    
    return formatter.format(data)


# ── tests ─────────────────────────────────────────────────────────

class TestPair:
    def test_first_second(self):
        p = Pair(1, 2)
        assert p.first == 1
        assert p.second == 2

    def test_swap(self):
        assert Pair(1, 2).swap() == Pair(2, 1)

    def test_map(self):
        assert Pair(2, 4).map(lambda x: x * 3) == Pair(6, 12)

    def test_map_strings(self):
        assert Pair("a", "b").map(str.upper) == Pair("A", "B")

    def test_to_list(self):
        assert Pair(10, 20).to_list() == [10, 20]

    def test_equality(self):
        assert Pair(1, 2) == Pair(1, 2)
        assert Pair(1, 2) != Pair(2, 1)

    def test_repr(self):
        assert repr(Pair(1, 2)) == "Pair(1, 2)"

    def test_generic_types(self):
        # Works for any type
        p_str = Pair("hello", "world")
        p_float = Pair(1.5, 2.5)
        assert p_str.to_list() == ["hello", "world"]
        assert p_float.swap() == Pair(2.5, 1.5)


class TestDrawable:
    @pytest.fixture
    def shapes(self):
        class CircleShape:
            def draw(self) -> str: return "Circle"
            def bounding_box(self): return (0, 0, 10, 10)

        class SquareShape:
            def draw(self) -> str: return "Square"
            def bounding_box(self): return (1, 1, 5, 5)

        return [CircleShape(), SquareShape()]

    def test_render_all(self, shapes):
        result = render_all(shapes)
        assert result == ["Circle", "Square"]

    def test_render_empty(self):
        assert render_all([]) == []

    def test_isinstance_check(self):
        class HasBoth:
            def draw(self) -> str: return "x"
            def bounding_box(self): return (0, 0, 1, 1)

        assert isinstance(HasBoth(), Drawable)

    def test_not_drawable_without_methods(self):
        assert not isinstance("just a string", Drawable)
        assert not isinstance(42, Drawable)


class TestFindMin:
    def test_integers(self):
        assert find_min([3, 1, 4, 1, 5]) == 1

    def test_strings(self):
        assert find_min(["banana", "apple", "cherry"]) == "apple"

    def test_single_item(self):
        assert find_min([42]) == 42

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            find_min([])

    def test_already_sorted(self):
        assert find_min([1, 2, 3]) == 1

    def test_reverse_sorted(self):
        assert find_min([5, 4, 3, 2, 1]) == 1


class TestInMemoryRepository:
    @pytest.fixture
    def repo(self):
        return InMemoryRepository()

    def test_save_returns_id(self, repo):
        assert repo.save("Alice") == 1
        assert repo.save("Bob") == 2

    def test_get_by_id(self, repo):
        id = repo.save("Carol")
        assert repo.get(id) == "Carol"

    def test_get_missing_returns_none(self, repo):
        assert repo.get(999) is None

    def test_delete_existing(self, repo):
        id = repo.save("Dave")
        assert repo.delete(id) is True
        assert repo.get(id) is None

    def test_delete_missing(self, repo):
        assert repo.delete(999) is False

    def test_list_all(self, repo):
        repo.save("Alice")
        repo.save("Bob")
        assert repo.list_all() == ["Alice", "Bob"]

    def test_list_all_empty(self, repo):
        assert repo.list_all() == []

    def test_count(self, repo):
        repo.save("Alice")
        repo.save("Bob")
        assert repo.count() == 2

    def test_count_after_delete(self, repo):
        id = repo.save("Alice")
        repo.save("Bob")
        repo.delete(id)
        assert repo.count() == 1


class TestFormatterStrategy:
    @pytest.fixture
    def data(self):
        return {"name": "Ada", "role": "engineer"}

    def test_json_formatter(self, data):
        result = JSONFormatter().format(data)
        assert '"name"' in result
        assert '"Ada"' in result

    def test_plain_formatter(self, data):
        result = PlainFormatter().format(data)
        assert "name=Ada" in result
        assert "role=engineer" in result

    def test_generate_report_json(self, data):
        result = generate_report(data, JSONFormatter())
        assert "Ada" in result

    def test_generate_report_plain(self, data):
        result = generate_report(data, PlainFormatter())
        assert "Ada" in result

    def test_swappable_formatters(self, data):
        # Same data, different formatters — different output
        json_out = generate_report(data, JSONFormatter())
        plain_out = generate_report(data, PlainFormatter())
        assert json_out != plain_out

    def test_formatter_protocol_satisfied(self):
        # Any object with .format() satisfies Formatter
        class CustomFormatter:
            def format(self, data: dict) -> str:
                return "custom"

        result = generate_report({"x": 1}, CustomFormatter())
        assert result == "custom"
