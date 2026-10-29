---
id: tlc-integer-break-2-code
node: b.integer-break
type: qa
step: 2
---
## Q
**LC 343 整数拆分**｜Medium · 字节高频｜写出 Python 实现

给正整数 `n`（`2 <= n <= 58`），把它拆成至少两个正整数之和，返回这些整数乘积的最大值。用一维 DP。

## A
**思路。** `dp[i]` 表示把 `i` 拆成至少两份的最大乘积。对每个 `i`，枚举第一块 `j`（`1 <= j < i`）：剩下的 `i - j` 或者直接作为一个因子，或者继续拆成 `dp[i - j]`，两种取较大者。答案是 `dp[n]`。

```python
def integer_break(n: int) -> int:
    dp = [0] * (n + 1)                 # dp[i]：把 i 拆成至少 2 个正整数的最大乘积
    for i in range(2, n + 1):
        for j in range(1, i):          # 先切下一块 j，剩下的 i - j 可以不再拆，也可以继续拆
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
    return dp[n]
```

运行：`integer_break(2)` → `1`，`integer_break(3)` → `2`，`integer_break(4)` → `4`，`integer_break(10)` → `36`，`integer_break(58)` → `1549681956`。

**复杂度。** 时间 `O(n^2)`：两层循环；空间 `O(n)`：一维数组 `dp`。

**写法要点。** `max` 接受多个参数，一次比较三个候选，不必写嵌套的 `if`；`range(2, n + 1)` 从 `2` 开始，因为 `1` 不能拆成至少两份，`dp[1]` 保持 `0` 且不会被用作「已拆」的结果；`dp = [0] * (n + 1)` 创建一维列表，没有别名问题。
