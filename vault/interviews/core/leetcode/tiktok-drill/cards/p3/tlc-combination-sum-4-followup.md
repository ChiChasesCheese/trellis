---
id: tlc-combination-sum-4-followup
node: p3.combination-sum
type: qa
step: 4
---
## Q
**LC 39 组合总和**｜追问

面试官接着问：（1）数组含重复元素，且每个数字最多用一次（LC 40）怎么改？（2）只问有多少种组合，`target` 很大（LC 518）怎么办？（3）如果元素里有负数会怎样？

## A
1. **每个数只用一次、含重复**：排序后递归传 `i + 1`；为了不产生重复组合，在同一层里跳过与前一个相同的数（`i > start and candidates[i] == candidates[i - 1]`）。

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            if i > start and candidates[i] == candidates[i - 1]:    # 同一层里相同的数只选一次
                continue
            path.append(candidates[i])
            dfs(i + 1, remain - candidates[i])
            path.pop()

    dfs(0, target)
    return result
```

`combination_sum2([10,1,2,7,6,1,5], 8)` → `[[1,1,6],[1,2,5],[1,7],[2,6]]`。
2. **只求个数**：回溯会枚举全部方案，目标很大时太慢。改用完全背包式的动态规划：外层遍历数、内层遍历和，每个组合只按数的顺序累计一次。

```python
def count_ways(candidates: list[int], target: int) -> int:
    dp = [1] + [0] * target
    for x in candidates:                           # 外层遍历数，内层遍历和：同一组合只算一次
        for t in range(x, target + 1):
            dp[t] += dp[t - x]
    return dp[target]
```

`count_ways([1,2,5], 5)` → `4`，`count_ways([2], 3)` → `0`，时间 `O(len * target)`。两层循环交换顺序就变成统计**排列**数（LC 377）。
3. **含负数**：搜索不再有界，`remain` 不会单调减小，可能无限递归，必须额外限制组合长度，或者题目本身禁止负数；这也是原题限定 `candidates[i] >= 2` 的原因。

**Python 提醒**：`[1] + [0] * target` 一次建好 `dp` 初始值；不要写成 `[[]] * n` 之类的嵌套乘法来初始化二维结构，所有行会共享同一个列表。
