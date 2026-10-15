"""LC 1 Two Sum -- hash map of value -> index. Time O(n), space O(n)."""
# --- solution ---
def two_sum(nums, target):
    seen = {}                       # value -> index where we saw it
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:            # look BEFORE inserting x: no element is used twice
            return [seen[need], i]
        seen[x] = i
    return []
# --- end ---

if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]          # duplicates
    assert two_sum([1, 2], 10) == []             # no answer
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
    print("ok 1_two_sum")
