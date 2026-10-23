---
id: hl-heap-trap-thread-remove
node: foundations.heap-priority-queue
type: qa
step: 28
---
## Q
`PriorityQueue` 是线程安全的吗？在百万元素队列里每处理一个事件就 `remove(obj)` 会怎样？

## A
- **不是线程安全**。多线程读写用 `java.util.concurrent.PriorityBlockingQueue`（单把锁，内部同样是堆）或自己加锁。高并发低延迟场景更常见的设计是**单线程拥有堆**，其他线程通过队列把任务或事件交给它。
- `remove(Object)` 和 `contains` 是 **O(n)**：百万元素上每个事件都 `remove(obj)`，整体 O(n²)。改用懒删除或索引堆。
