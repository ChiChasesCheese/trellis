---
id: tlc-employee-free-time-0-whole
node: c.employee-free-time
type: qa
---
## Q
**LC 759 员工空闲时间**｜Hard · LC TikTok 全时段热度 26/100

给定员工的 `schedule`，每个员工有一个已排好序、互不重叠的工作时间段列表（`Interval`，有 `start` 和 `end` 属性）。返回所有员工**共同**的、长度为正的、有限的空闲时间段，按开始时间排序。`schedule` 与 `schedule[i]` 的长度在 `[1, 50]` 内，`0 <= schedule[i].start < schedule[i].end <= 10^8`。例：`schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`（`[-inf,1]` 和 `[10,inf]` 不是有限区间，不返回）；`schedule = [[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]` → `[[5,6],[7,9]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把所有员工的忙碌区间摊平按开始时间排序，扫描时维护「目前最晚的结束时刻」，下一段开始晚于它的空档就是共同空闲。

**识别。** 「所有人都空闲」等于「没有任何人忙碌」，即所有忙碌区间的并集的补集；求并集的补集是合并区间的套路，不用逐个员工比较。

**推导。** 暴力：在时间轴上逐点标记谁忙，值域 `10^8` 不可行。洞察：把所有区间合并成并集，相邻两段之间的空隙就是答案。排序后用 `reach` 记录已覆盖的最远位置，`iv.start > reach` 说明出现空隙，端点相接（`start == reach`）不算正长度的空闲。

```python
class Interval:
    def __init__(self, start: int = 0, end: int = 0) -> None:
        self.start = start
        self.end = end


def employee_free_time(schedule: list[list[Interval]]) -> list[Interval]:
    # 所有员工的工作区间摊平，按开始时间排序
    busy = sorted((iv for person in schedule for iv in person), key=lambda iv: iv.start)
    free: list[Interval] = []
    reach = busy[0].end                          # 目前为止所有人最晚忙到的时刻
    for iv in busy[1:]:
        if iv.start > reach:                     # 下一段工作晚于之前所有人的结束：中间是共同空闲
            free.append(Interval(reach, iv.start))
        reach = max(reach, iv.end)
    return free
```

运行：示例一 `[[3,4]]`；示例二 `[[5,6],[7,9]]`；`[[[1,2]],[[2,3]]]` → `[]`（端点相接）；单个员工单个区间 → `[]`。

**复杂度。** 时间 `O(N log N)`（`N` 为区间总数），空间 `O(N)`。

**拓展优化。**
- 每个员工的区间本来就有序，用 `heapq.merge` 做 `k` 路归并，省去整体排序，时间 `O(N log k)`：

```python
from heapq import merge


def employee_free_time_kway(schedule: list[list[Interval]]) -> list[Interval]:
    # 每个员工自己的区间已有序，heapq.merge 做 k 路归并，不必整体排序
    busy = merge(*schedule, key=lambda iv: iv.start)
    free: list[Interval] = []
    first = next(busy)
    reach = first.end
    for iv in busy:
        if iv.start > reach:
            free.append(Interval(reach, iv.start))
        reach = max(reach, iv.end)
    return free
```

**易错点。**
- 空隙判断写成 `>=`：端点相接的区间 `[1,2]` 与 `[2,3]` 会产生长度为 0 的 `[2,2]`，题目要求长度为正。
- `reach` 直接赋成当前区间的 `end` 而不是取最大：被一个很长的区间覆盖的情形下，后面短区间会让 `reach` 倒退，`[[1,10]]` 与 `[[2,3],[5,6]]` 会错误地产生空闲 `[3,5]`。
- 把无穷区间也返回：只在忙碌区间之间找空隙，最前面和最后面的无限区间自然不会出现。

**追问。**
- 指定一个工作窗口 `[T0, T1]`：在首尾补上空档 `[T0, first.start]` 和 `[last_end, T1]`。
- 找出至少有 `m` 个人空闲的时间段：改用事件扫描线，`+1/-1` 计数。

**同模式。** LC 56 合并区间、LC 57 插入区间、LC 253 会议室 II、LC 986 区间列表的交集、LC 1235 规划兼职工作。
