---
slug: combination-sum-iv
---
## Q
**LC 377 组合总和 Ⅳ**｜Medium

不同正整数数组 `nums` 可重复取，求和为 `target` 的序列个数（顺序不同算不同）。

## A
**一句话。** 完全背包求排列数：`dp[t] = Σ dp[t-x]`，外层枚举目标和，内层枚举数。

```python
def combination_sum4(nums, target):
    dp = [0] * (target + 1)
    dp[0] = 1                    # 空序列
    for t in range(1, target + 1):   # 外层是目标和 → 计顺序
        for x in nums:
            if x <= t:
                dp[t] += dp[t - x]   # 以 x 结尾
    return dp[target]
```

**复杂度。** 时间 `O(target·|nums|)`，空间 `O(target)`。

**易错点。**
- 循环顺序写反（先数后目标）：变成不计顺序的组合数，`[1,2,3]`、`4` 得 `4` 而非 `7`。
- `dp[0]` 写成 `0`：整张表恒为 `0`。
- 漏掉 `x <= t`：负下标读到数组末尾。

**追问。**
- 数组含负数会怎样？：可能出现无限长序列，必须限制序列长度或禁止正负抵消。
- 不计顺序怎么算？：循环顺序对调，即 LC 518 零钱兑换 II。

**同模式。** LC 518 零钱兑换 II、LC 322 零钱兑换、LC 70 爬楼梯、LC 279 完全平方数
