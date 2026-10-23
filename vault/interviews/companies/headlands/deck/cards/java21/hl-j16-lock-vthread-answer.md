---
id: hl-j16-lock-vthread-answer
node: java21.j16-concurrency-primitives
type: qa
step: 28
---
## Q
面试问：「JDK 21 里为什么在虚拟线程中要用 `ReentrantLock` 而不是 `synchronized`？」
(Why prefer `ReentrantLock` over `synchronized` with virtual threads on JDK 21?)

## A
- JDK 21 里虚拟线程在 `synchronized` 内阻塞会 **pin** 住载体线程（无法卸载），载体数量有限（默认等于核数），可能耗尽吞吐；
- `ReentrantLock` 基于 `LockSupport.park`，阻塞时虚拟线程可**卸载**，载体放去跑别人；
- **JDK 24 修复了 `synchronized` 的 pinning**，之后这一理由不再成立，只按功能选锁。
