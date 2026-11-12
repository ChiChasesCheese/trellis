---
slug: tt-percentile-finder
---
## Q
**PercentileFinder：实时维护数字并返回第 p 百分位**｜Medium

设计 `PercentileFinder`：`addNums(nums)` 加入一批整数，`findPercentile(p)` 返回当前数据的第 `p`（0 到 100 的整数）百分位。用最近秩法：第 `max(1, ceil(p * N / 100))` 小的数；无数据抛 `ValueError`。先用 `bisect` 实现。

## A
**一句话。** 列表始终有序：批量小用 `insort` 逐个插，批量大 `extend` 后 `sort`；查询算出名次直接取 `data[rank - 1]`。

```python
class PercentileFinder:
    def __init__(self):
        self.data = []      # 始终升序

    def addNums(self, nums):
        if len(nums) * 8 > len(self.data):   # 批量大：拼上再排
            self.data.extend(nums)
            self.data.sort()
        else:                                # 批量小：逐个二分插入
            for x in nums:
                insort(self.data, x)

    def findPercentile(self, p):
        if not self.data:
            raise ValueError("no data")
        if not 0 <= p <= 100:
            raise ValueError("bad p")
        # ceil(p*N/100)，用整数算避免浮点误差
        rank = max(1, -(-p * len(self.data) // 100))
        return self.data[rank - 1]
```

**复杂度。** 时间 `addNums` 单个 `O(N)`（平移），`findPercentile` 为 `O(1)`，空间 `O(N)`。

**易错点。**
- 忘了 `max(1, …)`：`p = 0` 时 `data[-1]` 取到最大值，应为最小值。
- 用 `int(p / 100 * N)` 当下标：`p = 40`、`N = 5` 得 `35`，应为 `20`；`p = 100` 越界。

**追问。**
- 除了 `bisect` 还能用什么？：`p` 固定用两个堆；值域有界用 Fenwick 树找第 `k` 小；一般情形用平衡树或 `SortedList`。
- 允许近似？：t-digest、GK 摘要，内存与 `N` 无关。

**同模式。** LC 295 数据流的中位数、LC 703 数据流中的第 K 大元素、LC 480 滑动窗口中位数
