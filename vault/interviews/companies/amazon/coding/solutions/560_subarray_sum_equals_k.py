"""LC 560 Subarray Sum Equals K -- prefix sums + hash map of counts. Time O(n), space O(n)."""
from random import Random

# --- solution ---
def subarray_sum(nums, k):
    seen = {0: 1}                   # prefix sum 0 occurred once (the empty prefix)
    prefix = 0
    ans = 0
    for x in nums:
        prefix += x
        ans += seen.get(prefix - k, 0)   # earlier prefixes p with prefix - p == k
        seen[prefix] = seen.get(prefix, 0) + 1
    return ans
# --- end ---

def _brute(nums, k):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if sum(nums[i:j + 1]) == k)

if __name__ == "__main__":
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum([1, -1, 0], 0) == 3          # negatives and zeros: sliding window would fail
    assert subarray_sum([], 0) == 0
    assert subarray_sum([0, 0, 0], 0) == 6
    rng = Random(7)
    for _ in range(300):
        a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 9))]
        k = rng.randint(-4, 4)
        assert subarray_sum(a, k) == _brute(a, k), (a, k)
    print("ok 560_subarray_sum_equals_k")
