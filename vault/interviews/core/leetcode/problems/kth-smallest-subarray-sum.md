---
slug: kth-smallest-subarray-sum
---
## Q
**LC 1918 第 K 小的子数组和**｜Medium

正整数数组 `nums`，返回所有非空连续子数组的和中第 `k` 小的（不同位置的子数组各算一个）。

## A
**一句话。** 对答案二分，元素为正，用双指针数「和不超过 `x` 的子数组个数」，找最小的 `x` 使个数 `>= k`。

```python
def kth_smallest_subarray_sum(nums, k):
    def count_le(x):               # 和 <= x 的子数组个数
        cnt = left = cur = 0
        for r, v in enumerate(nums):
            cur += v
            while cur > x:
                cur -= nums[left]
                left += 1
            cnt += r - left + 1    # 以 r 结尾的合法子数组
        return cnt

    lo, hi = min(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log S)`，空间 `O(1)`。

**易错点。**
- 判定写成 `count_le(mid) > k`：`([2,1,3],4)` 得 `4`，应为 `3`，等于也要收。
- 上界取 `max(nums)`：`([2,1,3],6)` 得 `3`，应为 `6`，上界要 `sum(nums)`。

**追问。**
- 数组含负数怎么办？：窗口和不再单调，改用前缀和排序后二分，`O(n log n log S)`。
- `k` 很小、`n` 很大呢？：最小堆多路归并，`O(k log n)`。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 668 乘法表中第 k 小的数、LC 719 找出第 K 小的数对距离、LC 786 第 K 个最小的素数分数
