---
id: hl-cx-log-everywhere
node: foundations.complexity
type: qa
step: 19
---
## Q
哪些常见场景的复杂度里有 log n？为什么 Big-O 里不用写对数的底数？

## A
- **二分查找**：每次丢一半。
- **平衡二叉树 / 堆的高度**：每往下一层节点数翻倍，n 个节点只有约 log₂ n 层，`TreeMap`、`PriorityQueue` 的 O(log n) 就是「从根走到叶子」。
- **数字的位数**：n 有 log₁₀ n + 1 位十进制、log₂ n + 1 位二进制。
- **分治递归的层数**：归并排序每层拆半，共 log n 层。

底数不用写：`log₂ n` 与 `log₁₀ n` 只差固定倍数（约 3.32），Big-O 忽略常数倍，统称 O(log n)。
