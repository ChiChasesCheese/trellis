"""LC 55 Jump Game (+ LC 45 Jump Game II) -- greedy: track the farthest reachable index. Time O(n), space O(1)."""
from random import Random

# --- solution ---
def can_jump(nums):
    farthest = 0
    for i, step in enumerate(nums):
        if i > farthest:                      # index i is unreachable, and so is everything after it
            return False
        farthest = max(farthest, i + step)
    return True


def min_jumps(nums):                          # LC 45 (answer exists): BFS by levels, without a queue
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):            # stop BEFORE the last index: we only need to reach it
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                      # the current jump's range is exhausted: we must jump again
            jumps += 1
            cur_end = farthest
    return jumps
# --- end ---

def _brute_can(nums):                         # O(n^2) DP: reach[i] if some earlier reachable j covers i
    reach = [False] * len(nums)
    reach[0] = True
    for i in range(1, len(nums)):
        reach[i] = any(reach[j] and j + nums[j] >= i for j in range(i))
    return reach[-1]

def _brute_min(nums):
    INF = float("inf")
    best = [INF] * len(nums)
    best[0] = 0
    for i in range(1, len(nums)):
        best[i] = min((best[j] + 1 for j in range(i) if best[j] < INF and j + nums[j] >= i), default=INF)
    return best[-1]

if __name__ == "__main__":
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    assert can_jump([0]) is True
    assert can_jump([0, 1]) is False
    assert min_jumps([2, 3, 1, 1, 4]) == 2
    assert min_jumps([2, 3, 0, 1, 4]) == 2
    assert min_jumps([0]) == 0
    rng = Random(1)
    for _ in range(500):
        a = [rng.randint(0, 4) for _ in range(rng.randint(1, 10))]
        assert can_jump(a) == _brute_can(a), a
        if _brute_can(a):
            assert min_jumps(a) == _brute_min(a), a
    print("ok 55_jump_game")
