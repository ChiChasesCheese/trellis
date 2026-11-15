---
slug: maximum-and-sum-of-array
---
## Q
**LC 2172 数组的最大与和**｜Hard

`n` 个整数 `nums` 和 `numSlots` 个篮子（编号 `1` 到 `numSlots`，每个篮子至多放 `2` 个数，`2 · numSlots >= n`）。一个放置方案的"与和"是每个数与其所在篮子编号按位与之和。求最大与和。

## A
**一句话。** 三进制状压：每个篮子装了 `0/1/2` 个数，`dp[mask]` 表示该装法下前 `i` 个数（`i` 为各位之和）的最大与和，依次决定第 `i` 个数放哪个篮子。

```python
def maximum_and_sum(nums, num_slots):
    n = len(nums)
    size = 3 ** num_slots
    dp = [0] * size
    for mask in range(size):
        i, m = 0, mask
        while m:                           # 各三进制位之和 = 已放个数
            i += m % 3
            m //= 3
        if i >= n:
            continue
        p = 1
        for slot in range(1, num_slots + 1):
            if mask // p % 3 < 2:          # 篮子没满
                gain = nums[i] & slot
                dp[mask + p] = max(dp[mask + p], dp[mask] + gain)
            p *= 3
    return max(dp)
```

**复杂度。** 时间 `O(3^s · s)`，空间 `O(3^s)`（`s = numSlots`）。

**易错点。**
- 把每个篮子拆成两个槽位用二进制掩码：`2^(2s)` 比 `3^s` 大，而且同篮子的两个槽位有重复状态。
- 篮子满了仍转移：每位三进制数不能超过 `2`。

**追问。**
- 也能当成匹配问题吗？：每个篮子拆成两个槽位，是二分图最大权匹配，可用 KM 算法。

**同模式。** LC 1066 校园自行车分配 II、LC 1947 最大兼容性评分和、LC 1879 两个数组最小的异或值之和
