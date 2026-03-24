import pytest
import time
from contextlib import contextmanager

# Phase 2 — Exercise 04: Context Managers
# Run: pytest src/python_lab/phases/phase_2/exercises/test_04_context_managers.py -v


class ManagedFile:
    """Context manager that opens a file and guarantees it's closed.

    with ManagedFile("/tmp/test.txt", "w") as f:
        f.write("hello")
    # file is closed here, even if an exception occurred

    Must implement __enter__ and __exit__.
    __enter__ returns the file object.
    __exit__ closes the file. Does not suppress exceptions.
    """
    def __init__(self, path: str, mode: str = "r"):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

        return False


class SuppressErrors:
    """Context manager that suppresses specified exception types silently.
    If an unexpected exception type occurs, it propagates normally.

    with SuppressErrors(ValueError, TypeError):
        raise ValueError("gone")   # suppressed
    # execution continues here

    with SuppressErrors(ValueError):
        raise TypeError("boom")    # NOT suppressed — propagates
    """
    def __init__(self, *exception_types):
        self.exception_types = exception_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exception_types):
            return True
        return False


class Timer:
    """Context manager that records elapsed time.
    After the block, `elapsed` attribute holds the duration in seconds.

    t = Timer()
    with t:
        time.sleep(0.01)
    assert t.elapsed >= 0.01
    """
    def __init__(self):
        self.elapsed: float = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        return False


@contextmanager
def temp_value(obj, attr: str, temp):
    """Context manager: temporarily set obj.attr to temp,
    then restore the original value when the block exits —
    even if an exception is raised.

    class Config:
        debug = False

    cfg = Config()
    with temp_value(cfg, "debug", True):
        assert cfg.debug is True
    assert cfg.debug is False   # restored

    Implement using @contextmanager and yield.
    """

    MISSING = object()

    original = getattr(obj, attr, MISSING)
    setattr(obj, attr, temp)

    try:
        yield
    finally:
        if original is not MISSING:
            setattr(obj, attr, original)
        else:
            delattr(obj, attr)


@contextmanager
def managed_list():
    """Context manager that provides a fresh list, then clears it on exit.
    Yield the list. After the block, clear it regardless of exceptions.

    with managed_list() as items:
        items.append(1)
        items.append(2)
        assert items == [1, 2]
    assert items == []   # cleared on exit
    """
    items = []
    try:
        yield items
    finally: 
        items.clear()


# ── tests ─────────────────────────────────────────────────────────

class TestManagedFile:
    def test_writes_and_reads(self, tmp_path):
        path = str(tmp_path / "test.txt")
        with ManagedFile(path, "w") as f:
            f.write("hello")
        with ManagedFile(path, "r") as f:
            assert f.read() == "hello"

    def test_file_closed_after_block(self, tmp_path):
        path = str(tmp_path / "test.txt")
        path_obj = tmp_path / "test.txt"
        path_obj.write_text("data")

        with ManagedFile(str(path_obj)) as f:
            pass
        assert f.closed

    def test_file_closed_on_exception(self, tmp_path):
        path = tmp_path / "test.txt"
        path.write_text("data")
        f_ref = None
        try:
            with ManagedFile(str(path)) as f:
                f_ref = f
                raise ValueError("boom")
        except ValueError:
            pass
        assert f_ref.closed

    def test_exception_propagates(self, tmp_path):
        path = tmp_path / "test.txt"
        path.write_text("")
        with pytest.raises(RuntimeError):
            with ManagedFile(str(path)):
                raise RuntimeError("should propagate")


class TestSuppressErrors:
    def test_suppresses_listed_exception(self):
        with SuppressErrors(ValueError):
            raise ValueError("gone")
        # No exception here means it was suppressed ✅

    def test_suppresses_multiple_types(self):
        with SuppressErrors(ValueError, TypeError):
            raise TypeError("gone")

    def test_propagates_unlisted_exception(self):
        with pytest.raises(RuntimeError):
            with SuppressErrors(ValueError):
                raise RuntimeError("not suppressed")

    def test_no_exception_is_fine(self):
        with SuppressErrors(ValueError):
            x = 1 + 1   # no exception — should work normally
        assert x == 2

    def test_returns_self_from_enter(self):
        ctx = SuppressErrors(ValueError)
        with ctx as result:
            pass
        assert result is ctx


class TestTimer:
    def test_elapsed_is_set(self):
        t = Timer()
        with t:
            time.sleep(0.02)
        assert t.elapsed >= 0.02

    def test_elapsed_starts_at_zero(self):
        t = Timer()
        assert t.elapsed == 0.0

    def test_elapsed_on_exception(self):
        t = Timer()
        try:
            with t:
                time.sleep(0.01)
                raise ValueError("boom")
        except ValueError:
            pass
        assert t.elapsed >= 0.01  # still recorded despite exception

    def test_enter_returns_self(self):
        t = Timer()
        with t as result:
            pass
        assert result is t


class TestTempValue:
    def test_sets_temp_value(self):
        class Obj:
            x = 10

        o = Obj()
        with temp_value(o, "x", 99):
            assert o.x == 99

    def test_restores_original(self):
        class Obj:
            pass
        o = Obj()
        o.value = "original"

        with temp_value(o, "value", "temporary"):
            assert o.value == "temporary"
        assert o.value == "original"

    def test_restores_on_exception(self):
        class Obj:
            pass
        o = Obj()
        o.flag = False

        try:
            with temp_value(o, "flag", True):
                assert o.flag is True
                raise RuntimeError("boom")
        except RuntimeError:
            pass

        assert o.flag is False   # restored even after exception


class TestManagedList:
    def test_provides_list(self):
        with managed_list() as items:
            assert isinstance(items, list)

    def test_usable_inside_block(self):
        with managed_list() as items:
            items.append(1)
            items.append(2)
            assert items == [1, 2]

    def test_cleared_on_exit(self):
        with managed_list() as items:
            items.append(1)
            items.append(2)
        assert items == []

    def test_cleared_on_exception(self):
        items_ref = None
        try:
            with managed_list() as items:
                items_ref = items
                items.append(99)
                raise ValueError("boom")
        except ValueError:
            pass
        assert items_ref == []
