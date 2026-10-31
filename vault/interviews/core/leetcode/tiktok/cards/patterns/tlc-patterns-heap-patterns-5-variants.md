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

3. **双堆调度（LC 2402 会议室 III）**：空闲房间号的最小堆 + 正在使用的 `(结束时间, 房间号)` 最小堆。每场会议前，先把 `结束时间 <= 开始时间` 的房间还到空闲堆；有空房取编号最小的；没有就取最早结束的房间，会议顺延 `t + (end - start)`（例：LC 2402 会议室 III）。

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

4. **频次聚合取最值（LC 347、2456）**：`Counter` / 字典聚合后用 `heapq.nlargest(k, cnt, key=cnt.get)`；LC 2456 只需遍历一遍求最大值，堆不是必需（例：LC 347 前 K 个高频元素）。

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

**例题：** LC 2402 会议室 III

`n` 个会议室（`1 <= n <= 100`）编号 `0..n-1`，`meetings[i] = [start, end)`（至多 `10^5` 场，`start` 互不相同）。每场会议用编号最小的空闲房间；没有空房就延期到有房间空出，时长不变。返回举办会议最多的房间，并列取编号最小。

```python
from heapq import heappop, heappush
def most_booked(n: int, meetings: list[list[int]]) -> int:
    free = list(range(n))                      # 空闲房间号的最小堆（升序列表本身就是堆）
    busy: list[tuple[int, int]] = []           # (结束时间, 房间号) 的最小堆
    count = [0] * n
    for start, end in sorted(meetings):        # 按开始时间依次安排
        while busy and busy[0][0] <= start:    # 区间半开：结束时间 == start 的房间已空
            heappush(free, heappop(busy)[1])
        if free:
            room = heappop(free)               # 编号最小的空房间
            finish = end
        else:
            ready, room = heappop(busy)        # 最早空出来的房间（同时空出取编号小）
            finish = ready + (end - start)     # 延期：时长不变，从 ready 开始
        count[room] += 1
        heappush(busy, (finish, room))
    return max(range(n), key=count.__getitem__)   # max 取并列里第一个，即编号最小
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
