"""LC 239 Sliding Window Maximum -- monotonic deque (decreasing values). Time O(n), space O(k)."""
from collections import deque
from random import Random

# --- solution ---
def max_sliding_window(nums, k):
    dq = deque()                         # indices; nums[dq[0]] > nums[dq[1]] > ...
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:  # smaller elements before x can never be a max again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:               # front fell out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
# --- end ---

def _brute(a, k):
    return [max(a[i:i + k]) for i in range(len(a) - k + 1)]

if __name__ == "__main__":
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    assert max_sliding_window([9, 11], 2) == [11]
    assert max_sliding_window([4, 3, 2, 1], 2) == [4, 3, 2]
    assert max_sliding_window([2, 2, 2], 2) == [2, 2]
    rng = Random(10)
    for _ in range(300):
        a = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, len(a))
        assert max_sliding_window(a, k) == _brute(a, k), (a, k)
    print("ok 239_sliding_window_maximum")
