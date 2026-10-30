---
id: tlc-merge-intervals-4-followup
node: p1.merge-intervals
type: qa
step: 4
---
## Q
**LC 56 合并区间**｜追问

面试官接着问：（1）输入已经按起点排好序，再插入一个新区间（LC 57）能做到 `O(n)` 吗？（2）区间不断一个个到达，怎么维护？（3）只要被覆盖的总长度？

## A
1. **插入区间，`O(n)`**：已有区间互不重叠且有序，分成三类：完全在新区间左边的（`end < new.start`）、完全在右边的（`start > new.end`）、与它重叠的。重叠的那批合并成一个，三段拼起来。

```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    left = [iv for iv in intervals if iv[1] < new[0]]       # 完全在 new 左边
    right = [iv for iv in intervals if iv[0] > new[1]]      # 完全在 new 右边
    mid = [iv for iv in intervals if iv[1] >= new[0] and iv[0] <= new[1]]   # 与 new 重叠
    if mid:
        new = [min(new[0], mid[0][0]), max(new[1], mid[-1][1])]
    return left + [new] + right
```

`insert([[1,3],[6,9]], [2,5])` → `[[1,5],[6,9]]`；`insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8])` → `[[1,2],[3,10],[12,16]]`。
2. **流式到达**：用一个按起点有序的列表，新区间用 `bisect` 找到插入位置，向左右吞并重叠的邻居，每次插入 `O(log n)` 定位加合并代价；数据量很大时换平衡树。
3. **覆盖总长度**：合并后 `sum(e - s for s, e in merge(intervals))`，例如 `[[1,3],[2,6],[8,10]]` 总长 `7`。注意是连续长度，不是区间个数。

**Python 提醒**：`sorted(intervals)` 返回新列表，但里面的内层列表还是原对象；若不想改动调用方的数据，合并时要新建 `[start, end]`，不要把原来的内层列表直接放进结果再原地修改。
