---
id: tlc-patterns-heap-patterns-5-variants
node: patterns.heap-patterns
type: qa
step: 5
---
## Q
**堆（Heap）｜变形：K 路归并、就绪堆调度（单线程 CPU）、值域上的堆**

合并 K 个链表、有序矩阵第 `k` 小、单线程 CPU（LC 1834）分别在堆里放什么？

## A
1. **K 路归并（LC 23）**：堆里每路一个元素 `(值, 路号, 节点)`；弹出最小的，把该路的下一个压入。时间 `O(N log k)`（例：LC 23 合并 K 个升序链表）。

2. **有序矩阵第 `k` 小（LC 378，堆法）**：把每行的第一个元素 `(值, 行, 列)` 入堆，弹出 `k - 1` 次，每次把该行的下一个元素压入；`O(k log n)`。值域二分是另一种解法（例：LC 378 有序矩阵中第 K 小的元素）。

```python
import heapq
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    h = [(matrix[r][0], r, 0) for r in range(min(n, k))]
    heapq.heapify(h)
    for _ in range(k - 1):
        v, r, c = heapq.heappop(h)
        if c + 1 < n:
            heapq.heappush(h, (matrix[r][c + 1], r, c + 1))
    return h[0][0]
print(kth_smallest([[1,5,9],[10,11,13],[12,13,15]], 8))   # 13
```

3. **就绪堆 + 事件推进（LC 1834 单线程 CPU）**：任务按入队时间排序，用指针推进；CPU 空闲时把此刻已到达的任务压进以 `(执行时间, 下标)` 为键的最小堆，弹出堆顶执行；堆空而下一个任务还没到，时间直接跳到它的到达时刻，不逐秒模拟。每个任务入堆、出堆各一次，`O(n log n)`（例：LC 1834 单线程 CPU；高频：LC 253 会议室 II）。

```python
def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap: list[tuple[int, int]] = []           # (执行时间, 下标)：元组比较先时间后下标
    res: list[int] = []
    t = p = 0
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]             # 空闲且队列空：时间跳到下一个到达时刻
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heapq.heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heapq.heappop(heap)
        t += cost
        res.append(i)
    return res
print(get_order([[1,2],[2,4],[3,2],[4,1]]), get_order([[7,10],[7,12],[7,5],[7,4],[7,2]]))   # [0, 2, 3, 1] [4, 3, 2, 0, 1]
```

4. **频次聚合取最值（LC 347）**：`Counter` / 字典聚合后用 `heapq.nlargest(k, cnt, key=cnt.get)`；只要最大值时遍历一遍即可，堆不是必需（例：LC 347 前 K 个高频元素）。

**例题：** LC 23 合并 K 个升序链表

`lists` 是 `k` 个升序链表（`0 <= k <= 10^4`，所有链表长度之和不超过 `10^4`），把它们合并成一个升序链表。

```python
import heapq
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]            # 堆顶就是当前最小的队头
        tail.next = node
        tail = node
        if node.next:                   # 该链表还有后继：原地替换堆顶，只做一次下沉
            heapq.heapreplace(heap, (node.next.val, i, node.next))
        else:
            heapq.heappop(heap)
    return dummy.next
```

**例题：** LC 378 有序矩阵中第 K 小的元素

`n x n` 矩阵（`1 <= n <= 300`）每行每列都按升序排列，求排序后第 `k` 小的元素（`1 <= k <= n^2`，重复元素各算一个），要求内存优于 `O(n^2)`。

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    def count_le(mid: int) -> int:             # 矩阵中 <= mid 的元素个数，阶梯式 O(n)
        count, col = 0, n - 1
        for row in matrix:                     # 行从上到下，每行的列边界只会左移
            while col >= 0 and row[col] > mid:
                col -= 1
            count += col + 1
        return count
    lo, hi = matrix[0][0], matrix[-1][-1]      # 答案一定落在 [最小值, 最大值]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:                 # 至少有 k 个数 <= mid：答案 <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 1834 单线程 CPU

`tasks[i] = [enqueueTime, processingTime]`（`1 <= n <= 10^5`，两个值都 `<= 10^9`）：单线程 CPU 空闲时从已入队的任务里选执行时间最短的，并列选下标最小的，任务一旦开始就执行完；返回任务的执行顺序。

```python
from heapq import heappop, heappush
def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])   # 任务下标按入队时间排好
    heap: list[tuple[int, int]] = []                      # (执行时间, 下标)：元组比较天然先时间后下标
    res: list[int] = []
    t = p = 0                                             # t：当前时刻；p：下一个还没入队的任务在 order 里的位置
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]                        # CPU 空闲且队列空：时间直接跳到下一个任务到达
        while p < n and tasks[order[p]][0] <= t:          # 此刻已到达的任务全部入堆
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)                           # 取执行时间最短的；并列时下标小的先出
        t += cost
        res.append(i)
    return res
```

**例题：** LC 347 前 K 个高频元素

整数数组 `nums`（`1 <= nums.length <= 10^5`）和 `k`，返回出现频率前 `k` 高的元素，顺序不限；进阶要求时间优于 `O(n log n)`。

```python
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # 下标 = 出现次数
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):          # 从高频到低频
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

**例题：** LC 253 会议室 II

给一个会议时间数组 `intervals`，`intervals[i] = [start_i, end_i]`，返回需要的最少会议室数量。一个会议结束的时刻可以立刻开始下一个会议。`1 <= intervals.length <= 10^4`，`0 <= start_i < end_i <= 10^6`。

```python
import heapq


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []                           # 小根堆：每个在用会议室的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:              # 最早结束的会议已结束：复用它的房间
            heapq.heapreplace(ends, end)           # 弹出旧结束时间并压入新的，一次 O(log n)
        else:
            heapq.heappush(ends, end)              # 没有空房间：新开一间
    return len(ends)                               # 堆里剩几个 = 同时在用的房间数峰值
```
