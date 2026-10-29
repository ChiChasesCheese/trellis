---
id: tlc-frog-jump-5-alt
node: a.frog-jump
type: qa
step: 5
---
## Q
**LC 403 青蛙过河**｜另一种解法

写出自顶向下的记忆化搜索版本，并说明它和自底向上字典 DP 相比，什么时候选哪个。

## A
**思路。** `dfs(pos, k)`：站在 `pos`、上一跳为 `k`，能否到达终点。到终点返回 `True`；否则尝试 `k + 1, k, k − 1`（必须为正且落点是石子），任一成功就返回 `True`。用 `functools.cache` 记忆，保证每个状态只算一次。先尝试大步，通常更快碰到终点。

```python
from functools import cache

def can_cross_memo(stones: list[int]) -> bool:
    on_stone = set(stones)
    last = stones[-1]

    @cache
    def dfs(pos: int, k: int) -> bool:         # 站在 pos，上一跳长度为 k
        if pos == last:
            return True
        return any(step > 0 and pos + step in on_stone and dfs(pos + step, step)
                   for step in (k + 1, k, k - 1))

    return dfs(0, 0)
```

运行：`[0,1,3,5,6,8,12,17]` → `True`，`[0,1,2,3,4,8,9,11]` → `False`，`[0,1]` → `True`，`[0,2]` → `False`；`1999` 块连续石子加一块位置 `10^9` 的终点 → `False`，没有触发 `RecursionError`。

**对比。** 自顶向下只访问从起点可达的状态，找到终点就提前结束，成功的输入通常很快；但最坏仍是 `O(n^2)` 个状态，并且递归深度没有保证（路径越长越深），`n` 更大时有 `RecursionError` 风险。自底向上按位置扫描，没有递归，复杂度稳定，写法也短；缺点是不能提前退出（不过也可以在终点集合非空时 `break`）。面试里先写自底向上字典 DP，被问到「怎么只搜可达状态」时再给这个版本。

**不要用的做法。** 用 `dp[位置]` 数组：位置高达 `2^31`，开不出来；只用「石子下标」又丢掉了上一跳长度。
