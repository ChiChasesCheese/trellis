---
id: tlc-patterns-intervals-sweep-2-template
node: patterns.intervals-sweep
type: qa
step: 2
---
## Q
**区间与扫描线｜模板：合并区间与能否参加全部会议**

写出合并区间（LC 56）和判断能否参加所有会议（LC 252）的模板，端点相接的情况怎么处理？

## A
```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    res: list[list[int]] = []
    for start, end in sorted(intervals):          # 按左端点排序
        if res and start <= res[-1][1]:           # 与上一个区间重叠（含端点相接）
            res[-1][1] = max(res[-1][1], end)     # 取更大的右端点：可能被完全包含
        else:
            res.append([start, end])
    return res
```

运行：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`；`[[1,4],[4,5]]` → `[[1,5]]`；`[[1,4],[2,3]]` → `[[1,4]]`；`[[1,4],[0,4]]` → `[[0,4]]`。时间 `O(n log n)`（排序），空间 `O(n)`。

```python
from itertools import pairwise
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    intervals.sort()
    return all(a[1] <= b[0] for a, b in pairwise(intervals))   # 前一场结束 <= 后一场开始
print(can_attend_meetings([[0,30],[5,10],[15,20]]), can_attend_meetings([[7,10],[2,4]]), can_attend_meetings([]))
# False True True
```

- **相接是否重叠**由题目决定：LC 56 里 `[1,4]` 与 `[4,5]` 合并（`start <= last_end`）；LC 252 里在 `t` 结束的会议与在 `t` 开始的会议**不**冲突（`prev_end <= next_start` 才可行）。
- `sorted(intervals)` 对 `[start, end]` 列表先比较 `start`，再比较 `end`，无需 `key`。
- 修改的是 `res[-1][1]`：`res` 里的区间是新建的列表，不会改动输入。
