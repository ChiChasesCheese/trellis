"""LC 53 Maximum Subarray -- Kadane: best sum ending here = max(x, prev + x). Time O(n), space O(1)."""
from random import Random

# --- solution ---
def max_sub_array(nums):
    ending_here = best = nums[0]
    for x in nums[1:]:
        ending_here = max(x, ending_here + x)      # extend the previous run, or restart at x
        best = max(best, ending_here)
    return best
# --- end ---

def _brute(a):
    return max(sum(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a)))

if __name__ == "__main__":
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_sub_array([1]) == 1
    assert max_sub_array([5, 4, -1, 7, 8]) == 23
    assert max_sub_array([-3, -1, -2]) == -1         # all negative: init with nums[0], not 0
    rng = Random(17)
    for _ in range(300):
        a = [rng.randint(-5, 5) for _ in range(rng.randint(1, 9))]
        assert max_sub_array(a) == _brute(a), a
    print("ok 53_maximum_subarray")
