---
id: hl-heap-pq-impl
node: foundations.heap-priority-queue
type: qa
step: 21
---
## Q
`java.util.PriorityQueue` 内部是什么数据结构？有哪些构造器？初始容量和扩容规则是什么？

## A
内部是 `Object[] queue` 实现的**二叉堆**，下标公式同上；JDK 的下沉用「空洞」优化：待下沉元素拿在手里，孩子逐个上移，最后一次放入，省一半写入。

```java
new PriorityQueue<>();                                  // 自然顺序，小的先出；初始容量 11
new PriorityQueue<>(64);                                // 初始容量，必须 >= 1
new PriorityQueue<>(Comparator.reverseOrder());         // 大根堆
new PriorityQueue<>(256, Comparator.reverseOrder());
new PriorityQueue<>(List.of(9, 4, 7, 1));               // O(n) heapify
```
初始容量不能是 0（`IllegalArgumentException`）。扩容：小于 64 时翻倍加 2，否则增加一半（约 1.5 倍），几何增长，摊还 O(1)；已知规模时传初始容量能避免扩容。
