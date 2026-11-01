---
id: tlc-tops-find-median-from-data-stream-0-whole
node: heap-priority-queue.find-median-from-data-stream
type: qa
---
## Q
**LC 295 数据流的中位数**｜Hard · 全公司热度第 22 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

中位数是有序整数列表中的中间值；列表大小为偶数时没有中间值，中位数是两个中间值的平均值（`[2,3,4]` 的中位数是 `3`，`[2,3]` 的中位数是 `2.5`）。实现 `MedianFinder` 类：`MedianFinder()` 初始化；`void addNum(int num)` 将数据流中的整数 `num` 加入数据结构；`double findMedian()` 返回到目前为止所有元素的中位数，与实际答案相差 `10^-5` 以内的答案会被接受。`-10^5 <= num <= 10^5`，调用 `findMedian` 之前数据结构中至少有一个元素，`addNum` 与 `findMedian` 总共最多调用 `5 * 10^4` 次。例：依次 `addNum(1)`、`addNum(2)`、`findMedian()`、`addNum(3)`、`findMedian()` → `1.5`、`2.0`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 双堆（two heaps）：大根堆放较小的一半，小根堆放较大的一半，中位数在两个堆顶。

**一句话。** 大根堆 `low` 存较小的一半，小根堆 `high` 存较大的一半，保持 `len(low)` 等于 `len(high)` 或多 `1`；中位数就是 `low` 的堆顶，或两个堆顶的平均。

**识别。** 「数据流 + 随时查中位数」：只关心中间的一两个元素，不需要全体有序。「中间值 = 左半的最大值与右半的最小值」，正好是两个堆的堆顶。`addNum` 总共 `5 * 10^4` 次，每次 `O(log n)`。

**推导。** 每次查询时排序，`O(n log n)`。用 `bisect.insort` 保持有序，查询 `O(1)`，插入 `O(n)`（`memmove` 很快）。浪费在于维护了全局顺序，却只用中间的元素。把元素分成左右两半，只要「`low` 里每个数都不大于 `high` 里每个数」且两半大小差不超过 `1`，中位数就在两个堆顶。插入时先放进 `low`，把 `low` 的最大值挪给 `high`（保证有序性），再在 `high` 更大时挪回一个（保证大小）。

**简单解法。** 列表始终有序：`addNum` 用 `bisect.insort` 插入，`findMedian` 按下标取中间。

```python
from bisect import insort

class MedianFinder:
    def __init__(self) -> None:
        self.nums: list[int] = []                  # 始终保持升序

    def addNum(self, num: int) -> None:
        insort(self.nums, num)                     # 二分找位置，再整体后移插入

    def findMedian(self) -> float:
        n = len(self.nums)
        if n % 2:
            return float(self.nums[n // 2])
        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2
```

`addNum` 为 `O(n)`（元素后移是很快的 `memmove`），`findMedian` 为 `O(1)`；`5 * 10^4` 次调用够用。

最优解：

```python
import heapq

class MedianFinder:
    def __init__(self) -> None:
        self.low: list[int] = []                   # 大根堆（存相反数）：较小的一半，堆顶是这一半的最大值
        self.high: list[int] = []                  # 小根堆：较大的一半，堆顶是这一半的最小值

    def addNum(self, num: int) -> None:
        # 先过 low 再交给 high：low 里每个数都 <= high 里每个数
        heapq.heappush(self.high, -heapq.heappushpop(self.low, -num))
        if len(self.high) > len(self.low):         # 保持 len(low) == len(high) 或多 1
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])             # 奇数个：中位数是 low 的堆顶
        return (-self.low[0] + self.high[0]) / 2   # 偶数个：两个堆顶的平均
```

运行：`addNum(1)`、`addNum(2)` 后 `findMedian()` → `1.5`；再 `addNum(3)` 后 → `2.0`；依次加入 `5, 1, 3` 后 → `3.0`；依次加入 `2, 1, 5, 3` 后 → `2.5`。

**复杂度。** `addNum` 时间 `O(log n)`；`findMedian` 时间 `O(1)`；空间 `O(n)`。

**拓展优化。**
- 所有数都在 `0..100`：计数数组代替堆，`addNum` 为 `O(1)`，`findMedian` 最多扫 101 个桶：
```python
class MedianFinderBuckets:
    def __init__(self) -> None:
        self.count = [0] * 101                     # count[v]：数值 v 出现的次数
        self.total = 0

    def addNum(self, num: int) -> None:
        self.count[num] += 1
        self.total += 1

    def kth(self, k: int) -> int:                  # 第 k 小的数（k 从 1 开始）
        for value, c in enumerate(self.count):
            k -= c
            if k <= 0:
                return value
        raise ValueError("k 超出范围")

    def findMedian(self) -> float:
        lo = self.kth((self.total + 1) // 2)       # 奇数个时 lo 与 hi 是同一个数
        hi = self.kth(self.total // 2 + 1)
        return (lo + hi) / 2
```
- 99% 的数在 `0..100`：桶数组照用，界外的数各用一个小的计数或有序列表，中位数几乎总落在桶里。

**易错点。**
- 新数按大小路由到某个堆却不再平衡：依次加入 `1,2,3`，`1` 进 `low`，`2`、`3` 都进 `high`，`findMedian` 得 `1.5`，正确是 `2.0`。每次插入后都要保持两堆大小差不超过 `1`。
- 不经过「先过 `low` 再交给 `high`」直接轮流放：`5, 1, 3` 得 `5.0`，正确是 `3.0`（`low` 里留下了 `5`，比 `high` 里的 `1` 还大）。
- 大根堆要存相反数，取出时取反；偶数个时用 `/ 2` 得浮点数，奇数个返回 `float(...)`，类型保持一致。
**同模式。** LC 480 滑动窗口中位数、LC 703 数据流中的第 K 大元素、LC 502 IPO、LC 23 合并 K 个升序链表。
