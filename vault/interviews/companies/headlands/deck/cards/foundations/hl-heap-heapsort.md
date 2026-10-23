---
id: hl-heap-heapsort
node: foundations.heap-priority-queue
type: qa
step: 17
---
## Q
堆排序（heapsort）的复杂度和性质是什么？为什么 Java 库不拿它做主排序？

## A
建堆 O(n)，poll n 次 O(n log n)，总 **O(n log n)**。原地、不稳定、不需额外数组。

实际比快排慢，因为缓存局部性差：下沉时 `i` 到 `2i+1` 跳跃大。所以 Java 库不用它做主排序，只在快排退化时当后备（`Arrays.sort(int[])` 的 dual-pivot quicksort 检测到劣化转堆排序）。
