"""LC 435 Non-overlapping Intervals -- greedy: sort by END, keep the interval that ends first. O(n log n)."""
from itertools import combinations
from random import Random

# --- solution ---
def erase_overlap_intervals(intervals):
    intervals = sorted(intervals, key=lambda iv: iv[1])   # earliest end first leaves most room
    kept = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:        # touching ([1,2],[2,3]) is NOT an overlap here
            kept += 1
            last_end = end
    return len(intervals) - kept
# --- end ---

def _brute(iv):
    n = len(iv)
    for keep in range(n, -1, -1):
        for comb in combinations(iv, keep):
            c = sorted(comb)
            if all(c[i][1] <= c[i + 1][0] for i in range(len(c) - 1)):
                return n - keep
    return n

if __name__ == "__main__":
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
    assert erase_overlap_intervals([]) == 0
    assert erase_overlap_intervals([[1, 100], [11, 22], [1, 11], [2, 12]]) == 2
    rng = Random(6)
    for _ in range(300):
        iv = []
        for _ in range(rng.randint(0, 6)):
            a = rng.randint(0, 6)
            iv.append([a, a + rng.randint(1, 4)])
        assert erase_overlap_intervals(iv) == _brute(iv), iv
    print("ok 435_non_overlapping_intervals")
