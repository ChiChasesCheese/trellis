"""LC 875 Koko Eating Bananas -- binary search on the answer (speed). Time O(n log max), space O(1)."""
from random import Random

# --- solution ---
def min_eating_speed(piles, h):
    def hours(speed):
        return sum((p + speed - 1) // speed for p in piles)    # ceil(p / speed) without floats

    lo, hi = 1, max(piles)                  # answer is in [1, max]; speed max always works (if h >= len)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:                 # feasible: try slower
            hi = mid
        else:                               # too slow: must go faster
            lo = mid + 1
    return lo
# --- end ---

def _brute(piles, h):
    for s in range(1, max(piles) + 1):
        if sum(-(-p // s) for p in piles) <= h:
            return s

if __name__ == "__main__":
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([1], 1) == 1
    assert min_eating_speed([10 ** 9], 2) == 5 * 10 ** 8
    rng = Random(12)
    for _ in range(300):
        p = [rng.randint(1, 12) for _ in range(rng.randint(1, 6))]
        h = rng.randint(len(p), len(p) + 12)
        assert min_eating_speed(p, h) == _brute(p, h), (p, h)
    print("ok 875_koko_eating_bananas")
