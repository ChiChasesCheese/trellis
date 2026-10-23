---
id: hl-javaq-f-q28-treiber
node: java-questions.f-concurrency
type: qa
step: 13
---
## Q
实现一个线程安全的计数器和一个无锁栈（Treiber stack）的思路是什么？`VarHandle` 是干什么的？
Implement a thread-safe counter / a lock-free stack. What's `VarHandle` for?

## A
- **线程安全计数器**：`AtomicLong.incrementAndGet()`；高竞争统计用 `LongAdder`。
- **Treiber 栈**：`AtomicReference<Node> head`；push：新节点的 `next = head.get()`，再 `compareAndSet(old, node)`，失败就重试；pop 同理，CAS 把 `head` 改成 `head.next`。要注意 ABA（用不可变节点或版本戳）。
- **`VarHandle`**：对字段、数组元素、堆外缓冲做**细粒度内存序**操作：`getAcquire` / `setRelease` / `compareAndSet`；跨进程共享内存的可见性也用它。
