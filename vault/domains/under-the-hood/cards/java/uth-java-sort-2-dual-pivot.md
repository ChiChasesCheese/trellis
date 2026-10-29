---
id: uth-java-sort-2-dual-pivot
node: java.sort
type: qa
step: 2
---
## Q
**双轴快排怎么避免最坏 O(n²)**｜Java · OpenJDK 25

`Arrays.sort(int[])` 选两个轴点（pivot）把数组分成几段？构造恶意数据能让它退化吗？

## A
**结构。** 选 `pivot1 ≤ pivot2`，一趟分成三段：小于 `pivot1`、介于两者之间、大于 `pivot2`，再递归。

**细节。**

- 轴点取自五个样本，间隔近似黄金比例，有序输入也不会选到边缘。
- 递归超过 `MAX_RECURSION_DEPTH`（384）就切到堆排序，保证 O(n log n)。
- 近乎有序的数据直接合并已有的有序段。
- `byte` 数组 64 个以上、`short` 与 `char` 数组 1750 个以上，改用计数排序。

**为什么。** 有堆排序兜底，不再有数据能让它退化。JDK 11 文档只写「许多会让其他快排退化的数据」，现在写「所有数据」。

**对应 LeetCode：** LC 75 颜色分类 · LC 215 数组中的第 K 个最大元素
