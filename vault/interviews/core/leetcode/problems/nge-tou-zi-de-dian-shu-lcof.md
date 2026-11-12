---
slug: nge-tou-zi-de-dian-shu-lcof
---
## Q
**剑指 Offer 60 n个骰子的点数**｜Medium

掷 `num` 个六面骰子，按点数和从小到大（`num` 到 `6num`）返回每个和出现的概率。

## A
**一句话。** 计数 DP，`dp[i][j]` 为 `i` 个骰子和为 `j` 的方案数，按最后一颗的点数转移，最后除以 `6^num`。

```python
def dice_probability(num):
    top = 6 * num
    dp = [[0] * (top + 1) for _ in range(num + 1)]
    dp[0][0] = 1
    for i in range(1, num + 1):
        for j in range(i, 6 * i + 1):
            dp[i][j] = sum(dp[i - 1][j - f]
                           for f in range(1, 7) if j >= f)
    total = 6 ** num
    return [dp[num][j] / total for j in range(num, top + 1)]
```

**复杂度。** 时间 `O(num²)`，空间 `O(num²)`。

**易错点。**
- 结果下标没平移：和从 `num` 开始，`range(5*num+1)` 在 `num=1` 时混进不可能的和 `0`，漏了和 `6`。
- `j - f` 为负：Python 负下标不报错，会读到行尾，必须显式判断。
- 中间就把概率四舍五入：误差逐层放大，先用整数计数最后一次相除。

**追问。**
- `k` 面骰子呢？：内层改 `range(1, k+1)`，和的范围 `[num, k*num]`。
- 能省空间吗？：`dp[i]` 只依赖 `dp[i-1]`，压成一维滚动。

**同模式。** LC 1155 掷骰子等于目标和的方法数、LC 518 零钱兑换 II、LC 837 新 21 点
