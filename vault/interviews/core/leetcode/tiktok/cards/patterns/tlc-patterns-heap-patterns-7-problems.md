---
id: tlc-patterns-heap-patterns-7-problems
node: patterns.heap-patterns
type: qa
step: 7
---
## Q
**堆（Heap）｜本组用到堆的题**

按变形分类，这个题组里哪些题用到堆？

## A
**Top-K / 第 K 个**
- LC 215 数组中的第 K 个最大元素
- LC 347 前 K 个高频元素
- LC 378 有序矩阵中第 K 小的元素

**K 路归并**
- LC 23 合并 K 个升序链表

**双堆 / 数据流**
- LC 295 数据流的中位数

**按时间调度（排序 + 堆装结束时间）**
- LC 253 会议室 II
- LC 1834 单线程 CPU（高频）

**每次取当前最大 / 最小的贪心**
- LC 767 重构字符串

**聚合后取最值（堆可选）**

**堆 + 最短路**
- LC 787 K 站中转内最便宜的航班（见最短路一组）
- LC 778 水位上升的泳池中游泳（高频）

提示：先写出「每一步要从剩余的东西里取哪个最值」，再决定存什么键、是否要暂存刚用过的项、是否需要懒删除。

**例题：** LC 215 数组中的第 K 个最大元素

给整数数组 `nums`（长度 `<= 10^5`）和 `k`，返回排序后的第 `k` 个最大元素（重复值各算一个）。

```python
import random
def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):
            nums = bigger
        elif k <= len(bigger) + equal:
            return pivot
        else:
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

**例题：** LC 347 前 K 个高频元素

给整数数组 `nums`（长度 `<= 10^5`）和 `k`，返回出现次数最多的前 `k` 个元素，顺序任意，答案唯一。

```python
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

**例题：** LC 378 有序矩阵中第 K 小的元素

给 `n x n` 矩阵（`n <= 300`），每行每列都非递减，返回排序后的第 `k` 小的元素（重复值各算一个）。

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    def count_le(mid: int) -> int:
        count, col = 0, n - 1
        for row in matrix:
            while col >= 0 and row[col] > mid:
                col -= 1
            count += col + 1
        return count
    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 23 合并 K 个升序链表

给 `k` 个升序链表（`k <= 10^4`，总长度 `<= 10^4`），合并成一个升序链表并返回。

```python
import heapq
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]
        tail.next = node
        tail = node
        if node.next:
            heapq.heapreplace(heap, (node.next.val, i, node.next))
        else:
            heapq.heappop(heap)
    return dummy.next
```

**例题：** LC 295 数据流的中位数

实现 `MedianFinder`：`addNum(num)` 加入一个整数，`findMedian()` 返回目前所有数的中位数；最多 `5 * 10^4` 次调用。

```python
from heapq import heappop, heappush, heappushpop
class MedianFinder:
    def __init__(self) -> None:
        self.low: list[int] = []
        self.high: list[int] = []
    def addNum(self, num: int) -> None:
        heappush(self.high, -heappushpop(self.low, -num))
        if len(self.high) > len(self.low):
            heappush(self.low, -heappop(self.high))
    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```

**例题：** LC 253 会议室 II

给会议时间区间 `intervals`（`<= 10^4` 个，`0 <= start < end <= 10^6`），求同时进行的会议数的最大值，即最少需要的会议室数；一个会议结束的时刻可以立刻开始下一个。

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)
```

**例题：** LC 767 重构字符串

给小写字母字符串 `s`（长度 `<= 500`），重新排列使相邻字符都不同，返回任意一种排列，不可能则返回 `""`。

```python
from collections import Counter
from heapq import heapify, heappop, heappush
def reorganize_string(s: str) -> str:
    heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]
    heapify(heap)
    out: list[str] = []
    held = (0, "")
    while heap:
        cnt, ch = heappop(heap)
        out.append(ch)
        if held[0]:
            heappush(heap, held)
        held = (cnt + 1, ch)
    return "".join(out) if len(out) == len(s) else ""
```

**例题：** LC 787 K 站中转内最便宜的航班

`n` 个城市（`n <= 100`）和带价格的有向航班，求从 `src` 到 `dst` 最多经过 `k` 次中转的最便宜价格，不存在返回 `-1`。

```python
from math import inf
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0
    for t in range(1, k + 2):
        dp[t] = dp[t - 1][:]
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

**例题：** LC 1834 单线程 CPU

`tasks[i] = [enqueueTime, processingTime]`；CPU 空闲时从已到达的任务里选执行时间最短的（并列取下标最小），一次只做一项且不可中断；返回任务的执行顺序；`1 <= n <= 10^5`，时间 `<= 10^9`。

```python
from heapq import heappop, heappush
def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap: list[tuple[int, int]] = []
    res: list[int] = []
    t = p = 0
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)
        t += cost
        res.append(i)
    return res
```

**例题：** LC 778 水位上升的泳池中游泳

`n x n` 矩阵 `grid[i][j]` 是平台高度，时刻 `t` 的水位是 `t`，只有水位不低于相邻两平台的高度时才能游过去；返回从 `(0, 0)` 到 `(n-1, n-1)` 的最少时间；`1 <= n <= 50`，高度互不相同。

```python
from heapq import heappop, heappush
def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)
        if x == y == n - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                seen.add((nx, ny))
                heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return -1
```
