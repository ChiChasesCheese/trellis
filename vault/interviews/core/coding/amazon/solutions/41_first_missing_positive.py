"""LC 41 First Missing Positive -- use the array itself as a hash set (cyclic placement). Time O(n), space O(1)."""
from random import Random

# --- solution ---
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        # put value v at index v-1, as long as v is in range and not already there
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def first_missing_positive_set(nums):          # O(n) space baseline; say this one first
    present = set(nums)
    ans = 1
    while ans in present:
        ans += 1
    return ans
# --- end ---

if __name__ == "__main__":
    for f in (first_missing_positive, first_missing_positive_set):
        assert f([1, 2, 0]) == 3
        assert f([3, 4, -1, 1]) == 2
        assert f([7, 8, 9, 11, 12]) == 1
        assert f([1]) == 2
        assert f([]) == 1
        assert f([1, 1]) == 2                   # duplicates: swap loop must not spin forever
        rng = Random(24)
        for _ in range(300):
            a = [rng.randint(-2, 8) for _ in range(rng.randint(0, 8))]
            assert f(list(a)) == first_missing_positive_set(a), a
    print("ok 41_first_missing_positive")
