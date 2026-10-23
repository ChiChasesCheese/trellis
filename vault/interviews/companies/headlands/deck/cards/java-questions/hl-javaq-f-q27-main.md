---
id: hl-javaq-f-q27-main
node: java-questions.f-concurrency
type: qa
step: 7
---
## Q
`synchronized` 和 `ReentrantLock` 有什么区别、开销如何？虚拟线程出现后有什么变化？
`synchronized` vs `ReentrantLock` — differences, cost, and what changed with virtual threads?

## A
一句话：两者语义相近（互斥 + 可见性 + 可重入）；`ReentrantLock` 多了 `tryLock`、可中断、公平性、多个 `Condition`，需手动 `unlock`（放进 `finally`）；`synchronized` 简洁、自动释放、JIT 可做锁消除 / 粗化。**JDK 21 里虚拟线程在 `synchronized` 里阻塞会 pin 住载体线程，`ReentrantLock` 不会。**

```java
lock.lock();
try { /* critical section */ }
finally { lock.unlock(); }
```
- `synchronized` 用对象头 mark word 里的锁状态：无竞争轻量，有竞争膨胀成 monitor。
- `ReentrantLock` 基于 AQS（`AbstractQueuedSynchronizer`），纯 Java。
