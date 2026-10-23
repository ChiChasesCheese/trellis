---
id: hl-heap-heapify-vs-add
node: foundations.heap-priority-queue
type: qa
step: 15
---
## Q
实测 n = 10⁶ 个随机 int，heapify 与逐个 add 的交换次数各是多少？Java 的 `PriorityQueue` 构造器怎么利用这一点？

## A
- heapify（从 n/2−1 下沉）：744,070 次交换（每元素 0.74）；
- n 次 add（上浮）：1,280,829 次（每元素 1.28）。

随机数据下只差 1.7 倍，因为随机数据对上浮很友好；但逐个 add 最坏 O(n log n)（递减输入），heapify 最坏始终 O(n)。

Java：`new PriorityQueue<>(Collection)` 对非有序集合走 heapify（O(n)）；对已有队列 `addAll` 或逐个 `add` 是逐个上浮，O(m log n)。**一开始就知道全部元素，用构造器传集合更快**。
