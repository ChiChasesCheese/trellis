---
id: tlc-sliding-window-median-0-whole
node: b.sliding-window-median
type: qa
---
## Q
**LC 480 滑动窗口中位数**｜Hard · CodeTop 国内累计 2 次 · 最近 2026-03-26（CodeTop）

数组 `nums` 上有一个长度为 `k` 的窗口从最左端滑到最右端，每次右移一位。返回每个窗口的**中位数**组成的数组：窗口排序后，`k` 为奇数取最中间的数，`k` 为偶数取中间两个数的平均值。`1 <= k <= nums.length <= 10^5`，`nums[i]` 是 32 位有符号整数；与真实值误差在 `10^-5` 以内即算正确。例：`nums = [1,3,-1,-3,5,3,6,7], k = 3` → `[1,-1,-1,3,5,6]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对顶堆（two heaps）：大顶堆 `small` 存较小的一半、小顶堆 `large` 存较大的一半，中位数只看两个堆顶；滑出的元素不立刻从堆里找出来删，而是记进 `delayed`，等它浮到堆顶时再弹掉（延迟删除，lazy deletion）。`O(n log n)`。

**识别。** 「中位数 + 动态集合」是对顶堆的信号（LC 295 数据流中位数）；「滑动窗口」多了一个要求：**删除任意元素**，而 `heapq` 只能删堆顶，所以要配延迟删除。`n` 到 `10^5`，每个窗口重新排序的 `O(nk log k)` 在 `k` 大时不可行。

**推导。** 暴力：每个窗口排序取中位数，`O(nk log k)` → 浪费：相邻窗口只差一进一出，却整体重排 → 只需要一个支持「插入、删除、取中间」的结构：有序列表 + 二分是 `O(k)` 每步；对顶堆插入是 `O(log k)`，但删除任意元素要 `O(k)` 查找 → 洞察：中位数只读两个堆顶，埋在堆里的过期元素不影响答案，只要保证**堆顶有效**、并按「有效元素个数」做平衡即可 → 每步 `O(log n)`。

```python
from collections import Counter
from heapq import heapify, heappop, heappush


def median_sliding_window(nums: list[int], k: int) -> list[float]:
    small = [-x for x in nums[:k]]          # 大顶堆（存相反数）：窗口里较小的一半
    heapify(small)
    large: list[int] = []                   # 小顶堆：窗口里较大的一半
    for _ in range(k // 2):                 # 有效元素个数：small 比 large 多 0 或 1 个
        heappush(large, -heappop(small))
    delayed: Counter[int] = Counter()       # 延迟删除：值 -> 还欠删几次

    def mid() -> float:
        return float(-small[0]) if k % 2 else (-small[0] + large[0]) / 2

    res = [mid()]
    for out, new in zip(nums, nums[k:]):    # out 滑出窗口，new 滑入窗口
        delayed[out] += 1
        balance = -1 if out <= -small[0] else 1     # 「small 有效数 − large 有效数」的变化
        if new <= -small[0]:
            heappush(small, -new)
            balance += 1
        else:
            heappush(large, new)
            balance -= 1
        if balance < 0:                     # small 少了一个：从 large 补
            heappush(small, -heappop(large))
        elif balance > 0:                   # large 少了一个：从 small 补
            heappush(large, -heappop(small))
        while small and delayed[-small[0]]:  # 堆顶若是待删元素，现在真正弹掉
            delayed[-small[0]] -= 1
            heappop(small)
        while large and delayed[large[0]]:
            delayed[large[0]] -= 1
            heappop(large)
        res.append(mid())
    return res
```

运行：`[1,3,-1,-3,5,3,6,7], k=3` → `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]`，同一数组 `k=2` → `[2.0, 1.0, -2.0, 1.0, 4.0, 4.5, 6.5]`，`[1,2,3,4,2,3,1,4,2], k=3` → `[2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]`，`[1,4,2,3], k=4` → `[2.5]`，`[5], k=1` → `[5.0]`。

**复杂度。** 时间 `O(n log n)`：每个元素入堆、出堆各常数次；过期元素可能埋在堆底迟迟不出，堆的实际大小最坏是 `O(n)`，所以空间 `O(n)`。

**易错点。**
- 只清理一个堆的堆顶：两个堆顶都参与中位数，都必须有效。`[2,1,3], k=2` 只清 `small` 会得到 `[1.5, 1.5]`，正确是 `[1.5, 2.0]`（过期的 `2` 留在 `large` 堆顶）。
- 判断滑出元素在哪个堆用 `out < -small[0]`：`out` 恰好等于 `small` 的堆顶时被误判到 `large`，计数失衡。`[1,3], k=1` 会在取堆顶时 `IndexError`，正确是 `[1.0, 3.0]`。
- 偶数窗口用 `//` 求平均：`[1,4,2,3], k=4` 得 `2` 而不是 `2.5`。

**追问。**
- 用 `sortedcontainers.SortedList`（LeetCode 环境自带，非标准库）：`add` / `remove` / 下标取中位数，代码最短，`O(n log k)`。
- 只有插入没有删除（LC 295）：对顶堆即可，不需要 `delayed`。
- 求窗口内第 `p` 小而不是中位数：把 `small` 的有效大小固定为 `p`，其余逻辑不变。

**同模式。** LC 295 数据流的中位数、LC 239 滑动窗口最大值、LC 502 IPO、LC 1825 求出 MK 平均值。
