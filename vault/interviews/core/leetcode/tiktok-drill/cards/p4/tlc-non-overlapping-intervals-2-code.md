---
id: tlc-non-overlapping-intervals-2-code
node: p4.non-overlapping-intervals
type: qa
step: 2
---
## Q
**LC 435 无重叠区间**｜写出 Python 实现

给区间数组 `intervals`（`1 <= intervals.length <= 10^5`，`-5 * 10^4 <= start_i < end_i <= 5 * 10^4`），返回使剩余区间两两不重叠所需移除的最少区间数；只在端点接触的区间不算重叠。

## A
**思路。** 移除最少等于保留最多。按右端点升序排序，维护最后一个保留区间的右端点 `end`：当前区间起点 `>= end` 就保留并更新 `end`，否则丢弃。答案是总数减保留数。

```python
from math import inf
from operator import itemgetter


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    kept, end = 0, -inf                                   # 已保留的区间数、最后保留区间的右端点
    for start, finish in sorted(intervals, key=itemgetter(1)):   # 按右端点升序
        if start >= end:                                  # 只在端点接触不算重叠，所以是 >=
            kept += 1
            end = finish
    return len(intervals) - kept
```

运行：`[[1,2],[2,3],[3,4],[1,3]]` → `1`，`[[1,2],[1,2],[1,2]]` → `2`，`[[1,2],[2,3]]` → `0`，`[[1,2]]` → `0`，`[[1,100],[2,3],[4,5]]` → `1`。

**复杂度。** 时间 `O(n log n)`，排序占主导，扫描 `O(n)`；空间 `O(n)`，`sorted` 返回新列表。

**写法要点。** `sorted` 不改变传入的 `intervals`；`itemgetter(1)` 比 `lambda x: x[1]` 更快也更直白；循环变量直接解包成 `start, finish`，避免下标；`-inf` 做初值，对负数起点也成立；`len(intervals) - kept` 把「最少移除」转成「最多保留」。
