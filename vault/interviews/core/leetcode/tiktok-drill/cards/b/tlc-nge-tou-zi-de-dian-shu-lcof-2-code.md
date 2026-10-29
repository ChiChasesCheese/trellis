---
id: tlc-nge-tou-zi-de-dian-shu-lcof-2-code
node: b.nge-tou-zi-de-dian-shu-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 60 n个骰子的点数**｜写出 Python 实现

`num`（`1` 到 `11`）个六面骰子，返回点数和为 `num, num+1, …, 6num` 的概率数组。用完整的二维 DP 表实现。

## A
**思路。** `dp[i][j]` 是 `i` 个骰子和为 `j` 的方案数，`dp[0][0] = 1`。第 `i` 行由第 `i - 1` 行按最后一个骰子的点数（1 到 6）累加得到。最后把第 `num` 行的 `[num, 6num]` 段除以 `6^num`。

```python
def dice_probability(num: int) -> list[float]:
    top = 6 * num
    # dp[i][j]：掷 i 个骰子、点数和恰好为 j 的方案数（整数，最后再除，避免浮点误差累积）
    dp = [[0] * (top + 1) for _ in range(num + 1)]
    dp[0][0] = 1                                     # 0 个骰子和为 0：一种方案
    for i in range(1, num + 1):
        for j in range(i, 6 * i + 1):                # i 个骰子的和只可能落在 [i, 6i]
            dp[i][j] = sum(dp[i - 1][j - face] for face in range(1, 7) if j - face >= 0)
    total = 6 ** num
    return [dp[num][j] / total for j in range(num, top + 1)]
```

运行（保留 5 位小数）：`num = 1` → 6 个 `0.16667`；`num = 3` → `[0.00463, 0.01389, 0.02778, 0.0463, 0.06944, 0.09722, 0.11574, 0.125, 0.125, 0.11574, 0.09722, 0.06944, 0.0463, 0.02778, 0.01389, 0.00463]`；`num = 11` → 长度 56，最小的概率 `1/6^11 ≈ 2.76e-09`。

**复杂度。** 时间 `O(num^2)`：`(num+1)(6num+1)` 格，每格最多 6 项；空间 `O(num^2)`。

**写法要点。** 二维表用列表推导 `[[0] * (top + 1) for _ in range(num + 1)]` 建，每行独立；内层用 `sum(生成器表达式)` 把 6 项累加写成一行，条件 `if j - face >= 0` 挡住负下标；`6 ** num` 是精确的整数，`int / int` 得到正确舍入的浮点数；`j` 只遍历 `[i, 6i]`，不可能的和保持 0。
