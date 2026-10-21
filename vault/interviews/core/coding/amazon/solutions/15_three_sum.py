"""LC 15 3Sum -- sort, fix one, two pointers on the rest, skip duplicates. Time O(n^2), space O(1) extra."""
from itertools import combinations
from random import Random

# --- solution ---
def three_sum(nums):
    nums = sorted(nums)
    out = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:     # same first number -> same triples
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # skip duplicate second numbers
                    lo += 1
    return out
# --- end ---

def _brute(nums):
    return sorted({tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0})

if __name__ == "__main__":
    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]            # duplicates must not repeat the triple
    assert three_sum([]) == []
    rng = Random(3)
    for _ in range(300):
        a = [rng.randint(-4, 4) for _ in range(rng.randint(0, 9))]
        assert sorted(map(tuple, three_sum(a))) == _brute(a), a
    print("ok 15_three_sum")
