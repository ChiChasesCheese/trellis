---
id: tlc-kth-smallest-subarray-sum-4-followup
node: p4.kth-smallest-subarray-sum
type: qa
step: 4
---
## Q
**LC 1918 第 K 小的子数组和**｜追问

面试官接着问：（1）改成第 `k` **大**？（2）`k` 很小而 `n` 很大，有没有比二分更快的？（3）数组里可能有 `0` 或负数？分别怎么改。

## A
1. **第 `k` 大**：总共有 `m = n(n+1)/2` 个子数组，第 `k` 大就是第 `m - k + 1` 小，直接调用原函数 `kth_smallest_subarray_sum(nums, m - k + 1)`。
2. **`k` 小**：用最小堆做多路归并。对每个起点 `i`，从 `nums[i]` 开始的子数组和随长度递增，把 `(nums[i], i, i)` 作为初始元素放进堆，弹出 `(s, i, j)` 后推入 `(s + nums[j+1], i, j+1)`，弹出 `k` 次就是第 `k` 小，`O((n + k) log n)`。`k` 接近 `n(n+1)/2` 时退化，不如二分。
3. **含 `0`**：窗口和非严格单调，同一套双指针依然正确（`cur > x` 才收缩）。**含负数**：窗口和不单调，改用前缀和：子数组和 `= pre[r] - pre[l]`，和 `<= x` 的对数可以在对前缀和排序、或归并排序的过程中数出，每次判定 `O(n log n)`，总 `O(n log n log S)`。

```python
import heapq


def kth_smallest_heap(nums: list[int], k: int) -> int:
    heap = [(v, i, i) for i, v in enumerate(nums)]      # (子数组和, 起点, 终点)
    heapq.heapify(heap)
    for _ in range(k - 1):
        s, i, j = heapq.heappop(heap)
        if j + 1 < len(nums):
            heapq.heappush(heap, (s + nums[j + 1], i, j + 1))
    return heap[0][0]
```

   `([2,1,3], 4)` → `3`，`([3,3,5,5], 7)` → `10`。

**Python 提醒**：`heapq.heapify` 是 `O(n)`，比逐个 `heappush` 的 `O(n log n)` 快；堆里的元组在和相同时会比较后面的下标，下标都是整数，不会报错。
