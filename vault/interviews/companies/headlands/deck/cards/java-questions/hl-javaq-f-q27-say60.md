---
id: hl-javaq-f-q27-say60
node: java-questions.f-concurrency
type: qa
step: 32
---
## Q
用英文 60 秒回答：`synchronized` vs `ReentrantLock` - differences, cost, and what changed with virtual threads?

## A
结构：语义相同 → synchronized 简洁且 JIT 可优化 → ReentrantLock 多出超时、可中断、公平、多条件 → 性能相当 → 21 里 synchronized 内阻塞会 pin 载体线程（2.4 秒对 0.35 秒）。

> "Both give mutual exclusion, visibility and reentrancy. `synchronized` is built into the language, releases automatically, and the JIT can elide or coarsen locks. `ReentrantLock` is a library lock built on AQS with `tryLock`, interruptible and timed acquisition, optional fairness and multiple conditions, at the price of a manual `unlock` in `finally`. Performance is about the same since Java 6 - in my test with eight contended threads they were within a few percent. The practical difference in Java 21 is virtual threads: blocking inside `synchronized` pins the carrier thread - with one carrier, eight 200-ms sleeps took 2.4 seconds inside `synchronized` versus 0.35 seconds outside - whereas `ReentrantLock` lets the virtual thread unmount."
