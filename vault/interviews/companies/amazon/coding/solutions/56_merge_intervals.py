"""LC 56 Merge Intervals -- sort by start, extend the last merged interval. Time O(n log n), space O(n)."""
# --- solution ---
def merge(intervals):
    merged = []
    for start, end in sorted(intervals):             # sorted() copies: input is not mutated
        if merged and start <= merged[-1][1]:        # overlaps (or touches) the last block
            merged[-1][1] = max(merged[-1][1], end)  # max: the new one may be fully inside
        else:
            merged.append([start, end])
    return merged
# --- end ---

if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]                 # touching counts as overlap
    assert merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]       # nested: max() matters
    assert merge([[5, 6], [1, 2]]) == [[1, 2], [5, 6]]         # unsorted input
    assert merge([]) == []
    assert merge([[1, 1]]) == [[1, 1]]
    print("ok 56_merge_intervals")
