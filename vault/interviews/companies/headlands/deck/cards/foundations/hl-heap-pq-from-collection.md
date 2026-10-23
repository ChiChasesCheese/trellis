---
id: hl-heap-pq-from-collection
node: foundations.heap-priority-queue
type: qa
step: 29
---
## Q
`new PriorityQueue<>(Collection)` 传入不同类型的集合时行为有什么区别？Java 有现成的「最大 k 个」API 吗？

## A
- 传入 `SortedSet` 或另一个 `PriorityQueue`：构造器**沿用它的比较器**并直接拷贝（已是合法顺序，不用重新 heapify）。
- 传入其他 `Collection`：用自然顺序并 heapify；元素不可比较则构造时抛 `ClassCastException`。

没有「最大 k 个」的现成 API，要自己写 top-k（大小为 k 的小根堆，O(n log k)）。`stream().sorted().limit(k)` 是 O(n log n)。
