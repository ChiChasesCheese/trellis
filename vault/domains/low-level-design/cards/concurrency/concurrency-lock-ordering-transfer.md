---
id: concurrency-lock-ordering-transfer
node: concurrency.hazards
type: qa
---
## Q
锁定顺序如何防止死锁？什么是锁定转移？

## A
**锁定顺序**（Consistent Lock Ordering）：
- 所有线程以相同的顺序获取锁
```
线程 1：获取 lockA，然后 lockB
线程 2：获取 lockA，然后 lockB
```
- 消除循环等待（四个死锁条件之一）

**锁定转移**（Lock Transfer）：
- 不释放锁，而是将其所有权转移给另一个线程
- 例子：一个线程已完成其工作，将锁传递给下一个线程
- 避免释放和重新获取的开销
- 在 Java 中不直接支持，但在 spinlock 或无锁数据结构中可以模拟

锁定顺序的问题：
- 强制所有代码路径遵循相同的顺序
- 添加新的锁时需要小心
- 可能与对象图中的自然依赖不一致
