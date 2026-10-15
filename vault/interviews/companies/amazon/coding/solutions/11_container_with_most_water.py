"""LC 11 Container With Most Water -- two pointers, move the shorter wall. Time O(n), space O(1)."""
from random import Random

# --- solution ---
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:      # the shorter wall limits the area; only moving it can help
            lo += 1
        else:
            hi -= 1
    return best
# --- end ---

def _brute(h):
    return max((j - i) * min(h[i], h[j]) for i in range(len(h)) for j in range(i + 1, len(h)))

if __name__ == "__main__":
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    assert max_area([4, 3, 2, 1, 4]) == 16
    assert max_area([1, 2, 1]) == 2
    rng = Random(4)
    for _ in range(300):
        h = [rng.randint(0, 9) for _ in range(rng.randint(2, 9))]
        assert max_area(h) == _brute(h), h
    print("ok 11_container_with_most_water")
