---
id: tlc-median-of-two-sorted-arrays-5-alt
node: a.median-of-two-sorted-arrays
type: qa
step: 5
---
## Q
**LC 4 寻找两个正序数组的中位数**｜另一种解法

除了在较短数组上二分切割点，还有什么 `O(log(m + n))` 的做法？再给一个更直接、数据小时能过的做法，并说明怎么选。

## A
**第 `k` 小的逐步排除。** 中位数就是第 `k` 小。每轮比较两个数组的第 `k // 2` 个元素，较小的那一边的前 `k // 2` 个元素一定排在第 `k` 小之前，可以整段丢掉，`k` 减去丢掉的个数；`k` 缩小到 `1`，或有一个数组用完时结束。每轮 `k` 至少减半，`O(log(m + n))`。

```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    def kth(k: int) -> int:             # 两个数组合并后第 k 小（k 从 1 开始）
        i = j = 0
        while True:
            if i == len(nums1):
                return nums2[j + k - 1]
            if j == len(nums2):
                return nums1[i + k - 1]
            if k == 1:
                return min(nums1[i], nums2[j])
            step = k // 2
            ni, nj = min(i + step, len(nums1)), min(j + step, len(nums2))
            if nums1[ni - 1] <= nums2[nj - 1]:      # nums1[i:ni] 都排在第 k 小之前，整段丢掉
                k -= ni - i
                i = ni
            else:
                k -= nj - j
                j = nj

    total = len(nums1) + len(nums2)
    if total % 2:
        return float(kth(total // 2 + 1))
    return (kth(total // 2) + kth(total // 2 + 1)) / 2
```

`([1,3], [2])` → `2.0`，`([1,2], [3,4])` → `2.5`。

**数据小时的直接做法。** `m + n <= 2000`，合并后取中间只需线性时间，用 `heapq.merge` 加 `islice` 几行就能写完：`list(islice(merge(a, b), (total - 1) // 2, total // 2 + 1))` 取出中间的一个或两个数，求平均。

**怎么选。** 面试要求对数级时，切割法最短，边界靠 `±inf` 哨兵；逐步排除法思路好讲，还直接给出第 `k` 小；线性合并只作为先讲清楚模型的第一步。
