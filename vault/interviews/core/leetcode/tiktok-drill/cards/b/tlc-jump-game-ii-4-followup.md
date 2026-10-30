---
id: tlc-jump-game-ii-4-followup
node: b.jump-game-ii
type: qa
step: 4
---
## Q
**LC 45 跳跃游戏 II**｜追问

面试官接着问：（1）如果不保证能到达终点，怎么判断并返回 `-1`？（2）要输出具体跳在哪些下标？（3）如果每次跳跃有不同的代价，贪心还成立吗？

## A
1. **不保证可达**：换层时若 `farthest` 没有超过 `cur_end`，说明被卡住了。
```python
def jump_or_fail(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            if farthest <= i:          # 下一层没有新位置：到不了
                return -1
            jumps += 1
            cur_end = farthest
    return jumps
```
`[3,2,1,0,4]` → `-1`，`[2,3,1,1,4]` → `2`。
   只判可达（LC 55）则不用计数：维护 `farthest`，`i > farthest` 时返回 `False`。
2. **输出路径**：每层记下使 `i + nums[i]` 最大的那个下标 `best_i`；换层时把 `best_i` 追加到路径。BFS 版则用 `parent` 数组回溯，空间 `O(n)`。
3. **带代价**：贪心依赖「每一跳等价」。代价不同后要用 DP（`dp[j] = min(dp[i] + cost)`，`O(n^2)`）或 Dijkstra；若代价相同但每格只能跳固定几种长度，则是普通 BFS。

**Python 提醒**：写 DP 版时 `dp = [math.inf] * n` 得到的是 `float`，不可达时返回类型会变成 `float`；用大整数哨兵 `n` 或单独判断更干净。
