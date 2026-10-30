---
id: tlc-find-median-from-data-stream-5-alt
node: p2.find-median-from-data-stream
type: qa
step: 5
---
## Q
**LC 295 数据流的中位数**｜另一种解法

不用堆，用 `bisect.insort` 维护一个有序列表怎么做？它在这个问题的数据范围内表现如何，什么时候该选哪个？

## A
**思路。** 始终保持列表有序。`addNum` 用 `bisect.insort` 二分找到插入位置并插入；`findMedian` 直接按下标读中间一个或两个元素。

```python
import bisect

class MedianFinderSorted:
    def __init__(self) -> None:
        self.a: list[int] = []

    def addNum(self, num: int) -> None:
        bisect.insort(self.a, num)            # 二分找位置 O(log n)，插入时搬元素 O(n)，但是 memmove 很快

    def findMedian(self) -> float:
        n = len(self.a)
        return float(self.a[n // 2]) if n % 2 else (self.a[n // 2 - 1] + self.a[n // 2]) / 2
```

运行：依次 `addNum(1)`、`addNum(2)`、`addNum(3)`，`findMedian()` 依次是 `1.0`、`1.5`、`2.0`。

**复杂度。** `addNum` 比较次数 `O(log n)`，元素搬移 `O(n)`（由 C 的 `memmove` 完成，常数很小）；`findMedian` 时间 `O(1)`；空间 `O(n)`。

**什么时候选哪个。**
- 在 `5×10^4` 次调用的规模下：有序列表版和双堆版都很快，有序列表代码最短、最不容易出错，没有相反数和平衡逻辑。
- 双堆：`addNum` 是严格 `O(log n)`，规模涨到 `10^6` 以上仍然稳定；这是面试官期望看到的数据结构，也是追问（滑动窗口、值域小）的基础。
- 有序列表版天然支持「第 `k` 小」「删除某个值」（`bisect_left` 加 `del`，也是 `O(n)`），在需要这些操作的变体里更方便。
- 面试里先说清有序列表的 `O(n)` 插入，再给出双堆；如果面试官不追问规模，有序列表是可接受的起点。
