---
id: tlc-find-median-from-data-stream-4-followup
node: p2.find-median-from-data-stream
type: qa
step: 4
---
## Q
**LC 295 数据流的中位数**｜追问

面试官接着问：（1）如果所有整数都在 `[0, 100]` 内？（2）如果 99% 的整数在 `[0, 100]` 内，其余零星在外？（3）需要的是滑动窗口中位数，窗口外的数要删除？

## A
1. **值域 `[0, 100]`**：用计数数组 `count[0..100]`，`addNum` 是 `O(1)`；`findMedian` 扫描 `101` 个桶找第 `k` 小，是常数次扫描。
```python
class MedianFinder100:
    def __init__(self) -> None:
        self.count = [0] * 101
        self.n = 0

    def addNum(self, num: int) -> None:
        self.count[num] += 1
        self.n += 1

    def _kth(self, k: int) -> int:            # 第 k 小（k 从 1 起）
        for v, c in enumerate(self.count):
            k -= c
            if k <= 0:
                return v
        raise ValueError(k)

    def findMedian(self) -> float:
        if self.n % 2:
            return float(self._kth(self.n // 2 + 1))
        return (self._kth(self.n // 2) + self._kth(self.n // 2 + 1)) / 2
```
   依次加入 `1, 2, 3`，`findMedian()` 依次是 `1.0, 1.5, 2.0`。
2. **99% 在 `[0, 100]`**：桶数组之外，另存「小于 0 的数」和「大于 100 的数」。绝大多数查询落在桶里，界外只有 1% 的数，用两个很小的堆或有序列表存即可，找第 `k` 小时先跳过界外较小的部分。
3. **滑动窗口**（LC 480）：堆不支持删除任意元素。常见做法是**延迟删除**：要删的数先记在一个计数字典里，等它浮到堆顶时才真正弹出，并保持两堆的有效大小（不含待删元素）平衡；或者直接用有序结构（`sortedcontainers.SortedList`、平衡树）支持 `O(log n)` 的插入、删除和按排名取值。

**Python 提醒**：`heapq` 只保证 `heap[0]` 是最小值，其余位置并不有序，不要拿 `heap[-1]` 当最大值，也不要用 `append` 之类绕过 `heappush` 的写法修改堆列表，那会破坏堆性质。标准库没有自带的有序列表，`bisect.insort` 在 `5×10^4` 级别可用，更大规模要用第三方的 `SortedList`。
