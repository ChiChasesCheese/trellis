---
id: tlc-meeting-rooms-2-code
node: a.meeting-rooms
type: qa
step: 2
---
## Q
**LC 252 会议室**｜写出 Python 实现

`intervals` 是至多 `10^4` 个 `[start, end]`（`0 <= start < end <= 10^6`，可能为空）。判断一个人能否参加所有会议；一个会议的结束时间等于另一个的开始时间，不算重叠。

## A
**思路。** 按开始时间排序。然后用 `pairwise` 遍历每一对相邻会议，要求前者的结束时间 `<=` 后者的开始时间；全部满足就返回 `True`。

```python
from itertools import pairwise

def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals)                          # 按开始时间排序，不改入参
    return all(prev[1] <= cur[0] for prev, cur in pairwise(ordered))
```

运行：`[[0,30],[5,10],[15,20]]` → `False`，`[[7,10],[2,4]]` → `True`，`[]` → `True`，`[[1,2],[2,3]]` → `True`，`[[1,5]]` → `True`。

**复杂度。** 时间 `O(n log n)`：排序；扫描 `O(n)`。空间 `O(n)`：`sorted` 返回新列表；若允许改入参，用 `intervals.sort()` 可降到 `O(1)` 额外空间（不计排序栈）。

**写法要点。** `sorted(list_of_lists)` 按列表的字典序比较，先比起点、再比终点，不需要写 `key`；`itertools.pairwise`（Python 3.10+）直接给出相邻对，免去下标；`all()` 配生成器遇到第一个 `False` 就短路，空序列返回 `True`，省掉空输入的判断。
