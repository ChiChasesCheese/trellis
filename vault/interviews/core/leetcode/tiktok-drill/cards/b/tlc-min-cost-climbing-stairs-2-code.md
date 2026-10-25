---
id: tlc-min-cost-climbing-stairs-2-code
node: b.min-cost-climbing-stairs
type: qa
step: 2
---
## Q
**LC 746 使用最小花费爬楼梯**｜写出 Python 实现

整数数组 `cost`（`2 <= 长度 <= 1000`，`0 <= cost[i] <= 999`），每付一次 `cost[i]` 可从第 `i` 级向上爬一级或两级，起点可选下标 `0` 或 `1`，求到达下标 `cost.length` 的最低总花费。

## A
**思路。** `dp[i]` 表示到达第 `i` 级的最小花费，`dp[0] = dp[1] = 0`。到达 `i` 要么从 `i-1` 付 `cost[i-1]`，要么从 `i-2` 付 `cost[i-2]`，取较小者。只需前两项，用两个变量滚动。

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    two_back = one_back = 0                    # 到达第 i-2、i-1 级的最小花费；起点 0、1 都免费
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    return one_back
```

运行：`[10,15,20]` → `15`；`[1,100,1,1,1,100,1,1,100,1]` → `6`；`[0,0]` → `0`；`[5,3]` → `3`；长度 `1000` 且全为 `999` → `499500`。

**复杂度。** 时间 `O(n)`：循环 `n - 1` 次；空间 `O(1)`：两个变量。

**写法要点。** `two_back, one_back = one_back, min(...)` 用元组赋值同时更新两个变量，右边先整体算完再赋值，所以不会用到被覆盖的旧值，不需要临时变量；`range(2, len(cost) + 1)` 的上界是 `n` 本身，因为状态 `n` 才是顶部；`two_back = one_back = 0` 链式赋值只用于不可变的整数。
