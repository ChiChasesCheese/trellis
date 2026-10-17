"""LC 128 Longest Consecutive Sequence -- set + only start counting at sequence starts. O(n)."""
# --- solution ---
def longest_consecutive(nums):
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 in present:        # x is not the start of a run: skip, someone else counts it
            continue
        length = 1
        while x + length in present:
            length += 1
        best = max(best, length)
    return best
# --- end ---

if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([5]) == 1
    assert longest_consecutive([1, 1, 1]) == 1       # duplicates
    assert longest_consecutive([-2, -1, 0, 10]) == 3
    print("ok 128_longest_consecutive_sequence")
