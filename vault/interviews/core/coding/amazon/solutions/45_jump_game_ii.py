"""LC 45 Jump Game II -- greedy BFS by levels; the path-returning version keeps the farthest-reaching index per level."""
from random import Random

# --- solution ---
def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])                       # farthest index reachable with jumps + 1
        if i == end:                                      # left the current level: must take one more jump
            jumps += 1
            end = far
    return jumps

def jump_path(nums):
    n = len(nums)
    path, end, far, best = [], 0, 0, 0                    # best = index that attains `far`
    for i in range(n - 1):
        if i + nums[i] > far:
            far, best = i + nums[i], i
        if i == end:
            path.append(best)                             # the landing of this level = index reaching farthest
            end = far
    return path + [n - 1] if n > 1 else [0]
# --- end ---

def _dp(nums):
    n = len(nums)
    INF = 10**9
    d = [INF] * n
    d[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            d[j] = min(d[j], d[i] + 1)
    return d[-1]

if __name__ == "__main__":
    assert jump([2, 3, 1, 1, 4]) == 2 and jump([2, 3, 0, 1, 4]) == 2 and jump([0]) == 0
    assert jump_path([2, 3, 1, 1, 4]) == [0, 1, 4]
    rng = Random(45)
    done = 0
    while done < 500:
        nums = [rng.randint(0, 4) for _ in range(rng.randint(1, 10))]
        want = _dp(nums)
        if want >= 10**9:
            continue
        done += 1
        assert jump(nums) == want, nums
        p = jump_path(nums)
        assert p[0] == 0 and p[-1] == len(nums) - 1 and len(p) - 1 == want, (nums, p)
        assert all(0 < b - a <= nums[a] for a, b in zip(p, p[1:])), (nums, p)
    print("ok 45_jump_game_ii")
