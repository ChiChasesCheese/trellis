---
slug: minimum-sum-of-squared-difference
---
## Q
**LC 2333 最小差值平方和**｜Medium

两个正整数数组 `nums1`、`nums2`。差平方和 `Σ (nums1[i] - nums2[i])²`。可以对 `nums1` 的元素做最多 `k1` 次 ±1，对 `nums2` 的元素做最多 `k2` 次 ±1（可以变成负数）。求最小的差平方和。

## A
**一句话。** 每次 ±1 等价于让某个绝对差 `|d|` 减 `1`，共 `k = k1 + k2` 次；贪心每次减当前最大的 `|d|`，批量处理：把最大的几个"削平"到下一个高度。

```python
def min_sum_square_diff(nums1, nums2, k1, k2):
    d = sorted((abs(a - b) for a, b in zip(nums1, nums2)),
               reverse=True)
    k = k1 + k2
    if sum(d) <= k:
        return 0
    d.append(0)
    for i in range(len(d) - 1):
        cost = (i + 1) * (d[i] - d[i + 1])   # 前 i+1 个削平到 d[i+1]
        if k >= cost:
            k -= cost
        else:                                 # 削不完：均匀减
            q, r = divmod(k, i + 1)
            level = d[i] - q
            rest = sum(x * x for x in d[i + 1:])
            return (r * (level - 1) ** 2
                    + (i + 1 - r) * level ** 2 + rest)
    return 0
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用堆逐次减 `1`：`k` 可达 `10^9`，必须批量削平。
- 削不完时漏掉余数 `r`：有 `r` 个元素要再多减 `1`，值是 `level - 1`。

**追问。**
- 为什么先削最大的？：平方是凸函数，同样的减量，在大的数上节省更多。

**同模式。** LC 1648 销售价值减少的颜色球、LC 1647 字符频次唯一的最小删除次数、LC 462 最小操作次数使数组元素相等 II
