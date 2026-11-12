---
slug: reverse-subarray-to-maximize-array-value
---
## Q
**LC 1330 翻转子数组得到最大的数组值**｜Hard

数组值是所有相邻差的绝对值之和。可以翻转一次任意子数组，求最大数组值。

## A
**一句话。** 翻转只改变子数组两端的两条相邻差；翻转在中间时增益是 `2*(最大的线段左端点 - 最小的线段右端点)`，贴着端点时直接算一条边的变化。

```python
def max_value_after_reverse(nums):
    n = len(nums)
    total = sum(abs(a - b) for a, b in pairwise(nums))
    lo = max(min(a, b) for a, b in pairwise(nums))
    hi = min(max(a, b) for a, b in pairwise(nums))
    gain = max(0, 2 * (lo - hi))         # 翻转区间在中间
    for i in range(1, n):                # 翻转区间顶着端点
        d = abs(nums[i-1] - nums[i])
        gain = max(gain,
                   abs(nums[0] - nums[i]) - d,
                   abs(nums[-1] - nums[i-1]) - d)
    return total + gain
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉贴着端点的情形：`[1,5,4]` 只算中间情形得 `5`，翻转 `[1,5]` 才得 `7`。
- 增益写成 `2*(全局最大 - 全局最小)`：`[2,3,1,5,4]` 得 `16`，应为 `10`。

**追问。**
- 为什么内部相邻差不变？：`|a-b| = |b-a|`，翻转后内部相邻对只是反向。
- 要返回具体的 `(l, r)`？：记录取到最大左端点和最小右端点的线段下标，翻转它们之间。

**同模式。** LC 1014 最佳观光组合、LC 121 买卖股票的最佳时机、LC 53 最大子数组和
