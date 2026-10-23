---
id: hl-javaq-rubric-f-strong
node: java-questions.rubric
type: qa
step: 9
---
## Q
回答并发与内存模型的问题时，"强"的答案要覆盖哪些点？

## A
- JMM 的目的与 happens-before 规则（监视器、volatile、start / join、传递性）。
- `volatile` = 可见性 + 有序性但**非原子**，能举例并说"`count++` 要用 atomic / `LongAdder`"。
- `synchronized` vs `ReentrantLock`，及 21 里的 pinning。
- CAS 的原理、ABA、高竞争下 CAS 重试的问题。
- `HashMap` 的 `h ^ (h>>>16)`、2 的幂、扩容、树化阈值（8 与表 ≥ 64）。
- `ConcurrentHashMap` Java 8 的 CAS + 桶头 `synchronized`，禁止 null 的原因。
- 虚拟线程的适用 / 不适用。
- 线程池参数顺序和无界队列陷阱。
- 安全发布与 DCL 的 `volatile`；`final` 字段语义。
