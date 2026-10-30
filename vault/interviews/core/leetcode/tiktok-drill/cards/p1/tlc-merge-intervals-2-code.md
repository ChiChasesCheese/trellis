---
id: tlc-merge-intervals-2-code
node: p1.merge-intervals
type: qa
step: 2
---
## Q
**LC 56 合并区间**｜写出 Python 实现

`intervals` 是区间列表，`1 <= intervals.length <= 10^4`，每个区间是 `[start, end]`，`0 <= start <= end <= 10^4`。合并所有重叠区间（端点相接也算重叠），返回互不重叠的区间列表。

## A
**思路。** 先按起点排序。结果列表里只看最后一个区间：新区间起点不超过它的终点就是重叠，把终点延长到两者较大者；否则新区间自己成为结果里的新一项。

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

运行：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`；`[[1,4],[4,5]]` → `[[1,5]]`；`[[4,7],[1,4]]` → `[[1,7]]`；`[[1,4],[0,4]]` → `[[0,4]]`；`[[1,4],[2,3]]` → `[[1,4]]`；`[[5,5]]` → `[[5,5]]`。

**复杂度。** 时间 `O(n log n)`，排序占主导；空间 `O(n)`。

**写法要点。** `sorted(intervals)` 对内层列表按字典序比较，天然先比起点再比终点，不用写 `key`；`for start, end in ...` 直接解包；`merged.append([start, end])` 新建列表，之后原地修改 `merged[-1][1]` 不会改动调用方传入的输入（如果直接 `append(interval)` 再改，就会改到输入）；`merged and ...` 先判空再取 `merged[-1]`。
