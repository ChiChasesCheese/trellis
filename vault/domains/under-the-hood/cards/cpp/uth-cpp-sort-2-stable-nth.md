---
id: uth-cpp-sort-2-stable-nth
node: cpp.sort
type: qa
step: 2
---
## Q
**stable_sort 与 nth_element 各是什么算法**｜C++ · libstdc++ 16

标准库里“稳定排序”和“取第 k 小”分别是怎么实现的？

## A
**结构。** `stable_sort` 是归并排序（merge sort）；`nth_element` 是快速选择（quickselect）。

**细节。**

- `stable_sort` 申请一块 n/2 大小的临时缓冲来归并，O(n log n)
- 缓冲申请不到时退化成不用额外内存的原地归并，标准允许慢到 O(n log² n)
- `nth_element` 每轮划分后只处理含第 n 位的一侧，平均 O(n)
- 它同样有深度上限，超限改用堆选择（heap_select）

**为什么。** 稳定要求相等元素保持原顺序，快排做不到，归并天然稳定，代价是额外空间。

**对应 LeetCode：** LC 215 数组中的第 K 个最大元素 · LC 912 排序数组
