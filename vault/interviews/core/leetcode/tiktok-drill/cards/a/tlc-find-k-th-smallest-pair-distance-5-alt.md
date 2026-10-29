---
id: tlc-find-k-th-smallest-pair-distance-5-alt
node: a.find-k-th-smallest-pair-distance
type: qa
step: 5
---
## Q
**LC 719 找出第 k 小的距离对**｜另一种解法

不做二分答案，能不能用堆（heap）直接取出第 `k` 小的距离？它和二分答案相比，什么时候该选哪个？

## A
**思路。** 排序后，对每个 `i`，距离序列 `nums[i+1] - nums[i]`、`nums[i+2] - nums[i]`、... 是递增的。把每条序列的当前头放进最小堆，每次弹出最小的距离，并把它所在序列的下一个元素推进去；弹出 `k` 次，第 `k` 次弹出的就是答案。这和「合并 `k` 个有序链表」是同一个模式。

```python
import heapq


def smallest_distance_pair_heap(nums: list[int], k: int) -> int:
    nums = sorted(nums)
    n = len(nums)
    # 每个 i 对应一条递增序列：nums[j] - nums[i]，j = i+1, i+2, ...；堆里放每条序列当前的头
    heap = [(nums[i + 1] - nums[i], i, i + 1) for i in range(n - 1)]
    heapq.heapify(heap)
    for _ in range(k - 1):                      # 弹出前 k - 1 小，第 k 次弹出的就是答案
        d, i, j = heapq.heappop(heap)
        if j + 1 < n:
            heapq.heappush(heap, (nums[j + 1] - nums[i], i, j + 1))
    return heap[0][0]
```

运行：`[1,3,1]`、`k = 1` → `0`；`[1,1,1]`、`k = 2` → `0`；`[1,6,1]`、`k = 3` → `5`。

**为什么对。** 每条序列有序，堆顶永远是所有序列头部里最小的，也就是尚未弹出的全部距离里最小的；所以第 `j` 次弹出的恰是第 `j` 小的距离。代码弹出 `k - 1` 次后，堆顶 `heap[0]` 就是第 `k` 小。

**取舍。** 堆法时间 `O(n + k log n)`，思路直观，`k` 小时（如 `k <= 10^5`）比二分更快；但 `k` 最大可达 `n(n-1)/2 ≈ 5 * 10^7`，堆要弹 `5 * 10^7` 次，在 Python 里不可接受。二分答案只依赖 `n` 与值域，`k` 多大都一样快。`n` 很小（如 `<= 2000`）时，直接 `sorted(abs(a - b) for a, b in combinations(nums, 2))[k - 1]` 最不容易写错。
