---
id: hl-javaq-f-q27-cost
node: java-questions.f-concurrency
type: qa
step: 8
---
## Q
每个线程 500 万次受保护的 `++`，1、4、8 个线程下 `synchronized`、`ReentrantLock`、`AtomicLong`、`LongAdder` 各约多少毫秒？能不能说"ReentrantLock 比 synchronized 快"？

## A
- **1 线程**：synchronized 13 / ReentrantLock 16 / AtomicLong 6 / LongAdder 12。
- **4 线程**：115 / 131 / 195 / 13。
- **8 线程**：228 / 236 / 320 / 17。
- 两种锁**同一数量级**，不要说"ReentrantLock 比 synchronized 快"（Java 6 之后基本拉平）；偏向锁已移除。
- 选择：简单互斥 → `synchronized`；要超时、可中断、公平、多条件 → `ReentrantLock`；读多写少 → `StampedLock` / `ReadWriteLock`（要测）。
- 公平锁排队、吞吐低；非公平允许插队、吞吐高、可能饥饿。
- 锁膨胀：对象头从无锁 → 轻量 → 重量 monitor。
