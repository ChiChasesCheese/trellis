---
id: tlc-maximum-length-of-repeated-subarray-2-code
node: b.maximum-length-of-repeated-subarray
type: qa
step: 2
---
## Q
**LC 718 最长重复子数组**｜写出 Python 实现

两个整数数组 `nums1`、`nums2`，长度都在 `[1, 1000]`，值在 `[0, 100]`。返回两个数组公共的最长**连续**子数组的长度，要求 `O(m·n)` 时间，空间尽量小。

## A
**思路。** `dp[j]` 保存"以 `nums1` 当前元素、`nums2[j-1]` 结尾"的公共子数组长度。逐个取 `nums1` 的元素 `x`，`j` 从大到小：相等则 `dp[j] = dp[j-1] + 1`（此时 `dp[j-1]` 仍是上一个元素对应的值），不等则清零；同时维护最大值。

```python
def find_length(nums1: list[int], nums2: list[int]) -> int:
    m = len(nums2)
    dp = [0] * (m + 1)                     # dp[j]：以 nums1 当前元素、nums2[j-1] 结尾的最长公共子数组长度
    best = 0
    for x in nums1:
        for j in range(m, 0, -1):          # 倒序：dp[j-1] 还是上一行的值
            if x == nums2[j - 1]:
                dp[j] = dp[j - 1] + 1
                best = max(best, dp[j])
            else:
                dp[j] = 0                  # 子数组必须连续，不相等就断开
    return best
```

运行：`([1,2,3,2,1], [3,2,1,4,7])` → `3`，`([0]*5, [0]*5)` → `5`，`([1], [2])` → `0`，`([1,2,3], [1,3])` → `1`；两个 `1000` 个元素的随机数组约 `0.02` 秒，全零数组约 `0.04` 秒。

**复杂度。** 时间 `O(m·n)`，约 `10^6` 次比较；空间 `O(n)`，`n = len(nums2)`。

**写法要点。** `dp = [0] * (m + 1)` 多留一个哨兵位 `dp[0] = 0`，让 `dp[j-1]` 在 `j = 1` 时不越界；`for x in nums1` 直接迭代元素，省掉 `nums1[i-1]`；`range(m, 0, -1)` 的倒序是一维压缩的关键，因为新值依赖左上角（上一行的 `j-1`），正序会提前覆盖；`best` 只在匹配时更新，不匹配的格子是 `0`，不会比 `best` 更大。
