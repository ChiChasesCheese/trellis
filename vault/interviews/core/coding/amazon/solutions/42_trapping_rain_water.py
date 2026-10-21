"""LC 42 Trapping Rain Water -- two pointers with running left/right max. Time O(n), space O(1)."""
from random import Random

# --- solution ---
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            # the right wall is already taller than height[left], so left_max alone decides this cell
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
# --- end ---

def _brute(h):
    return sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))

if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0
    assert trap([3]) == 0
    assert trap([1, 2, 3, 4]) == 0          # monotone: no bowl
    rng = Random(2)
    for _ in range(300):
        h = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        assert trap(h) == _brute(h), h
    print("ok 42_trapping_rain_water")
