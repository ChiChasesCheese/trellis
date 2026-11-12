---
slug: find-k-closest-elements
---
## Q
**LC 658 找到 K 个最接近的元素**｜Medium

升序数组 `arr`，求最接近 `x` 的 `k` 个数（距离相同取小的），按升序返回。

## A
**一句话。** 答案是长度为 `k` 的连续窗口，二分窗口左端点：比较 `arr[mid]` 与 `arr[mid+k]` 谁离 `x` 更近。

```python
def find_closest_elements(arr, k, x):
    lo, hi = 0, len(arr) - k      # 左端点范围 [0, n-k]
    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:   # 右侧更近，窗口右移
            lo = mid + 1
        else:                     # 相等取小的，所以不右移
            hi = mid
    return arr[lo:lo + k]
```

**复杂度。** 时间 `O(log(n-k) + k)`，空间 `O(1)`。

**易错点。**
- 平局方向写反：`[1,3], k=1, x=2` 应为 `[1]`，把 `>` 写成 `>=` 得 `[3]`。
- 上界写成 `len(arr)-1`：`mid+k` 越界，左端点最大只能是 `n-k`。

**追问。**
- 数组没排序呢？：`heapq.nsmallest(k, arr, key=lambda a: (abs(a-x), a))`，`O(n log k)`。
- 另一种思路？：先二分找到 `x` 的位置，再双指针向两边扩展 `k` 步。

**同模式。** LC 34 排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置、LC 719 找出第 K 小的数对距离、LC 215 数组中的第K个最大元素
