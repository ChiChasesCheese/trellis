---
slug: split-array-with-same-average
---
## Q
**LC 805 数组的均值分割**｜Hard

`nums`（`n <= 30`，元素 `<= 10^4`）分成两个非空数组 `A`、`B`，判断能否使两者平均值相等。

## A
**一句话。** 两者平均值相等等价于都等于总平均值，即存在 `k` 个数（`1 <= k <= n/2`）的和恰为 `total·k/n`；按「选了几个」做 0-1 背包，每个 `k` 用一个整数当位集合记录可达的和。

```python
def split_array_same_average(nums):
    n, total = len(nums), sum(nums)
    dp = [0] * (n // 2 + 1)    # dp[k]：选 k 个数能凑出的和（位集）
    dp[0] = 1
    for x in nums:
        for k in range(n // 2, 0, -1):   # 倒序：每个数只用一次
            dp[k] |= dp[k - 1] << x
    for k in range(1, n // 2 + 1):
        if total * k % n == 0:           # 目标和必须是整数
            if dp[k] >> (total * k // n) & 1:
                return True
    return False
```

**复杂度。** 时间 `O(n²·S / w)`（`S` 为总和，`w` 为字长），空间 `O(n·S / w)`。

**易错点。**
- `k` 枚举到 `n`：`A` 取 `n` 个时 `B` 为空；只需看较小的一侧，`k <= n/2`。
- 正序更新 `k`：同一个数会被用多次。

**追问。**
- 折半枚举怎么做？：先把每个数减去平均值（乘 `n` 去分母），问题变成找和为 0 的非空真子集；两半各枚举 `2^15` 个子集和，查另一半里是否有相反数。
- 为什么只看 `total·k % n == 0` 的 `k`？：元素都是整数，凑出的和必为整数。

**同模式。** LC 416 分割等和子集、LC 494 目标和、LC 1755 最接近目标值的子序列和
