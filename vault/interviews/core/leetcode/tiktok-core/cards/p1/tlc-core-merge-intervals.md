---
id: tlc-core-merge-intervals
node: p1.merge-intervals
type: qa
---
## Q
**LC 56 合并区间**｜Medium · LC TikTok 近 3 个月热度 81/100（全时段 88） · 近一年被问：美国 7 次、国内 3 次 · CodeTop 国内累计 81 次 · 最近 2026-10（美国面试记录） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

`intervals[i] = [start_i, end_i]` 表示一组区间，合并所有重叠的区间，返回一个互不重叠、恰好覆盖输入全部区间的数组。端点相接（如 `[1,4]` 和 `[4,5]`）也算重叠。`1 <= intervals.length <= 10^4`，`intervals[i].length == 2`，`0 <= start_i <= end_i <= 10^4`。例：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`；`[[1,4],[4,5]]` → `[[1,5]]`；`[[4,7],[1,4]]` → `[[1,7]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按起点排序，然后只和结果里最后一个区间比较：起点不超过它的终点就把终点延长到两者较大者，否则另起一个新区间。`O(n log n)`，瓶颈在排序。

**识别。** 「区间 + 重叠 + 合并 / 覆盖」是区间题的信号，几乎都先**按起点（或终点）排序**。排序之后，能和当前区间重叠的只可能是紧邻的上一段，不需要两两比较。`n <= 10^4`，`O(n^2)` 两两合并能过但没有必要。

**推导。** 暴力：反复找到任意一对重叠的区间合并成一个，直到没有重叠为止，最坏 `O(n^2)` 甚至更差。浪费在于区间是乱序的，必须反复找。洞察：按起点排好后，若当前区间 `[s, e]` 与已合并的最后一个区间 `[ls, le]` 不重叠（`s > le`），那么它之后的所有区间起点也 `>= s > le`，也不会和 `[ls, le]` 重叠，这一段就封口；若重叠则 `le = max(le, e)`。一次线性扫描。

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):           # 按起点排序；起点相同按终点，不影响结果
        if merged and start <= merged[-1][1]:      # 与上一个区间重叠（端点相接也算）
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

运行：三个示例输出 `[[1,6],[8,10],[15,18]]`、`[[1,5]]`、`[[1,7]]`；`[[1,4],[0,4]]` → `[[0,4]]`，`[[1,4],[2,3]]` → `[[1,4]]`（被完全包含），`[[5,5]]` → `[[5,5]]`。

**复杂度。** 时间 `O(n log n)`（排序）加 `O(n)`（扫描）；空间 `O(n)` 存结果，排序副本也是 `O(n)`。

**拓展优化。**
- 坐标只有 `0..10^4`，可以不排序，按起点分桶后扫描坐标，`O(n + R)`（`R` 是坐标上限）；坐标范围很大时仍用排序：
```python
def merge_bucket(intervals: list[list[int]]) -> list[list[int]]:
    limit = max(end for _, end in intervals)
    reach = [-1] * (limit + 1)                      # reach[s]：以 s 为起点的最远终点，-1 表示没有
    for start, end in intervals:
        reach[start] = max(reach[start], end)
    merged: list[list[int]] = []
    for start, end in enumerate(reach):             # 按坐标从小到大 = 按起点排序
        if end < 0:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```
- 往已排序、互不重叠的区间里插入一个新区间（LC 57），不重排，`O(n)`：
```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    lo, hi = new
    i, n = 0, len(intervals)
    ans: list[list[int]] = []
    while i < n and intervals[i][1] < lo:           # 完全在新区间左边：原样保留
        ans.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= hi:          # 与新区间重叠：并进 [lo, hi]
        lo, hi = min(lo, intervals[i][0]), max(hi, intervals[i][1])
        i += 1
    ans.append([lo, hi])
    ans.extend(intervals[i:])                       # 完全在右边：原样拼上
    return ans
```

**易错点。**
- 重叠条件是 `start <= merged[-1][1]`，写成 `<` 会漏掉端点相接：`[[1,4],[4,5]]` 得到 `[[1,4],[4,5]]`，正确是 `[[1,5]]`。
- 延长终点必须取 `max`：`[[1,4],[2,3]]` 里 `[2,3]` 被 `[1,4]` 包含，直接写 `merged[-1][1] = end` 会得到 `[[1,3]]`，正确是 `[[1,4]]`。
- 不排序直接扫描会错：`[[1,2],[8,9],[2,3]]` 输出 `[[1,2],[8,9]]`，丢掉了 `3`，正确是 `[[1,3],[8,9]]`。

**追问。**
- 区间不断流式到达：用有序结构（如按起点有序的列表加 `bisect`）维护已合并区间。
- 求被覆盖的总长度：合并后对 `end - start` 求和。

**同模式。** LC 57 插入区间、LC 252 / 253 会议室、LC 435 无重叠区间、LC 452 用最少数量的箭引爆气球、LC 986 区间列表的交集。
