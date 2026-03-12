import pytest

def flatten(nested: list) -> list:
    """Recursively flatten a nested list to any depth.

    flatten([1, [2, [3, 4]], 5])     -> [1, 2, 3, 4, 5]
    flatten([[1, 2], [3, [4, [5]]]]) -> [1, 2, 3, 4, 5]
    flatten([])                      -> []

    Constraint: recursive — no libraries.
    """

    result = []

    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)

    return result



def is_balanced(s: str) -> bool:
    """Return True if all bracket pairs in s are properly balanced.
    Bracket types: () [] {}

    is_balanced("({[]})")  -> True
    is_balanced("([)]")    -> False
    is_balanced("")        -> True

    Hint: use a list as a stack.
    """
    
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ']})':
            if not stack:
                return False

            top = stack.pop()
            expected = matching[char]

            if top != expected:
                return False

    return not stack


def run_length_encode(s: str) -> list:
    """Encode consecutive repeated characters as (char, count) tuples.

    run_length_encode("aaabbc") -> [("a", 3), ("b", 2), ("c", 1)]
    run_length_encode("abcd")   -> [("a",1), ("b",1), ("c",1), ("d",1)]
    run_length_encode("")       -> []
    """

    if not s:
        return []

    result = []
    current_char = s[0]
    count = 1
    
    for char in s[1:]:
        if char == current_char:
            count += 1
        else:
            result.append((current_char, count))
            current_char = char
            count = 1

    result.append((current_char, count))
    return result



def group_consecutive(nums: list) -> list:
    """Group sorted consecutive integers into [start, end] ranges.
    Single elements become [n, n]. Input is sorted, no duplicates.

    group_consecutive([1, 2, 3, 6, 7, 9]) -> [[1, 3], [6, 7], [9, 9]]
    group_consecutive([1, 3, 5])           -> [[1,1], [3,3], [5,5]]
    group_consecutive([])                  -> []
    """

    result = []

    if not nums:
        return result

    start_num = end_num = nums[0]

    for n in nums[1:]:
        consecutive = n == end_num + 1
        if consecutive:
            end_num = n
        else:
            result.append([start_num, end_num])
            start_num = n
            end_num = n

    result.append([start_num, end_num])
    return result




def max_sliding_window(nums: list, k: int) -> list:
    """Return the max of each sliding window of size k.

    max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) -> [3, 3, 5, 5, 6, 7]
    max_sliding_window([4, 3, 2, 1], 2)               -> [4, 3, 2]
    """
    result = []

    for i in range(len(nums) - k + 1):
        window = nums[i:i+k]
        result.append(max(window))

    return result


def count_islands(grid: list) -> int:
    """Count connected groups of 1s in a binary grid (4-directional).
    Modifying the grid in-place to mark visited cells is fine.

    grid = [
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
    ]
    count_islands(grid) -> 2

    Hint: DFS from each unvisited 1.
    """
    
    counter = 0
    rows = len(grid)
    columns = len(grid[0])

    def dfs(row: int, col: int):
        if row < 0 or row >= rows:
            return
        if col < 0 or col >= columns:
            return

        if grid[row][col] != 1:
            return
        
        grid[row][col] = 0

        dfs(row - 1, col)
        dfs(row + 1, col)
        dfs(row, col - 1)
        dfs(row, col + 1)


    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == 1:
                counter += 1
                dfs(row, column)
    return counter
        
# ── tests ─────────────────────────────────────────────────────────

class TestFlatten:
    def test_nested(self):
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_empty(self):
        assert flatten([]) == []

    def test_deeply_nested(self):
        assert flatten([[[[[42]]]]]) == [42]

    def test_mixed_depth(self):
        assert flatten([[1, 2], [3, [4, [5]]]]) == [1, 2, 3, 4, 5]


class TestIsBalanced:
    @pytest.mark.parametrize("s", ["([]{})", "", "{[()]}", "()", "[]"])
    def test_balanced(self, s):
        assert is_balanced(s) is True

    @pytest.mark.parametrize("s", ["([)]", "(((", "{[}", ")", "(()"])
    def test_unbalanced(self, s):
        assert is_balanced(s) is False


class TestRunLengthEncode:
    def test_basic(self):
        assert run_length_encode("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]

    def test_no_repeats(self):
        assert run_length_encode("abcd") == [("a",1), ("b",1), ("c",1), ("d",1)]

    def test_empty(self):
        assert run_length_encode("") == []

    def test_all_same(self):
        assert run_length_encode("aaaa") == [("a", 4)]


class TestGroupConsecutive:
    def test_mixed(self):
        assert group_consecutive([1, 2, 3, 6, 7, 9]) == [[1, 3], [6, 7], [9, 9]]

    def test_all_singles(self):
        assert group_consecutive([1, 3, 5]) == [[1,1], [3,3], [5,5]]

    def test_single_range(self):
        assert group_consecutive([1, 2, 3, 4]) == [[1, 4]]

    def test_empty(self):
        assert group_consecutive([]) == []


class TestMaxSlidingWindow:
    def test_example(self):
        assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]

    def test_window_size_2(self):
        assert max_sliding_window([4, 3, 2, 1], 2) == [4, 3, 2]

    def test_window_equals_length(self):
        assert max_sliding_window([1, 2, 3], 3) == [3]

    def test_negatives(self):
        assert max_sliding_window([-1, -3, -5, -2], 2) == [-1, -3, -2]


class TestCountIslands:
    def test_two_islands(self):
        grid = [[1,1,0,0],[1,0,0,1],[0,0,0,1],[0,0,0,0]]
        assert count_islands(grid) == 2

    def test_one_island(self):
        assert count_islands([[1,1],[1,1]]) == 1

    def test_no_islands(self):
        assert count_islands([[0,0],[0,0]]) == 0

    def test_diagonal_not_connected(self):
        assert count_islands([[1,0],[0,1]]) == 2

    def test_single_cell(self):
        assert count_islands([[1]]) == 1
        assert count_islands([[0]]) == 0
