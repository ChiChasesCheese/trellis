---
id: tlc-find-median-from-data-stream-0-whole
node: a.find-median-from-data-stream
type: qa
---
## Q
**LC 295 数据流的中位数**｜Hard · LC TikTok 热度 62/100（近 3 个月） · 近一年被问：美国 3 次、国内 0 次 · CodeTop 国内累计 18 次 · 最近 2026-10-15（面试记录）

中位数是有序整数列表中的中间值；列表大小为偶数时没有中间值，中位数是两个中间值的平均值（`[2,3,4]` 的中位数是 `3`，`[2,3]` 的中位数是 `2.5`）。实现 `MedianFinder` 类：`MedianFinder()` 初始化；`void addNum(int num)` 将数据流中的整数 `num` 加入数据结构；`double findMedian()` 返回到目前为止所有元素的中位数，与实际答案相差 `10^-5` 以内的答案将被接受。`-10^5 <= num <= 10^5`，调用 `findMedian` 之前数据结构中至少有一个元素，最多 `5 * 10^4` 次调用 `addNum` 和 `findMedian`。例：依次 `addNum(1)`、`addNum(2)`、`findMedian()`、`addNum(3)`、`findMedian()` 返回 `1.5`、`2.0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 双堆（two heaps）：大根堆 `low` 存较小的一半，小根堆 `high` 存较大的一半，保持两堆大小相等或 `low` 多一个；中位数就在两个堆顶。`addNum` 是 `O(log n)`，`findMedian` 是 `O(1)`。

**识别。** 「数据流 + 随时查中位数」：每次插入后数据都要保持可查询的顺序结构。中位数只关心**中间那一两个**元素，不需要全体有序。「中间值 = 左半的最大值与右半的最小值」，正是两个堆的堆顶。

**推导。** 暴力：每次 `findMedian` 都对全部元素排序，`O(n log n)` → 每次 `addNum` 用 `bisect.insort` 保持有序，查询 `O(1)`，插入 `O(n)`（`memmove` 很快）→ 浪费：维护了全局顺序，但只要中间的元素 → 把元素分成左右两半，只让堆顶暴露边界：`low` 的所有数都不大于 `high` 的所有数，且两堆大小差不超过 1 → 新数先过 `low` 再把 `low` 的最大值送给 `high`（保证不变量），再按大小平衡。

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

运行：`addNum(1)`、`addNum(2)` 后 `findMedian()` → `1.5`；再 `addNum(3)` 后 → `2.0`；依次加入 `2, 1, 5, 3` 后 → `2.5`；加入 `5, 1, 3` 后 → `3.0`。

**复杂度。** `addNum` 时间 `O(log n)`（常数次堆操作）；`findMedian` 时间 `O(1)`；空间 `O(n)`。

**易错点。**
- 两个堆之间必须有序：简单地轮流往两个堆里放，不经过「先过 `low` 再送 `high`」，`5, 1, 3` 会得到 `5.0`，正确是 `3.0`（`low` 里留下了 `5`，比 `high` 里的 `1` 还大）。
- `heapq` 只有小根堆：大根堆要存相反数，取出时再取反；偶数个元素时中位数是 `(-low[0] + high[0]) / 2`，用 `/` 得到浮点数；奇数个时返回 `float(-low[0])`，保证类型是 `float`。
- 平衡的方向要固定：约定 `low` 比 `high` 多一个或相等，查询时按这个约定取中位数，换了方向两边都要改。

**追问。**
- 所有数都在 `0..100`：计数数组 `count[0..100]`，`findMedian` 扫 `101` 个桶找第 `k` 小，`addNum` 是 `O(1)`，`findMedian` 是 `O(101)` = `O(1)`。
- 99% 的数在 `0..100`，其余零星在外：计数数组加两个小堆（或一个排序列表）存界外的数，中位数仍在桶里附近。
- 滑动窗口中位数（LC 480）：除了插入还要删除，用两个堆加延迟删除，或 `sortedcontainers.SortedList` / 平衡树。

**同模式。** LC 480 滑动窗口中位数、LC 703 数据流中的第 K 大元素、LC 502 IPO、LC 23 合并 K 个升序链表（堆）。
