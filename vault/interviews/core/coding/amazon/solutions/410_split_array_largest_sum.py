"""LC 410 Split Array Largest Sum -- binary search the answer + greedy feasibility. Time O(n log sum)."""
from itertools import combinations
from random import Random

# --- solution ---
def split_array(nums, k):
    def pieces_needed(limit):                     # greedy: pack as much as possible into each piece
        pieces, cur = 1, 0
        for x in nums:
            if cur + x > limit:
                pieces += 1
                cur = 0
            cur += x
        return pieces

    lo, hi = max(nums), sum(nums)                 # limit can't be below the biggest item; sum always works
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(mid) <= k:               # feasible with <= k pieces (fewer can always be split more)
            hi = mid
        else:
            lo = mid + 1
    return lo
# --- end ---

def _brute(nums, k):
    n = len(nums)
    best = float("inf")
    for cuts in combinations(range(1, n), k - 1):
        bounds = (0,) + cuts + (n,)
        best = min(best, max(sum(nums[bounds[i]:bounds[i + 1]]) for i in range(k)))
    return best

if __name__ == "__main__":
    assert split_array([7, 2, 5, 10, 8], 2) == 18
    assert split_array([1, 2, 3, 4, 5], 2) == 9
    assert split_array([1, 4, 4], 3) == 4
    assert split_array([5], 1) == 5
    rng = Random(15)
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(1, 7))]
        k = rng.randint(1, len(a))
        assert split_array(a, k) == _brute(a, k), (a, k)
    print("ok 410_split_array_largest_sum")
