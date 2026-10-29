---
id: tlc-combination-sum-ii-4-followup
node: a.combination-sum-ii
type: qa
step: 4
---
## Q
**LC 40 组合总和 II**｜追问

面试官接着问：（1）不想比较相邻元素，有别的去重方式吗？（2）元素可以重复使用呢（LC 39）？（3）只问有多少种组合，不要列出来？

## A
1. **按值分组**：用 `Counter` 把数组变成 `(值, 个数)`，每层只决定「这个值选 `0..count` 个」，同一个值只在一层出现，重复组合不可能出现，也不依赖排序后的相邻比较：

```python
from collections import Counter


def combination_sum2_counts(candidates: list[int], target: int) -> list[list[int]]:
    items = sorted(Counter(candidates).items())      # [(值, 个数)]，每个不同的值只处理一次
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(k: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])
            return
        if k == len(items):
            return
        value, count = items[k]
        for used in range(min(count, remain // value) + 1):   # 这个值选 0..count 个
            path.extend([value] * used)
            dfs(k + 1, remain - used * value)
            del path[len(path) - used:]                       # 回退
    dfs(0, target)
    return result
```

2. **元素可重复使用（LC 39）**：选了 `nums[i]` 后下一层仍从 `i` 开始（`dfs(i, ...)`），不需要同层去重，因为数组本身无重复。
3. **只数个数**：这是 `0/1` 背包的计数版，`dp[s]` 表示和为 `s` 的方案数；有重复元素时，按值分组、同一个值最多取 `count` 个，需要多重背包的处理，或者先按 `Counter` 展开成「值 + 个数」再转移；`target <= 30` 时 `dp` 规模很小。

**Python 提醒**：`path.append(...)` 之后记得 `path.pop()`；把 `path` 直接放进结果会放进同一个对象的引用，要写 `result.append(path[:])` 或 `list(path)`。
