---
id: uth-java-priorityqueue-1-heap
node: java.priorityqueue
type: qa
step: 1
---
## Q
**PriorityQueue 遍历为什么不是有序的**｜Java · OpenJDK 25

依次 `add` 5、3、8、1、9、2 后打印 `PriorityQueue`，输出是什么？为什么不是排好序的？

## A
**结构。** 数组上的二叉最小堆（binary heap）：`queue[n]` 的两个孩子是 `queue[2n+1]` 和 `queue[2n+2]`，最小的在 `queue[0]`。

**细节。**

- 实测打印 `[1, 3, 2, 5, 9, 8]`，只保证堆序（父不大于子），不保证全局有序；连续 `poll` 才得到 `1 2 3 5 8 9`。
- 默认初始容量 11；容量小于 64 时扩为 `2n+2`，否则加 50%。
- `offer`、`poll` 是 O(log n)，`peek` 是 O(1)，`remove(Object)` 要先线性查找，是 O(n)。
- 最大堆传 `Comparator.reverseOrder()`。

**为什么。** 堆只维护「最小的在最前」这一点，比完整排序便宜得多。

**对应 LeetCode：** LC 215 数组中的第 K 个最大元素 · LC 23 合并 K 个升序链表
