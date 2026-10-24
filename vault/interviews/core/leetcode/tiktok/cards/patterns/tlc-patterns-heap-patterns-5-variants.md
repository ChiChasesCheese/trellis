---
id: tlc-patterns-heap-patterns-5-variants
node: patterns.heap-patterns
type: qa
step: 5
---
## Q
**堆（Heap）｜变形：K 路归并、双堆调度（会议室 III）、值域上的堆**

合并 K 个链表、有序矩阵第 `k` 小、会议室 III（LC 2402）分别在堆里放什么？

## A
1. **K 路归并（LC 23）**：堆里每路一个元素 `(值, 路号, 节点)`；弹出最小的，把该路的下一个压入。时间 `O(N log k)`。

2. **有序矩阵第 `k` 小（LC 378，堆法）**：把每行的第一个元素 `(值, 行, 列)` 入堆，弹出 `k - 1` 次，每次把该行的下一个元素压入；`O(k log n)`。值域二分是另一种解法。

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

3. **双堆调度（LC 2402 会议室 III）**：空闲房间号的最小堆 + 正在使用的 `(结束时间, 房间号)` 最小堆。每场会议前，先把 `结束时间 <= 开始时间` 的房间还到空闲堆；有空房取编号最小的；没有就取最早结束的房间，会议顺延 `t + (end - start)`。

```python
def best_meeting_room(n: int, meetings: list[list[int]]) -> int:
    meetings.sort()
    free = list(range(n))
    busy: list[tuple[int, int]] = []
    cnt = [0] * n
    for start, end in meetings:
        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (end, room))
        else:
            t, room = heapq.heappop(busy)
            heapq.heappush(busy, (t + end - start, room))
        cnt[room] += 1
    return cnt.index(max(cnt))                 # index 返回第一个最大值，即编号最小
print(best_meeting_room(2, [[0,10],[1,5],[2,7],[3,4]]), best_meeting_room(3, [[1,20],[2,10],[3,5],[4,9],[6,8]]))   # 0 1
```

4. **频次聚合取最值（LC 347、2456）**：`Counter` / 字典聚合后用 `heapq.nlargest(k, cnt, key=cnt.get)`；LC 2456 只需遍历一遍求最大值，堆不是必需。
