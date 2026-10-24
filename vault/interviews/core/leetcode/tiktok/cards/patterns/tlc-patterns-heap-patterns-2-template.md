---
id: tlc-patterns-heap-patterns-2-template
node: patterns.heap-patterns
type: qa
step: 2
---
## Q
**堆（Heap）｜模板：会议室 II 与 Top-K**

写出「按开始时间排序、堆装结束时间」的最少会议室数量，以及定长堆求第 `k` 大的模板。

## A
**按时间调度（LC 253）**：每开始一场会议，看最早结束的会议室是否已空闲。

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    intervals = sorted(intervals)          # 按开始时间排序
    ends: list[int] = []                   # 最小堆：正在使用的会议室的结束时间
    for start, end in intervals:
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)   # 最早结束的会议室已空闲：复用，换成新的结束时间
        else:
            heapq.heappush(ends, end)      # 没有空闲：新开一间
    return len(ends)
```

运行：`[[0,30],[5,10],[15,20]]` → `2`；`[[7,10],[2,4]]` → `1`；`[[1,5],[5,9]]` → `1`（首尾相接可复用）。时间 `O(n log n)`，空间 `O(n)`。

**Top-K（LC 215）**：只保留最大的 `k` 个，用最小堆，堆顶就是第 `k` 大。

```python
def find_kth_largest(nums: list[int], k: int) -> int:
    h: list[int] = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)        # 替掉当前第 k 大
    return h[0]
print(find_kth_largest([3,2,1,5,6,4], 2), find_kth_largest([3,2,3,1,2,4,5,5,6], 4))   # 5 4
```

时间 `O(n log k)`，空间 `O(k)`。

- 「堆顶是 `k` 个里最小的」：求第 `k` 大用**最小堆**，求第 `k` 小用最大堆（存负数）。
- `ends[0] <= start` 用 `<=`：结束时间等于开始时间的会议可以复用同一间。
