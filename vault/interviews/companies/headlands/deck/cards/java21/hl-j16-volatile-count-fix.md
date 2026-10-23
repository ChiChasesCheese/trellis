---
id: hl-j16-volatile-count-fix
node: java21.j16-concurrency-primitives
type: qa
step: 9
---
## Q
`volatile int count; void inc() { count++; }` 为什么仍然错？怎么改？

## A
`count++` 是读-加-写三步，`volatile` 只保证单次读写可见，不保证复合操作原子。两线程读到同一旧值各写回一次，**丢一次更新**。

改法：`AtomicInteger.incrementAndGet()`、`LongAdder.increment()` 或加锁。同理 `volatile long n; n++` 照样丢更新；`volatile int[] a` 只让**引用**可见，元素读写不是 volatile，元素级用 `AtomicIntegerArray` 或 `MethodHandles.arrayElementVarHandle`。
