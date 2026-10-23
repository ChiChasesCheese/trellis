---
id: hl-heap-floyd-heapify
node: foundations.heap-priority-queue
type: qa
step: 12
---
## Q
把 n 个已在数组里的元素整理成堆，Floyd 建堆（heapify）怎么做？写出代码，复杂度是多少？

## A
从**最后一个有孩子的节点**（下标 `n/2 − 1`）**倒着**到根，对每个节点做一次**下沉**：
```java
static void heapify(int[] a) {
    int n = a.length;
    for (int i = n / 2 - 1; i >= 0; i--) {
        siftDown(a, n, i);   // 下标 >= n/2 的都是叶子，本来就合法
    }
}
```
复杂度 **O(n)**，不是 O(n log n)。对比朴素做法：逐个 `add`（上浮）共 O(n log n)。
