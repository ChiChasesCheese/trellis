---
id: hl-cx-quicksort-worst
node: foundations.complexity
type: qa
step: 14
---
## Q
快速排序（quicksort）什么时候是 O(n log n)，什么时候退化成 O(n²)？怎么避免？Java 的 `Arrays.sort` 是怎么做的？

## A
快排每次选主元（pivot），把数组分成「比它小」和「比它大」两堆再递归。
- 主元总接近中位数：每次折半，log n 层、每层处理 n 个元素，O(n log n)。
- 主元总是最小（数组已排好序而你总选第一个）：每次只去掉 1 个，n + (n−1) + … = **O(n²)**。

修补：随机选主元、三数取中。Java 的 `Arrays.sort(int[])` 是 dual-pivot quicksort，检测到劣化会转堆排序避开最坏输入；`Arrays.sort(Object[])` 用 TimSort（归并类），保证 O(n log n) 且**稳定**。
