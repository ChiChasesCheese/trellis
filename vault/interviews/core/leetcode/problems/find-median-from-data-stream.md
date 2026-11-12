---
slug: find-median-from-data-stream
---
## Q
**LC 295 数据流的中位数**｜Hard

设计 `MedianFinder`：`addNum` 加入一个数，`findMedian` 返回当前所有数的中位数。

## A
**一句话。** 双堆：大根堆存较小的一半，小根堆存较大的一半，大小相等或前者多一个，中位数在两个堆顶。

```python
class MedianFinder:
    def __init__(self):
        self.low = []            # 大根堆（存负数）：较小的一半
        self.high = []           # 小根堆：较大的一半

    def addNum(self, num):
        # 先过 low 再送 high，保证 low 全 <= high 全
        x = heapq.heappushpop(self.low, -num)
        heapq.heappush(self.high, -x)
        if len(self.high) > len(self.low):   # low 多一个或相等
            y = heapq.heappop(self.high)
            heapq.heappush(self.low, -y)

    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```

**复杂度。** `addNum` 为 `O(log n)`，`findMedian` 为 `O(1)`，空间 `O(n)`。

**易错点。**
- 轮流往两个堆里放，不经过 `low` 中转：`5,1,3` 得 `5.0`，应为 `3.0`。
- 忘了大根堆存的是负数：取出时要取反，偶数个时是 `(-low[0] + high[0]) / 2`。

**追问。**
- 要第 `p` 百分位数？：两堆大小比例固定成 `p : (100-p)`，加数后按比例搬堆顶。
- 滑动窗口中位数（LC 480）？：还要删除，用两堆加延迟删除，或有序列表。

**同模式。** LC 480 滑动窗口中位数、LC 703 数据流中的第 K 大元素、LC 502 IPO、LC 23 合并 K 个升序链表
