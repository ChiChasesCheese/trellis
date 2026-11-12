---
slug: maximum-value-at-a-given-index-in-a-bounded-array
---
## Q
**LC 1802 有界数组中指定下标处的最大值**｜Medium

构造长度 `n` 的正整数数组，相邻元素之差不超过 `1`，总和不超过 `maxSum`。使 `nums[index]` 最大，返回这个最大值。

## A
**一句话。** 二分答案：峰值为 `v` 时两侧逐格降 `1`、降到 `1` 后补 `1` 得最小和，找最小和不超过 `maxSum` 的最大 `v`。

```python
def max_value(n, index, max_sum):
    def side(peak, length):      # 峰值一侧 length 格的最小和
        if length >= peak - 1:   # 降到 1 后全补 1
            tri = peak * (peak - 1) // 2
            return tri + length - peak + 1
        return (peak - 1 + peak - length) * length // 2

    def total(peak):
        left = side(peak, index)
        return peak + left + side(peak, n - 1 - index)

    lo, hi = 1, max_sum
    while lo < hi:
        mid = (lo + hi + 1) // 2   # 上取整，避免死循环
        if total(mid) <= max_sum:
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(log maxSum)`，空间 `O(1)`。

**易错点。**
- 一侧只用等差数列、不补 `1`：`(3, 0, 3)` 峰值 `2` 误判可行得 `2`，真实最小和是 `4`，应为 `1`。
- `mid = (lo + hi) // 2` 配 `lo = mid`：`lo + 1 == hi` 时死循环，求最大可行要上取整。
- `total` 里漏了峰值本身。

**追问。**
- 相邻差上限改成 `d`？：每格最多降 `d`，等差数列公差换成 `d`。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 69 x 的平方根、LC 2517 礼盒的最大甜蜜度
