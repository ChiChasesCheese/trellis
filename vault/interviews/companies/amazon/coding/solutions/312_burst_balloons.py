"""LC 312 Burst Balloons -- interval DP: pick the LAST balloon to burst in (l, r). Time O(n^3), space O(n^2)."""
from functools import lru_cache
from random import Random

# --- solution ---
def max_coins(nums):
    a = [1] + nums + [1]                      # virtual balloons at both ends
    n = len(a)
    dp = [[0] * n for _ in range(n)]          # dp[l][r]: best coins bursting everything strictly between l and r
    for length in range(2, n):                # widen the open interval (l, r)
        for l in range(n - length):
            r = l + length
            for k in range(l + 1, r):         # k is the LAST one burst: its neighbours are l and r
                dp[l][r] = max(dp[l][r], dp[l][k] + a[l] * a[k] * a[r] + dp[k][r])
    return dp[0][n - 1]
# --- end ---

def _brute(nums):
    @lru_cache(maxsize=None)
    def go(t):
        if not t:
            return 0
        best = 0
        for i in range(len(t)):
            left = t[i - 1] if i else 1
            right = t[i + 1] if i + 1 < len(t) else 1
            best = max(best, left * t[i] * right + go(t[:i] + t[i + 1:]))
        return best
    return go(tuple(nums))

if __name__ == "__main__":
    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10
    assert max_coins([]) == 0
    assert max_coins([7]) == 7
    rng = Random(21)
    for _ in range(100):
        a = [rng.randint(0, 5) for _ in range(rng.randint(0, 6))]
        assert max_coins(a) == _brute(a), a
    print("ok 312_burst_balloons")
