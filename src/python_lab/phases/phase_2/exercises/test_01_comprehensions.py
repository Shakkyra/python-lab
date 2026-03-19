import pytest

# Phase 2 — Exercise 01: Comprehensions
# Run: pytest src/python_lab/phases/phase_2/exercises/test_01_comprehensions.py -v


def squares_of_evens(numbers: list) -> list:
    """Return a list of squares of even numbers only.

    squares_of_evens([1, 2, 3, 4, 5, 6]) -> [4, 16, 36]
    squares_of_evens([1, 3, 5])           -> []
    squares_of_evens([])                  -> []

    Constraint: one-line list comprehension.
    """

    return [n ** 2 for n in numbers if n % 2 == 0]


def word_lengths(sentence: str) -> dict:
    """Return a dict mapping each word to its length.

    word_lengths("hello world")   -> {"hello": 5, "world": 5}
    word_lengths("hi")            -> {"hi": 2}
    word_lengths("")              -> {}

    Constraint: dict comprehension.
    """
    
    return {word: len(word) for word in sentence.split()}


def flatten_matrix(matrix: list[list]) -> list:
    """Flatten a 2D list into a 1D list.

    flatten_matrix([[1, 2], [3, 4], [5, 6]]) -> [1, 2, 3, 4, 5, 6]
    flatten_matrix([[1]])                     -> [1]
    flatten_matrix([])                        -> []

    Constraint: nested list comprehension — no loops, no flatten().
    """
    
    return [n for row in matrix for n in row]


def unique_chars(text: str) -> set:
    """Return the set of unique characters in text (excluding spaces).

    unique_chars("hello world") -> {"h","e","l","o","w","r","d"}
    unique_chars("aaa")         -> {"a"}
    unique_chars("")            -> set()

    Constraint: set comprehension.
    """

    return {char for char in text if not char.isspace()}


def invert_dict(d: dict) -> dict:
    """Swap keys and values. Assume values are unique.

    invert_dict({"a": 1, "b": 2, "c": 3}) -> {1: "a", 2: "b", 3: "c"}
    invert_dict({})                        -> {}

    Constraint: dict comprehension.
    """

    return {v: k for k, v in d.items()}


def top_scoring(scores: dict, threshold: int) -> list:
    """Return names of people who scored above threshold, sorted alphabetically.

    scores = {"Alice": 90, "Bob": 70, "Carol": 85}
    top_scoring(scores, 80) -> ["Alice", "Carol"]
    top_scoring(scores, 95) -> []

    Constraint: list comprehension + sorted().
    """

    return sorted([name for name, score in scores.items() if score > threshold])


def pipeline(numbers: list) -> int:
    """Chain of transformations using generator expressions (no intermediate lists):
    1. Filter: keep only positive numbers
    2. Transform: square each one
    3. Filter: keep only those divisible by 4
    4. Aggregate: return the sum

    pipeline([1, -2, 3, -4, 5, 6]) -> 1² + 3² + 5² + 6² filtered by %4==0
                                    -> keep: 36  (6²=36, 36%4==0)
                                              4  (2²=4  but 2 is negative, skip)
    pipeline([2, 4, 6])             -> 4 + 16 + 36 = 56
    pipeline([-1, -2])              -> 0

    Constraint: generator expressions chained into sum(). No lists created.
    """

    return sum(sq for sq in (n**2 for n in numbers if n > 0) if sq % 4 == 0)


# ── tests ─────────────────────────────────────────────────────────

class TestSquaresOfEvens:
    @pytest.mark.parametrize("numbers, expected", [
        ([1, 2, 3, 4, 5, 6], [4, 16, 36]),
        ([1, 3, 5],           []),
        ([2],                 [4]),
        ([],                  []),
    ])
    def test_cases(self, numbers, expected):
        assert squares_of_evens(numbers) == expected


class TestWordLengths:
    def test_basic(self):
        assert word_lengths("hello world") == {"hello": 5, "world": 5}

    def test_single_word(self):
        assert word_lengths("hi") == {"hi": 2}

    def test_empty(self):
        assert word_lengths("") == {}

    def test_repeated_word(self):
        # last occurrence wins (or first — just be consistent)
        result = word_lengths("hi hi")
        assert result == {"hi": 2}


class TestFlattenMatrix:
    def test_basic(self):
        assert flatten_matrix([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]

    def test_single_row(self):
        assert flatten_matrix([[1, 2, 3]]) == [1, 2, 3]

    def test_single_element(self):
        assert flatten_matrix([[1]]) == [1]

    def test_empty(self):
        assert flatten_matrix([]) == []

    def test_preserves_order(self):
        assert flatten_matrix([[3, 1], [4, 1], [5, 9]]) == [3, 1, 4, 1, 5, 9]


class TestUniqueChars:
    def test_basic(self):
        assert unique_chars("hello") == {"h", "e", "l", "o"}

    def test_excludes_spaces(self):
        result = unique_chars("hi there")
        assert " " not in result

    def test_empty(self):
        assert unique_chars("") == set()

    def test_all_same(self):
        assert unique_chars("aaa") == {"a"}


class TestInvertDict:
    def test_basic(self):
        assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_empty(self):
        assert invert_dict({}) == {}

    def test_roundtrip(self):
        original = {"x": 10, "y": 20}
        assert invert_dict(invert_dict(original)) == original


class TestTopScoring:
    @pytest.fixture
    def scores(self):
        return {"Alice": 90, "Bob": 70, "Carol": 85, "Dave": 95}

    def test_basic(self, scores):
        assert top_scoring(scores, 80) == ["Alice", "Carol", "Dave"]

    def test_none_qualify(self, scores):
        assert top_scoring(scores, 99) == []

    def test_all_qualify(self, scores):
        assert top_scoring(scores, 0) == ["Alice", "Bob", "Carol", "Dave"]

    def test_sorted_alphabetically(self, scores):
        result = top_scoring(scores, 80)
        assert result == sorted(result)


class TestPipeline:
    def test_basic(self):
        # positives: [2, 4, 6] → squares: [4, 16, 36] → div by 4: [4, 16, 36] → sum=56
        assert pipeline([2, 4, 6]) == 56

    def test_filters_negatives(self):
        assert pipeline([-1, -2, -3]) == 0

    def test_filters_not_divisible(self):
        # 3² = 9 — not divisible by 4 → excluded
        assert pipeline([3]) == 0

    def test_mixed(self):
        # positives: [1,3,5,6], squares: [1,9,25,36], div4: [36] → 36
        assert pipeline([1, -2, 3, -4, 5, 6]) == 36

    def test_empty(self):
        assert pipeline([]) == 0
