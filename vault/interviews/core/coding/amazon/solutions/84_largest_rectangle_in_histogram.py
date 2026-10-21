"""LC 84 Largest Rectangle in Histogram -- increasing stack; popping fixes a bar's width. O(n)."""
from random import Random

# --- solution ---
def largest_rectangle_area(heights):
    stack = []                                   # indices with increasing heights
    best = 0
    for i, h in enumerate(heights + [0]):        # sentinel 0 flushes the stack at the end
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]        # this bar can't extend past i
            left = stack[-1] if stack else -1    # first smaller bar on the left
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
# --- end ---

def _brute(h):
    best = 0
    for i in range(len(h)):
        for j in range(i, len(h)):
            best = max(best, min(h[i:j + 1]) * (j - i + 1))
    return best

if __name__ == "__main__":
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([2, 4]) == 4
    assert largest_rectangle_area([]) == 0
    assert largest_rectangle_area([5]) == 5
    assert largest_rectangle_area([3, 3, 3]) == 9           # equal heights
    assert largest_rectangle_area([0, 0]) == 0
    rng = Random(9)
    for _ in range(300):
        h = [rng.randint(0, 6) for _ in range(rng.randint(0, 9))]
        assert largest_rectangle_area(list(h)) == _brute(h), h
    print("ok 84_largest_rectangle_in_histogram")
