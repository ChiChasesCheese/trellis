---
slug: maximum-average-subarray-i
---
## Q
**LC 643 子数组最大平均数 I**｜Easy

整数数组 `nums` 和整数 `k`，求长度恰为 `k` 的连续子数组的最大平均数。

## A
**一句话。** 定长滑动窗口：长度固定，平均数最大就是窗口和最大，右移时加进新的、减去滑出的。

```python
def find_max_average(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]  # 一进一出
        best = max(best, window)
    return best / k                      # 只在最后除一次
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `best` 初始化为 `0`：全负数时错，`[-1]`、`k=1` 得 `0.0`，应为 `-1.0`。
- 滑出下标写错：应是 `i - k`，不是 `i - k + 1` 或 `i - 1`。

**追问。**
- 长度不固定、至少为 `k`（LC 644）？：二分平均值，配合前缀和判断是否存在平均不小于它的子数组。
- 为什么不逐窗口求平均？：整数和比较更精确，也省除法。

**同模式。** LC 1456 定长子串中元音的最大数目、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 239 滑动窗口最大值
