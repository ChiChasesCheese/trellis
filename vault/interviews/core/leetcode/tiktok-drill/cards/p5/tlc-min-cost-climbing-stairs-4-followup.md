---
id: tlc-min-cost-climbing-stairs-4-followup
node: p5.min-cost-climbing-stairs
type: qa
step: 4
---
## Q
**LC 746 使用最小花费爬楼梯**｜追问

面试官接着问：（1）要输出具体怎么爬（经过哪些台阶）？（2）每次最多可以爬 `k` 级？（3）能不能用记忆化递归写，什么时候更合适？分别怎么改。

## A
1. **输出路线**：滚动变量保存不下来路线，改回整张 `dp` 表，再多存一个 `prev[i]`（最优来源是 `i-1` 还是 `i-2`）。从 `n` 起沿 `prev` 往回走，到 `0` 或 `1` 停止，最后反转。空间升到 `O(n)`。
2. **最多爬 `k` 级**：`dp[i] = min(dp[j] + cost[j] for j in range(max(0, i-k), i))`，朴素 `O(nk)`。要降到 `O(n)`，用单调队列维护滑动窗口里 `dp[j] + cost[j]` 的最小值。
3. **记忆化递归**：

```python
from functools import cache


def min_cost_memo(cost: list[int]) -> int:
    n = len(cost)

    @cache
    def go(i: int) -> int:                     # 从第 i 级出发到顶的最小花费
        if i >= n:
            return 0
        return cost[i] + min(go(i + 1), go(i + 2))

    return min(go(0), go(1))
```

   `[10,15,20]` → `15`。写起来最接近题意，适合状态之间依赖不规则的题；这里是规则的线性依赖，迭代滚动更快、不占栈。长度 `1000` 的输入会让递归深度越过 Python 默认上限 `1000`，抛 `RecursionError`，所以主解用迭代。

**Python 提醒**：`functools.cache` 把参数当字典键，参数必须可哈希；缓存放在函数对象上，同一个模块里多次调用外层函数会各自新建内层 `go` 与缓存，不会互相污染，但也不会跨调用复用。
