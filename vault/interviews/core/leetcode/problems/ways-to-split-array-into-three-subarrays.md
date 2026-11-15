---
slug: ways-to-split-array-into-three-subarrays
---
## Q
**LC 1712 将数组分成三个子数组的方案数**｜Medium

非负整数数组切成非空的 `left`、`mid`、`right` 三段，要求 `sum(left) <= sum(mid) <= sum(right)`。求方案数，对 `10^9+7` 取余。

## A
**一句话。** 前缀和非降，枚举 `left` 的结尾 `i`，第二刀 `j` 的合法范围是一段连续区间 `2·p[i] <= p[j] <= (total+p[i])/2`，两次二分求出区间长度。

```python
def ways_to_split(nums):
    p = list(accumulate(nums, initial=0))
    n, total, ans = len(nums), p[-1], 0
    for i in range(1, n - 1):          # left = nums[:i]
        a = p[i]
        if a * 3 > total:               # left 太大，后面更大
            break
        # mid = nums[i:j]，j 在 [i+1, n-1]
        lo = max(bisect_left(p, 2 * a), i + 1)
        hi = min(bisect_right(p, (total + a) // 2), n)
        ans += max(0, hi - lo)
    return ans % (10**9 + 7)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 忘了 `lo >= i+1`：全 `0` 数组时 `bisect_left` 返回 `0`，`mid` 会变空。
- 忘了 `hi <= n`：`j = n` 时 `right` 为空，要截到 `n-1` 为止。

**追问。**
- 不用二分？：`i` 右移时 `lo` 与 `hi` 都只会右移，三指针一次扫完，`O(n)`。
- 为什么 `(total+a)//2` 能直接取整？：都是整数，`2p[j] <= total+a` 等价于 `p[j] <=` 向下取整的一半。

**同模式。** LC 209 长度最小的子数组、LC 1013 将数组分成和相等的三个部分、LC 2270 分割数组的方案数
