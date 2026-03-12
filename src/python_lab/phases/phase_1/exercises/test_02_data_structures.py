import pytest

class Stack:
    """LIFO stack backed by a list.
    pop() and peek() on empty stack must raise IndexError.
    """
    def __init__(self):
        self.items = []

    def push(self, item) -> None:
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def is_empty(self) -> bool:
        return not self.items

    def size(self) -> int:
        return len(self.items)


def two_sum(nums: list, target: int) -> list:
    """Return [i, j] where nums[i] + nums[j] == target. Exactly one solution.
    Solve in O(n) with a dict — not O(n²) with nested loops.

    two_sum([2, 7, 11, 15], 9) -> [0, 1]
    two_sum([3, 2, 4], 6)      -> [1, 2]
    two_sum([3, 3], 6)         -> [0, 1]
    """
    seen = {}

    for i, num in enumerate (nums):
        complement = target - num 
        if complement in seen:
            return [seen[complement], i]

        seen[num] = i 


def top_n_words(text: str, n: int) -> list:
    """Return the n most frequent words, sorted by frequency desc.
    Ties broken alphabetically. Case-insensitive.

    top_n_words("the cat sat on the mat the cat", 2) -> ["the", "cat"]
    top_n_words("a a b b c", 1)                      -> ["a"]
    top_n_words("", 3)                               -> []
    """
    words = text.lower().split()
    word_count = {}
    
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    sorted_words = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in sorted_words[:n]]


def deduplicate_ordered(items: list) -> list:
    """Remove duplicates preserving first-occurrence order.

    deduplicate_ordered([3,1,4,1,5,9,2,6,5,3]) -> [3,1,4,5,9,2,6]
    deduplicate_ordered([1,1,1])                -> [1]
    deduplicate_ordered([])                     -> []
    """
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)

    return result
        


def group_by(items: list, key_fn) -> dict:
    """Group items into a dict keyed by key_fn(item).

    group_by([1,2,3,4,5,6], lambda x: x % 2)
        -> {1: [1,3,5], 0: [2,4,6]}

    group_by(["apple","avocado","banana"], lambda s: s[0])
        -> {"a": ["apple","avocado"], "b": ["banana"]}
    """
    result = {}

    for item in items:
        group = key_fn(item)
        result[group] = result.get(group, [])
        result[group].append(item)
    
    return result

        

def longest_substring_no_repeat(s: str) -> int:
    """Return the length of the longest substring without repeating characters.
    Classic sliding window problem.

    longest_substring_no_repeat("abcabcbb") -> 3  ("abc")
    longest_substring_no_repeat("bbbbb")    -> 1  ("b")
    longest_substring_no_repeat("pwwkew")   -> 3  ("wke")
    longest_substring_no_repeat("")         -> 0

    Hint: use a dict to track the last-seen index of each character.
    """
    seen = {}
    start = 0
    max_len = 0

    for end, char in enumerate(s):
        if char in seen and seen[char] >= start:
            start = seen[char] + 1
        seen[char] = end
        max_len = max(max_len, end - start + 1)
    
    return max_len

# ── tests ─────────────────────────────────────────────────────────

class TestStack:
    @pytest.fixture
    def stack(self):
        return Stack()

    @pytest.fixture
    def loaded(self):
        s = Stack()
        s.push(1); s.push(2); s.push(3)
        return s

    def test_empty_on_init(self, stack):
        assert stack.is_empty() is True
        assert stack.size() == 0

    def test_push_and_size(self, stack):
        stack.push(10)
        assert stack.size() == 1

    def test_pop_lifo(self, loaded):
        assert loaded.pop() == 3
        assert loaded.pop() == 2
        assert loaded.pop() == 1

    def test_peek_no_removal(self, loaded):
        assert loaded.peek() == 3
        assert loaded.size() == 3

    def test_pop_empty_raises(self, stack):
        with pytest.raises(IndexError):
            stack.pop()

    def test_peek_empty_raises(self, stack):
        with pytest.raises(IndexError):
            stack.peek()

    def test_empty_after_all_pops(self, loaded):
        loaded.pop(); loaded.pop(); loaded.pop()
        assert loaded.is_empty() is True


class TestTwoSum:
    def test_basic(self):
        assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    def test_non_adjacent(self):
        assert two_sum([3, 2, 4], 6) == [1, 2]

    def test_duplicates(self):
        assert two_sum([3, 3], 6) == [0, 1]

    def test_returns_list_of_two(self):
        r = two_sum([1, 2, 3], 5)
        assert isinstance(r, list) and len(r) == 2


class TestTopNWords:
    def test_basic(self):
        assert top_n_words("the cat sat on the mat the cat", 2) == ["the", "cat"]

    def test_n_1(self):
        assert top_n_words("a a b b c", 1) == ["a"]

    def test_case_insensitive(self):
        assert top_n_words("The the THE", 1) == ["the"]

    def test_empty(self):
        assert top_n_words("", 3) == []


class TestDeduplicateOrdered:
    def test_basic(self):
        assert deduplicate_ordered([3,1,4,1,5,9,2,6,5,3]) == [3,1,4,5,9,2,6]

    def test_no_duplicates(self):
        assert deduplicate_ordered([1,2,3]) == [1,2,3]

    def test_empty(self):
        assert deduplicate_ordered([]) == []

    def test_all_same(self):
        assert deduplicate_ordered([1,1,1]) == [1]

    def test_preserves_first_occurrence(self):
        assert deduplicate_ordered([4,3,2,1,2,3,4]) == [4,3,2,1]


class TestGroupBy:
    def test_modulo(self):
        r = group_by([1,2,3,4,5,6], lambda x: x % 2)
        assert r[1] == [1,3,5]
        assert r[0] == [2,4,6]

    def test_first_letter(self):
        r = group_by(["apple","avocado","banana"], lambda s: s[0])
        assert r["a"] == ["apple","avocado"]
        assert r["b"] == ["banana"]

    def test_empty(self):
        assert group_by([], lambda x: x) == {}


class TestLongestSubstringNoRepeat:
    @pytest.mark.parametrize("s, expected", [
        ("abcabcbb", 3),
        ("bbbbb",    1),
        ("pwwkew",   3),
        ("",         0),
        ("abcdef",   6),
        ("dvdf",     3),
    ])
    def test_cases(self, s, expected):
        assert longest_substring_no_repeat(s) == expected
