"""LC 739 Daily Temperatures -- monotonic (decreasing) stack of indices. Time O(n), space O(n)."""
from random import Random

# --- solution ---
def daily_temperatures(temps):
    ans = [0] * len(temps)
    stack = []                                   # indices whose answer is still unknown; temps decreasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:    # t is the next warmer day for everything it beats
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
# --- end ---

def _brute(t):
    out = []
    for i in range(len(t)):
        d = 0
        for j in range(i + 1, len(t)):
            if t[j] > t[i]:
                d = j - i
                break
        out.append(d)
    return out

if __name__ == "__main__":
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
    assert daily_temperatures([50, 50, 50]) == [0, 0, 0]       # equal is not warmer
    assert daily_temperatures([]) == []
    rng = Random(8)
    for _ in range(300):
        t = [rng.randint(30, 36) for _ in range(rng.randint(0, 10))]
        assert daily_temperatures(t) == _brute(t), t
    print("ok 739_daily_temperatures")
