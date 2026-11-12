---
slug: find-k-th-smallest-pair-distance
---
## Q
**LC 719 找出第 k 小的距离对**｜Hard

数对 `(i, j)`（`i < j`）的距离是 `|nums[i] - nums[j]|`。求所有数对距离中第 `k` 小的。

## A
**一句话。** 对距离值二分答案：排序后用双指针数出距离 `<= d` 的数对数，找最小的 `d` 使个数 `>= k`。

```python
def smallest_distance_pair(nums, k):
    nums.sort()

    def count(d):                  # 距离 <= d 的数对数
        c = left = 0
        for r, x in enumerate(nums):
            while x - nums[left] > d:
                left += 1
            c += r - left
        return c

    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log n + n log V)`，空间 `O(1)`。

**易错点。**
- 忘了先排序：双指针计数要求有序，`[2,6,2,4]`、`k = 4` 会得 `4`，应为 `2`。
- 条件写成 `count(mid) > k`：找的是第一个 `>= k` 的 `d`，`[2,7,8]`、`k = 1` 会得 `5`，应为 `1`。
- 下界取 `1`：距离可以是 `0`，`[1,1,1]`、`k = 2` 应为 `0`。

**追问。**
- `k` 很小怎么办？：最小堆多路归并，弹 `k` 次，`O((n + k) log n)`。
- 同一模板还能做什么？：LC 378 有序矩阵第 K 小、LC 668 乘法表第 k 小。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 668 乘法表中第 k 小的数、LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力
