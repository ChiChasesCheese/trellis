---
slug: jump-game-ii
---
## Q
**LC 45 跳跃游戏 II**｜Medium

`nums[i]` 表示从下标 `i` 最多向后跳几格，求从下标 `0` 到最后一格的最少跳跃次数（保证能到）。

## A
**一句话。** 隐式 BFS 分层：边扫当前层边记下一层最远能到的位置，扫到层末就计一跳。

```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):   # 最后一格不用再跳
        farthest = max(farthest, i + nums[i])
        if i == cur_end:             # 这一层走完，必须再跳
            jumps += 1
            cur_end = farthest       # 下一层的右边界
    return jumps
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 循环扫到最后一格：`i == cur_end` 会多计一跳，`[2,3,1,1,4]` 得 `3`，应为 `2`。
- 每次跳到 `nums[j]` 最大的格子：该比的是 `j + nums[j]`。`[3,3,1,2,1,1]` 按值挑得 `3`，应为 `2`。

**追问。**
- 不保证能到达（LC 55）？：层末若 `farthest <= i` 就无解。
- 要输出路径？：每层记下使 `i + nums[i]` 最大的 `i`，走到层尾时把它记进路径，最后补上 `n - 1`。
- 每跳有不同代价？：贪心失效，改 DP 或 Dijkstra。

**同模式。** LC 55 跳跃游戏、LC 1024 视频拼接、LC 1326 灌溉花园的最少水龙头数目、LC 871 最低加油次数
