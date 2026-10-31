---
id: tlc-patterns-heap-patterns-1-signals
node: patterns.heap-patterns
type: qa
step: 1
---
## Q
**堆（Heap）｜信号**

什么样的题面该想到堆？Top-K、K 路归并、双堆、按时间调度分别由什么信号触发？哪些近似信号不需要堆？

## A
**堆的核心能力**：在动态变化的集合里，`O(log n)` 取出并删除最小（或最大）元素。

**信号：**
- 「**前 `k` 个最小 / 最大**的组合」：大小为 `k` 的堆，`O(n log k)`，不需要把所有组合都生成出来（例：LC 373 查找和最小的 K 对数字）。
- 「**合并 `k` 个有序**链表 / 数组」：堆里每路放一个当前头（例：LC 23 合并 K 个升序链表）。
- 「**数据流的中位数**」：一个最大堆装较小的一半，一个最小堆装较大的一半（例：LC 295 数据流的中位数）。
- 「**事件按时间顺序处理**」：会议室、任务调度、最早可用的资源：按开始时间排序，堆装结束时间（LC 253、2402）（例：LC 253 会议室 II）。
- 「**每次取当前最大 / 最小的可用项，再放回**」的贪心：重构字符串 LC 767、最长快乐字符串 LC 1405（例：LC 767 重构字符串）。
- Dijkstra 的边界选择（见最短路一组）（例：LC 778 水位上升的泳池中游泳）。

**近似信号：**
- 只要一次最小 / 最大 → `min` / `max`：扫描时只要记住迄今最小值（例：LC 121 买卖股票的最佳时机）。
- 数据一次给全、只要第 `k` 个、不要顺序 → 快速选择，平均 `O(n)`（例：LC 215 数组中的第K个最大元素）。
- 要的是频次且值域 `<= n` → 桶排序 `O(n)`（例：LC 347 前 K 个高频元素）。
- 要随时删除任意元素 / 取第 `k` 个 / 取「不超过某值的最近一个」 → 有序结构（`bisect`），堆做不了（删除可用懒删除）（例：LC 981 基于时间的键值存储）。
- `k` 接近 `n` → 直接排序：每个数都要参与配对，排序一次就够（例：LC 561 数组拆分 I）。
- `heapq` 只有**最小堆**：最大堆存负数，中位数里较小的那一半就存相反数（例：LC 295 数据流的中位数）。

**例题：** LC 373 查找和最小的 K 对数字

给两个非递减整数数组 `nums1`、`nums2` 和整数 `k`，返回和最小的 `k` 个数对 `(u, v)`（`u` 来自 `nums1`，`v` 来自 `nums2`）。两数组长度都不超过 `10^5`，`1 <= k <= 10^4`。

```python
import heapq

def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    if not nums1 or not nums2:
        return []
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(heap)
    answer = []
    while heap and len(answer) < k:
        _, i, j = heapq.heappop(heap)
        answer.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return answer
```

**例题：** LC 23 合并 K 个升序链表

给一个链表数组 `lists`，每个链表都已按升序排列。把所有链表合并成一个升序链表，返回合并后的链表。`k == lists.length`，`0 <= k <= 10^4`，`0 <= lists[i].length <= 500`，`-10^4 <= lists[i][j] <= 10^4`，所有链表长度之和不超过 `10^4`。

```python
import heapq
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # 堆里放 (值, 链表编号, 节点)：值相同时比编号，永远不会去比较 ListNode
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

**例题：** LC 295 数据流的中位数

中位数是有序整数列表中的中间值；列表大小为偶数时没有中间值，中位数是两个中间值的平均值（`[2,3,4]` 的中位数是 `3`，`[2,3]` 的中位数是 `2.5`）。实现 `MedianFinder` 类：`MedianFinder()` 初始化；`void addNum(int num)` 将数据流中的整数 `num` 加入数据结构；`double findMedian()` 返回到目前为止所有元素的中位数，与实际答案相差 `10^-5` 以内的答案将被接受。`-10^5 <= num <= 10^5`，调用 `findMedian` 之前数据结构中至少有一个元素，最多 `5 * 10^4` 次调用 `addNum` 和 `findMedian`。

```python
from heapq import heappop, heappush, heappushpop
class MedianFinder:
    def __init__(self) -> None:
        self.low: list[int] = []              # 大根堆（存相反数）：较小的一半，堆顶 = 这一半的最大值
        self.high: list[int] = []             # 小根堆：较大的一半，堆顶 = 这一半的最小值
    def addNum(self, num: int) -> None:
        heappush(self.high, -heappushpop(self.low, -num))   # 先过 low 再交给 high，保证 low 的每个数 <= high 的每个数
        if len(self.high) > len(self.low):                  # 保持 len(low) 等于 len(high) 或多 1
            heappush(self.low, -heappop(self.high))
    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
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

**例题：** LC 767 重构字符串

给字符串 `s`，判断能否重新排列其中的字母，使任意两个相邻字符都不同。可以就返回任意一种排列，不行就返回空字符串 `""`。`1 <= s.length <= 500`，`s` 只含小写字母。

```python
from collections import Counter
from heapq import heapify, heappop, heappush
def reorganize_string(s: str) -> str:
    heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]
    heapify(heap)                           # 出现次数最多的字符在堆顶
    out: list[str] = []
    held = (0, "")                          # 上一轮刚用过、暂时不能再选的 (负计数, 字符)
    while heap:
        cnt, ch = heappop(heap)
        out.append(ch)
        if held[0]:
            heappush(heap, held)            # 上一个字符隔了一位，可以重新参选
        held = (cnt + 1, ch)                # 用掉一个，剩余数量暂存
    return "".join(out) if len(out) == len(s) else ""
```

**例题：** LC 778 水位上升的泳池中游泳

`n x n` 的整数矩阵 `grid`，`grid[i][j]` 是位置 `(i, j)` 平台的高度。时间为 `t` 时水位是 `t`。你可以从一个平台游向上下左右相邻的平台，前提是此时水位**同时淹没**这两个平台（`t` 不小于两者的高度）；在平台内部移动、瞬间移动都不耗时。你从左上角 `(0, 0)` 出发，返回到达右下角 `(n-1, n-1)` 所需的**最少时间**。`1 <= n <= 50`，`0 <= grid[i][j] < n^2`，所有高度互不相同。

```python
from heapq import heappop, heappush
def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]                    # (到达此格所需的最低水位, 行, 列)
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)                    # 弹出的是"当前最低水位下能到的最低一格"
        if x == y == n - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                seen.add((nx, ny))
                heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return -1
```

**例题：** LC 121 买卖股票的最佳时机

数组 `prices`，`prices[i]` 是某支股票第 `i` 天的价格。你只能选择**某一天**买入，并在**未来的某一天**卖出，求最大利润；如果不能获利，返回 `0`。`1 <= prices.length <= 10^5`，`0 <= prices[i] <= 10^4`。

```python
def max_profit(prices: list[int]) -> int:
    low, best = prices[0], 0          # low：迄今最低价
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**例题：** LC 215 数组中的第K个最大元素

给整数数组 `nums` 和整数 `k`，返回数组**排序后**的第 `k` 个最大元素（不是第 `k` 个不同的元素）。必须设计并实现时间复杂度为 `O(n)` 的算法。`1 <= k <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

**例题：** LC 347 前 K 个高频元素

给整数数组 `nums` 和整数 `k`，返回出现频率前 `k` 高的元素，可按任意顺序返回。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`，`k` 的取值范围是 `[1, 数组中不相同元素的个数]`，数据保证答案唯一。

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

**例题：** LC 981 基于时间的键值存储

设计一个 `TimeMap` 类：同一个键在不同时间戳可以存多个值，并能按时间戳取值。`set(key, value, timestamp)` 在时间戳 `timestamp` 存入键 `key` 对应的值 `value`；`get(key, timestamp)` 返回此前某次 `set` 中满足 `timestamp_prev <= timestamp` 的值，若有多个，返回 `timestamp_prev` 最大的那个；没有则返回空串 `""`。`1 <= key.length, value.length <= 100`，由小写字母和数字组成，`1 <= timestamp <= 10^7`，所有 `set` 的时间戳**严格递增**，`set` 与 `get` 合计最多 `2 * 10^5` 次调用。

```python
from bisect import bisect_right
from collections import defaultdict
class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)
    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```

**例题：** LC 561 数组拆分 I

给长度为 `2n` 的整数数组 `nums`，把它分成 `n` 对 `(a_1, b_1), …, (a_n, b_n)`，使 `min(a_1, b_1) + … + min(a_n, b_n)` 最大，返回这个最大和。`1 <= n <= 10^4`，`nums.length == 2n`，`-10^4 <= nums[i] <= 10^4`。

```python
def array_pair_sum(nums: list[int]) -> int:
    nums = sorted(nums)                 # 不改调用方的列表
    return sum(nums[::2])               # 相邻两两配对，每对的较小者落在偶数下标
```
