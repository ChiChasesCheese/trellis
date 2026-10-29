---
id: uth-python-heapq-bisect-3-bisect
node: python.heapq-bisect
type: qa
step: 3
---
## Q
**bisect_left 与 bisect_right 差在哪**｜Python · CPython 3.14

对 `[1, 2, 2, 2, 3]` 查 `2`，两个函数分别返回什么？`insort` 为什么不是 O(log n)？

## A
**结构。** 在有序 `list` 上缩小 `[lo, hi)` 的二分，不额外分配内存（`bisect.py` 是纯 Python，另有 C 加速版）。

**细节。**

- 实测 `bisect_left` 返回 1（第一个 2 的位置），`bisect_right` 返回 4（最后一个 2 之后）。
- `bisect_left` 比较 `a[mid] < x`，`bisect_right` 比较 `x < a[mid]`，只用 `<`。
- `insort` 是二分加 `list.insert`，查找 O(log n)，但插入要搬动元素，整体 O(n)。

**为什么。** 3.10 起支持 `key=`，用法和 `sorted` 一致；键开销大时先预算一列键再二分。

**对应 LeetCode：** LC 34 在排序数组中查找元素的第一个和最后一个位置 · LC 35 搜索插入位置
