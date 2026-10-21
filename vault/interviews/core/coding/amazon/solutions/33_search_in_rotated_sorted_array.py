"""LC 33 Search in Rotated Sorted Array -- binary search; one half is always sorted. Time O(log n)."""
from random import Random

# --- solution ---
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                       # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                           # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
# --- end ---

if __name__ == "__main__":
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search([1], 0) == -1
    assert search([1], 1) == 0
    assert search([3, 1], 1) == 1                       # two elements: nums[lo] <= nums[mid] needs the "="
    rng = Random(13)
    for _ in range(300):
        base = sorted(rng.sample(range(-20, 20), rng.randint(1, 10)))
        k = rng.randint(0, len(base) - 1)
        a = base[k:] + base[:k]
        t = rng.randint(-21, 21)
        want = a.index(t) if t in a else -1
        assert search(a, t) == want, (a, t)
    print("ok 33_search_in_rotated_sorted_array")
