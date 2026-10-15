"""LC 4 Median of Two Sorted Arrays -- binary search the partition of the shorter array. Time O(log min(m, n))."""
from random import Random

# --- solution ---
def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a                                       # binary search over the shorter one
    m, n = len(a), len(b)
    half = (m + n + 1) // 2                               # size of the combined left part
    lo, hi = 0, m
    inf = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2                                # take i from a ...
        j = half - i                                      # ... and j from b into the left part
        a_left = a[i - 1] if i > 0 else -inf
        a_right = a[i] if i < m else inf
        b_left = b[j - 1] if j > 0 else -inf
        b_right = b[j] if j < n else inf
        if a_left > b_right:                              # took too many from a
            hi = i - 1
        elif b_left > a_right:                            # took too few from a
            lo = i + 1
        else:                                             # a valid split: left <= right on both sides
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
    raise ValueError("inputs must be sorted")
# --- end ---

def _brute(a, b):
    s = sorted(a + b)
    n = len(s)
    return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

if __name__ == "__main__":
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert find_median_sorted_arrays([], [1]) == 1.0
    assert find_median_sorted_arrays([0, 0], [0, 0]) == 0.0
    assert find_median_sorted_arrays([2], []) == 2.0
    rng = Random(14)
    for _ in range(500):
        a = sorted(rng.randint(-9, 9) for _ in range(rng.randint(0, 6)))
        b = sorted(rng.randint(-9, 9) for _ in range(rng.randint(0, 6)))
        if not a and not b:
            continue
        assert find_median_sorted_arrays(a, b) == _brute(a, b), (a, b)
    print("ok 4_median_of_two_sorted_arrays")
