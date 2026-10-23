---
id: hl-c13-lock-free-truth
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 15
---
## Q
lock-free 和 wait-free 有什么区别？无锁一定更快吗？什么时候选 `mutex` 而不是无锁？

## A
- **lock-free**：系统整体总有进展（某个线程失败是因为别的线程成功了）；**wait-free**：每个线程都在有限步内完成。多数 CAS 循环是 lock-free 不是 wait-free。
- 无锁 ≠ 更快：高争用下 CAS 重试可能比互斥锁更糟。SPSC 之所以好用，是因为它没有争用。
- 无锁结构的难点是**内存回收**和**正确性验证**，不是 CAS 本身。
- 选 `mutex` 的情况：保护多变量不变式、争用不高、没有性能证据、需要阻塞等待条件。除非性能分析证明锁是瓶颈，先用 `mutex`。
