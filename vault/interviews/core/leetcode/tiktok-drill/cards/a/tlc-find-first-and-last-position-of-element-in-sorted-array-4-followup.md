---
id: tlc-find-first-and-last-position-of-element-in-sorted-array-4-followup
node: a.find-first-and-last-position-of-element-in-sorted-array
type: qa
step: 4
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜追问

面试官接着问：（1）只问 `target` 出现了几次？（2）数组元素是浮点数，或要在按某个字段排序的对象列表里找？（3）数组被旋转过（LC 33），还能二分吗？

## A
1. **出现次数。** `bisect_right(nums, target) - bisect_left(nums, target)`，两次二分 `O(log n)`；`[5,7,7,8,8,10]` 里 `8` 出现 `2` 次。
2. **浮点数与对象。** 不能用 `target + 1` 代表“大于 `target` 的最小值”，浮点数没有后继，所以终点必须用 `bisect_right` 这样的“严格大于”版本，不要依赖整数性质。对象列表用 `key=`：`bisect_left(items, 3, key=lambda p: p[0])`，`items = [(1,'a'),(3,'b'),(5,'c')]` 得到 `1`；注意 `key` 只作用于列表元素，查找值 `3` 保持原样。
3. **旋转数组。** 整体不再单调，但任取 `mid`，`[lo, mid]` 与 `[mid, hi]` 至少有一半是有序的。先判断哪一半有序，再看 `target` 是否落在这一半的值域内，从而丢掉另一半，每步仍减半，`O(log n)`；含重复元素（LC 81）时可能退化成 `O(n)`，因为 `nums[lo] == nums[mid] == nums[hi]` 时无法判断哪边有序。

**Python 提醒**：`bisect.insort` 虽然用二分找位置，插入列表本身是 `O(n)`；需要频繁插入的有序序列，用 `sortedcontainers.SortedList`（第三方）或堆，别指望 `insort` 做到整体 `O(log n)`。
