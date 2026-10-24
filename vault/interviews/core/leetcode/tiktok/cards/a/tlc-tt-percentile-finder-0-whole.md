---
id: tlc-tt-percentile-finder-0-whole
node: a.tt-percentile-finder
type: qa
---
## Q
**PercentileFinder：实时维护数字并返回第 p 百分位**｜Medium · TikTok 高频

设计类 `PercentileFinder`，实时维护一组整数：`addNums(nums)` 加入一批数字；`findPercentile(p)` 返回当前全部数据的第 `p` 百分位值。约定：`p` 是 `0` 到 `100` 的整数，用最近秩法（nearest-rank）：第 `max(1, ceil(p * N / 100))` 小的数，`N` 是当前数据个数；没有数据时抛 `ValueError`。要求先用 `bisect`（有序列表 + 二分插入）实现。两个方法的调用总数不超过 `10^5`，加入的数字总数不超过 `10^5`。例：`addNums([15,20,35,40,50])` 之后，`p = 0, 5, 30, 40, 50, 100` 依次得到 `15, 15, 20, 20, 35, 50`；再 `addNums([1,100])`，`p = 0, 50, 90, 100` 得到 `1, 35, 100, 100`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 让列表始终有序：批量小时用 `bisect.insort` 逐个插入，批量大时直接 `extend` 再 `sort`（Timsort 对「已有序的前缀加一小段新数据」近似线性）；查询时按最近秩法算出名次，直接取 `data[rank - 1]`，`O(1)`。

**识别。** 「实时加入 + 任意时刻问第 `p` 百分位」就是动态的顺序统计：只要数据有序，第 `k` 小就是下标 `k - 1`；「先用 `bisect`」直接点出了有序列表这个实现；百分位的定义（最近秩、插值）必须先约定清楚。

**推导。** 暴力：每次 `findPercentile` 都把全部数据排序再取，`O(N log N)` 一次 → 浪费：每次查询重复排序，数据只增加了一点点 → 洞察：把排序分摊到每次加入：二分找到位置的比较是 `O(log N)`，列表插入要平移后面的元素 `O(N)`，但这是 `memmove`，常数极小；查询从 `O(N log N)` 降到 `O(1)`。批量加入的数据量接近或超过已有数据时，插入 `m` 个的总平移量 `O(m * N)` 不如整体排一次，所以按批量大小切换两种做法。

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

运行：`addNums([15,20,35,40,50])` 后 `p = 0, 5, 30, 40, 50, 100` → `[15, 15, 20, 20, 35, 50]`；再 `addNums([1,100])` 后 `p = 0, 50, 90, 100` → `[1, 35, 100, 100]`；没有数据时 `findPercentile(50)` → `ValueError: no data`。

**复杂度。** `addNums` 单个插入 `O(log N)` 次比较加 `O(N)` 平移；批量大时整体排序约 `O((N + m) + m log m)`；`findPercentile` 为 `O(1)`；空间 `O(N)`。

**易错点。**
- 忘了 `max(1, ...)`：`p = 0` 时 `ceil(0) = 0`，`data[0 - 1]` 取到列表最后一个，`[15,20,35,40,50]` 的 `p = 0` 会得到 `50`，正确是最小值 `15`。
- 用 `int(p / 100 * N)` 当下标（向下取整）：`p = 40` 时下标 `2`，得到 `35`，正确是第 `2` 小即 `20`；`p = 100` 时下标 `N`，越界 `IndexError`。
- 在 `for` 循环里对列表反复 `sort()`：正确但每次 `O(N log N)`，批量小的时候白白浪费。

**追问。**
- 除了 `bisect` 还能用什么：`p` 固定时用两个堆（最大堆存前 `k` 小、最小堆存其余）；值域有界时用 Fenwick 树按出现次数找第 `k` 小；一般情形用平衡树 / 顺序统计树 / 跳表，或第三方 `sortedcontainers.SortedList`（分块列表，插入和按秩访问近似 `O(sqrt N)`）。
- 允许近似：t-digest、GK 摘要，内存与精度参数成正比，与 `N` 无关。
- 百分位用线性插值：在相邻两个秩之间按小数部分加权，需要先约定插值公式。

**同模式。** LC 295 数据流的中位数、LC 703 数据流中的第 K 大元素、LC 480 滑动窗口中位数、LC 315 计算右侧小于当前元素的个数。
