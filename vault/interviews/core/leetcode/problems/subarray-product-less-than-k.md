---
slug: subarray-product-less-than-k
---
## Q
**LC 713 乘积小于 K 的子数组**｜Medium

正整数数组 `nums`，数出元素乘积严格小于 `k` 的连续子数组个数。

## A
**一句话。** 滑动窗口：右端逐个右移，乘积 `>= k` 就收缩左端，以右端结尾的合法子数组恰有窗口长度个。

```python
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:    # 元素都 >= 1，乘积不可能 < k
        return 0
    ans = left = 0
    prod = 1
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]
            left += 1
        ans += right - left + 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉 `k <= 1` 特判：`([1,1,1], 1)` 时 `left` 越过数组末尾，`IndexError`。
- 每步只 `ans += 1`：只数了窗口，`([10,5,2,6], 100)` 得 `4`，应为 `8`。
- 用 `/` 更新乘积：浮点误差让 `prod >= k` 判断出错，用 `//`。

**追问。**
- 有 `0` 或负数呢？：单调性消失，`0` 可切段；一般情况对数转前缀和加二分，也只对全正数有效。
- 不想做除法？：对 `log(nums[i])` 求前缀和，每个右端二分最小左端，`O(n log n)`，注意浮点精度。

**同模式。** LC 209 长度最小的子数组、LC 3 无重复字符的最长子串、LC 904 水果成篮、LC 560 和为 K 的子数组
