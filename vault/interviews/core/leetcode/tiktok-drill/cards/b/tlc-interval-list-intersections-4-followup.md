---
id: tlc-interval-list-intersections-4-followup
node: b.interval-list-intersections
type: qa
step: 4
---
## Q
**LC 986 区间列表的交集**｜追问

面试官接着问：（1）要求 `k` 个列表的公共交集？（2）要求两个列表的**并集**？（3）输入没有排序、内部也可能重叠？

## A
1. **`k` 个列表**：交集满足结合律，逐个折叠即可。每次结果长度不会超过参与者的总长度，总代价 `O(k * L)`（`L` 是最长列表长度的量级）。

```python
from functools import reduce

def intersect_many(lists: list[list[list[int]]]) -> list[list[int]]:
    return reduce(interval_intersection, lists)
```

   例：`[[1,5],[8,12]]`、`[[2,9],[11,20]]`、`[[4,11]]` → `[[4,5],[8,9],[11,11]]`。
2. **并集**：两个列表一起按起点排序（它们各自已有序，可用 `heapq.merge(first, second)` 线性归并），再按 LC 56 合并：当前起点 `<=` 上一段终点就扩张终点，否则新开一段。注意闭区间 `[1,3]` 与 `[3,5]` 相接于点 3，应合并。
3. **未排序或重叠**：每个列表先排序并合并重叠区间，化成已排序且不相交的前提；代价 `O(m log m + n log n)`，再线性求交。

**Python 提醒**：`reduce` 在空列表上不给初值会抛 `TypeError`；`k` 可能为 0 时写 `reduce(f, lists, [[0, 10**9]])`，用「全集」当单位元。
