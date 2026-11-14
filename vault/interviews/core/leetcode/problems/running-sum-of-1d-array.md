---
slug: running-sum-of-1d-array
---
## Q
**LC 1480 一维数组的动态和**｜Easy

返回数组 `ans`，`ans[i] = nums[0] + … + nums[i]`。

## A
**一句话。** 前缀和递推：每一位加上前一位已算好的和，原地即可。

```python
def running_sum(nums):
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]   # 前一位已是前缀和
    return nums
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 从下标 `0` 开始：`nums[-1]` 是最后一个元素，会被错加到第一位。
- 每位重新求和：`O(n^2)`。

**追问。**
- 一行写法？：`list(accumulate(nums))`。
- 求区间和？：在前面补一个 `0`，`sum(l..r) = s[r+1] - s[l]`。

**同模式。** LC 303 区域和检索 - 数组不可变、LC 560 和为 K 的子数组、LC 724 寻找数组的中心下标
