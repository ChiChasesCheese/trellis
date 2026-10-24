---
id: tlc-patterns-heap-patterns-3-why-two-heaps
node: patterns.heap-patterns
type: qa
step: 3
---
## Q
**堆（Heap）｜正确性：双堆求中位数的两条不变量**

LC 295 的两个堆必须同时满足哪两个条件？如果只是交替往两个堆里放数，会错在哪里？

## A
**不变量**：
1. **有序**：`lo`（最大堆，存较小的一半）里每个数 `<=` `hi`（最小堆，存较大的一半）里每个数；
2. **平衡**：`len(lo) == len(hi)` 或 `len(lo) == len(hi) + 1`。

满足这两条，中位数就在两个堆顶：奇数个取 `lo` 堆顶，偶数个取两个堆顶的平均。

```python
import heapq
class MedianFinder:
    def __init__(self) -> None:
        self.lo: list[int] = []            # 最大堆（存负数）：较小的一半
        self.hi: list[int] = []            # 最小堆：较大的一半
    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))   # 经过 lo 再转给 hi，保证有序
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))   # 保证平衡
    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2
m = MedianFinder(); m.addNum(1); m.addNum(2); print(m.findMedian())   # 1.5
m.addNum(3); print(m.findMedian())                                    # 2.0
```

**反例**：只按奇偶个数交替放入（第 1、3 个进 `lo`，第 2、4 个进 `hi`），不先过一遍另一个堆。依次加入 `5, 1, 2, 3`：
- 交替写法：`lo = {5, 2}`，`hi = {1, 3}`，两堆有序性被破坏，`findMedian()` 给出 `3.0`；
- 正确值：排序后 `1,2,3,5`，中位数 `2.5`。

做法：每个新数都**先进 `lo`，再把 `lo` 的最大值转给 `hi`**，保证 `lo` 的最大值不超过 `hi` 的最小值；然后再平衡个数。`addNum` 为 `O(log n)`，`findMedian` 为 `O(1)`。
