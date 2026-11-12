---
slug: frog-jump
---
## Q
**LC 403 青蛙过河**｜Hard

青蛙从第一块石子（位置 `0`）出发，第一步只能跳 `1`；上一步跳了 `k`，下一步只能跳 `k - 1`、`k` 或 `k + 1`，且必须落在石子上。判断能否到达最后一块石子。

## A
**一句话。** 状态是「站在哪块石子、上一步跳了多远」，用字典记录每块石子能以哪些步长到达，按位置从左到右推进。

```python
def can_cross(stones):
    jumps = {pos: set() for pos in stones}   # 位置 -> 到达它的步长
    jumps[0].add(0)                          # 下一跳只能是 1
    for pos in stones:
        for k in jumps[pos]:
            for step in (k - 1, k, k + 1):
                if step > 0 and pos + step in jumps:
                    jumps[pos + step].add(step)
    return bool(jumps[stones[-1]])
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 漏掉 `step > 0`：`step = 0` 时目标就是自己，往正在遍历的集合里加元素，`RuntimeError`。
- 只记石子可达、不记上一跳：丢了决定下一步范围的信息。
- 每次贪心跳最大步：`[0,1,3,5,8,11,13,15,16]` 会走进死路返回 `False`，应为 `True`。

**追问。**
- 递归怎么写？：`@cache` 的 `dfs(pos, k)`，逐个试 `k + 1, k, k - 1`，找到终点提前返回。
- 要输出一条跳法？：集合里存 `(上一块石子, 步长)`，终点回溯。

**同模式。** LC 55 跳跃游戏、LC 45 跳跃游戏 II、LC 1871 跳跃游戏 VII、LC 1306 跳跃游戏 III
