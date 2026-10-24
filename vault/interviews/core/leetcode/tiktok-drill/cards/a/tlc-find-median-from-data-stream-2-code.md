---
id: tlc-find-median-from-data-stream-2-code
node: a.find-median-from-data-stream
type: qa
step: 2
---
## Q
**LC 295 数据流的中位数**｜写出 Python 实现

实现 `MedianFinder`：`addNum(num)` 加入一个整数（`-10^5 <= num <= 10^5`），`findMedian()` 返回当前所有元素的中位数（偶数个时取中间两数的平均，返回 `float`）。至少有一个元素时才会查询，最多 `5×10^4` 次调用。

## A
**思路。** 两个堆：`low` 是大根堆（用相反数模拟），存较小的一半；`high` 是小根堆，存较大的一半。新数先 `heappushpop` 进 `low`，弹出的最大值送进 `high`，这样 `low` 的所有数都不大于 `high` 的所有数；再把大小调成 `len(low)` 等于 `len(high)` 或多 1。

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

运行：`addNum(1)`、`addNum(2)` 后 `findMedian()` → `1.5`；再 `addNum(3)` 后 → `2.0`；只加入 `7` 时 → `7.0`；依次加入 `2, 1, 5, 3` → `2.5`。

**复杂度。** `addNum` 时间 `O(log n)`：最多四次堆操作；`findMedian` 时间 `O(1)`；空间 `O(n)`。

**写法要点。** `heappushpop(heap, x)` 先推入 `x` 再弹出最小值，比分开写 `heappush` 加 `heappop` 少一次堆调整；大根堆用相反数模拟，所有进出都要取反，容易漏；`from heapq import ...` 直接导入函数，调用更短；返回 `float(...)` 保证奇数个时类型也是浮点。
