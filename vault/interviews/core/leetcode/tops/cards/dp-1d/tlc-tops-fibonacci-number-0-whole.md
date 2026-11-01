---
id: tlc-tops-fibonacci-number-0-whole
node: dp-1d.fibonacci-number
type: qa
---
## Q
**LC 509 斐波那契数**｜Easy · 全公司热度第 133 名

斐波那契数 `F(n)` 由 `F(0) = 0`、`F(1) = 1` 开始，之后每一项都是前两项之和：`F(n) = F(n - 1) + F(n - 2)`（`n > 1`）。给定 `n`，计算 `F(n)`。`0 <= n <= 30`。例：`n = 2` → `1`；`n = 3` → `2`；`n = 4` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 递推关系 + 记忆化（memoization）：重叠子问题是动态规划的起点。

**一句话。** 按定义写递归，用缓存保证每个 `F(i)` 只算一次。

**识别。** 题目直接给出递推式 `F(n) = F(n - 1) + F(n - 2)` = 自顶向下递归；递归树里 `F(n - 2)` 会被 `F(n)` 和 `F(n - 1)` 各算一次，出现**重叠子问题**，就用缓存。

**推导。** 直接递归，`F(30)` 要调用 `2692537` 次，调用次数随 `n` 指数增长（约 `1.618^n`）。只有 `n + 1` 个不同的子问题，缓存之后每个只算一次，调用次数降到 `O(n)`。

```python
from functools import cache


def fib(n: int) -> int:
    @cache  # 记忆化：每个 i 只算一次，其余直接取缓存
    def f(i: int) -> int:
        if i < 2:
            return i  # F(0) = 0, F(1) = 1
        return f(i - 1) + f(i - 2)

    return f(n)
```

运行：`n = 0..10` 依次得到 `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55`，`n = 2, 3, 4` 即示例的 `1, 2, 3`；`n = 30` → `832040`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（缓存与递归栈）。

**拓展优化。**
- 自底向上只保留最近两项，空间 `O(1)`，也没有递归深度的限制：

```python
def fib_iter(n: int) -> int:
    a, b = 0, 1  # a = F(i), b = F(i + 1)
    for _ in range(n):
        a, b = b, a + b
    return a
```

- `n` 很大（比如 `10^18`，结果取模）时用快速倍增（fast doubling），`O(log n)`，依据 `F(2m) = F(m) * (2F(m+1) - F(m))`、`F(2m+1) = F(m)^2 + F(m+1)^2`：

```python
def fib_doubling(n: int) -> int:
    def pair(k: int) -> tuple[int, int]:
        """返回 (F(k), F(k + 1))。"""
        if k == 0:
            return 0, 1
        a, b = pair(k >> 1)  # a = F(m), b = F(m + 1), m = k // 2
        c = a * (2 * b - a)  # F(2m)
        d = a * a + b * b    # F(2m + 1)
        return (d, c + d) if k & 1 else (c, d)

    return pair(n)[0]
```

**易错点。**
- 基准写成 `F(0) = F(1) = 1`：`n = 4` 得到 `5`，正确是 `3`；`n = 0` 得到 `1`，正确是 `0`。
- 不加缓存的纯递归：`n = 30` 勉强能跑（约 `2.7 * 10^6` 次调用），`n = 50` 要调用约 `4.1 * 10^10` 次。
- 缓存递归的深度是 `n`：`n` 超过约 `1000` 时 CPython 抛 `RecursionError`；`n <= 30` 没问题，更大的 `n` 用 `fib_iter`。

**同模式。** LC 70 爬楼梯、LC 1137 第 N 个泰波那契数、LC 746 使用最小花费爬楼梯、LC 198 打家劫舍。
