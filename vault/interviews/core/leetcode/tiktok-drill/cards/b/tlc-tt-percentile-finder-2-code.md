---
id: tlc-tt-percentile-finder-2-code
node: b.tt-percentile-finder
type: qa
step: 2
---
## Q
**PercentileFinder：实时维护数字并返回第 p 百分位**｜写出 Python 实现

用类实现：`addNums(nums)` 加入一批整数；`findPercentile(p)` 返回当前全部数据的第 `p` 百分位（`p` 为 `0` 到 `100` 的整数），最近秩法：第 `max(1, ceil(p * N / 100))` 小；没有数据抛 `ValueError`。用有序列表加 `bisect` 实现，调用总数不超过 `10^5`。

## A
**思路。** `_data` 始终升序。批量小就用 `insort` 逐个插入；批量大就 `extend` 后整体 `sort`。查询时用整数算出名次，返回 `_data[rank - 1]`。

```python
from bisect import insort


class PercentileFinder:
    def __init__(self) -> None:
        self._data: list[int] = []                # 始终保持升序

    def addNums(self, nums: list[int]) -> None:
        if len(nums) * 8 > len(self._data):       # 批量大：直接拼上再排，Timsort 会把已有序的前缀当一段，近似线性
            self._data.extend(nums)
            self._data.sort()
        else:                                     # 批量小：逐个二分插入，每次 O(log N) 比较 + O(N) 平移
            for x in nums:
                insort(self._data, x)

    def findPercentile(self, p: int) -> int:
        if not self._data:
            raise ValueError("no data")
        if not 0 <= p <= 100:
            raise ValueError("p must be in [0, 100]")
        rank = max(1, -(-p * len(self._data) // 100))     # 最近秩法：第 ceil(p·N/100) 小，用整数算避免浮点误差
        return self._data[rank - 1]
```

运行：`addNums([15,20,35,40,50])` 后 `p = 0, 5, 30, 40, 50, 100` → `[15, 15, 20, 20, 35, 50]`；再 `addNums([1,100])` 后 `p = 0, 50, 90, 100` → `[1, 35, 100, 100]`；无数据时 `findPercentile(50)` 抛 `ValueError: no data`。

**复杂度。** 单个插入 `O(log N)` 次比较加 `O(N)` 平移；批量大时整体排序；`findPercentile` 为 `O(1)`；空间 `O(N)`。

**写法要点。** `-(-a // b)` 是整数向上取整，等价于 `ceil(a / b)` 却没有浮点；`max(1, ...)` 处理 `p = 0`；`bisect.insort` 就地插入并保持有序；阈值 `len(nums) * 8 > len(self._data)` 是经验值，批量相对已有数据足够大时整体重排更划算，数值本身不关键；`_data.sort()` 对「已有序前缀加新数据」只需近似线性，这是 Timsort 识别已有序片段（run）的结果。
