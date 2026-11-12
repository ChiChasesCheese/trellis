---
slug: partition-equal-subset-sum
---
## Q
**LC 416 分割等和子集**｜Medium

正整数数组能否分成和相等的两个子集。

## A
**一句话。** 0/1 背包可行性：总和为奇数直接失败，否则判断能否选出和恰为 `S/2` 的子集。

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:                 # 奇数不可能平分
        return False
    n, half = len(nums), total // 2
    # dp[i][j]：前 i 个数能否凑出和 j
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True               # 一个都不选只能凑 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(half + 1):
            # 不选第 i 个 / 选第 i 个
            dp[i][j] = (dp[i-1][j]
                        or (j >= x and dp[i-1][j-x]))
    return dp[n][half]
```

**复杂度。** 时间 `O(nS)`，空间 `O(nS)`。

**易错点。**
- 转移读本行 `dp[i][j-x]`：同一个数重复用，变成完全背包。`[1,5]` 目标 `3` 错答 `True`。
- 漏掉奇数判断：`[1,2]` 的 `half=1`，选 `[1]` 错答 `True`。
- 忘了 `dp[0][0] = True`：整张表全 `False`，`[2,2]` 得 `False`。

**追问。**
- 怎么压空间？：一维数组，内层 `j` 倒序，空间 `O(S)`。
- 求两堆的最小差（LC 1049）？：看最后一行，找最接近 `S/2` 的可达和 `j`，差为 `S - 2j`。
- 要输出分法？：从 `dp[n][half]` 回走，`dp[i-1][j]` 为假则第 `i` 个必选。

**同模式。** LC 494 目标和、LC 1049 最后一块石头的重量 II、LC 474 一和零、LC 698 划分为k个相等的子集
