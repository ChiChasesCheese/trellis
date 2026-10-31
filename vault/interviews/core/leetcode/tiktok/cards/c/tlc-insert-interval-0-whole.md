---
id: tlc-insert-interval-0-whole
node: c.insert-interval
type: qa
---
## Q
**LC 57 插入区间**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2022-05-19（国内 CodeTop）

给定一个无重叠的、按起点升序排列的区间列表 `intervals`（`intervals[i] = [start_i, end_i]`）和一个新区间 `newInterval = [start, end]`。至少共享一个点就算重叠。把 `newInterval` 插入 `intervals`，使结果依然按起点升序且互不重叠（必要时合并），返回插入后的列表。`0 <= intervals.length <= 10^4`，`0 <= start_i <= end_i <= 10^5`，`0 <= start <= end <= 10^5`。例：`intervals = [[1,3],[6,9]], newInterval = [2,5]` → `[[1,5],[6,9]]`；`intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]` → `[[1,2],[3,10],[12,16]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 利用列表已有序，一次线性扫描分三段：左边不重叠的原样放入，中间与新区间重叠的并入新区间，右边不重叠的原样放入。

**识别。** 「区间已排序、插入一个新区间」：重叠的区间在列表中是连续的一段，只需判断这一段的边界。判断重叠的条件是 `旧.end >= 新.start` 且 `旧.start <= 新.end`。

**推导。** 暴力：加入新区间后整体排序再套「合并区间」，`O(n log n)`，没用上输入有序。洞察：`end < start` 的区间一定在左边（第一段）；`start_i <= end` 的区间与新区间重叠（第二段）；剩下的都在右边。第二段内不断扩张 `start`、`end`，最后只需放入一个合并后的区间。

```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    start, end = newInterval
    result: list[list[int]] = []
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < start:     # 1) 完全在新区间左边的区间：原样放入
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:      # 2) 与新区间重叠的区间：并入新区间
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    result.extend(intervals[i:])                 # 3) 完全在右边的区间：原样放入
    return result
```

运行：示例一 `[[1,5],[6,9]]`；示例二 `[[1,2],[3,10],[12,16]]`；`[]` 加 `[5,7]` → `[[5,7]]`；`[[1,5]]` 加 `[2,3]` → `[[1,5]]`；`[[1,5]]` 加 `[6,8]` → `[[1,5],[6,8]]`；`[[1,5]]` 加 `[5,8]` → `[[1,8]]`（端点相接算重叠）。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（返回新列表）。

**拓展优化。**
- 用 `bisect` 在 `O(log n)` 内找到第一段与第二段的边界，再用切片拼接 `intervals[:lo] + [[start, end]] + intervals[hi:]`；列表拷贝仍是 `O(n)`，真正 `O(log n)` 需要平衡树。
- 需要原地修改时，可以用切片赋值 `intervals[lo:hi] = [[start, end]]`。

**易错点。**
- 第一段条件写成 `<=`：`[[1,5]]` 加 `[5,8]` 会把 `[1,5]` 当成「在左边」，得到 `[[1,5],[5,8]]`，应为 `[[1,8]]`；端点相等算重叠，所以第一段用严格小于。
- 第二段把 `start` 直接赋成旧区间的起点而不是 `min`：`[[3,5]]` 加 `[0,4]` 会得到 `[[3,5]]`，应为 `[[0,5]]`；`end` 同理必须用 `max`。
- 空列表：三段循环都不执行，直接得到 `[newInterval]`。

**追问。**
- 不合并，只判断能否插入且不重叠（LC 729 我的日程安排表 I）：二分找邻居判断。
- 要求原地且 `O(1)` 额外空间：从右向左在同一个数组里搬运，只对数组语言有意义。

**同模式。** LC 56 合并区间、LC 435 无重叠区间、LC 986 区间列表的交集、LC 252 会议室、LC 759 员工空闲时间。
