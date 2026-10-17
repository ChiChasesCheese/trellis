"""LC 70 Climbing Stairs -- dp[i] = dp[i-1] + dp[i-2], compressed to two variables. Time O(n), space O(1)."""
from functools import lru_cache

# --- solution ---
def climb_stairs(n):
    a, b = 1, 1                    # ways(0), ways(1)
    for _ in range(n - 1):
        a, b = b, a + b            # ways(i) = ways(i-1) + ways(i-2)
    return b


def climb_stairs_memo(n):          # top-down version of the same recurrence
    @lru_cache(maxsize=None)
    def ways(i):
        return 1 if i <= 1 else ways(i - 1) + ways(i - 2)
    return ways(n)
# --- end ---

if __name__ == "__main__":
    for f in (climb_stairs, climb_stairs_memo):
        assert [f(i) for i in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]
        assert f(45) == 1836311903
    assert climb_stairs(0) == 1
    print("ok 70_climbing_stairs")
