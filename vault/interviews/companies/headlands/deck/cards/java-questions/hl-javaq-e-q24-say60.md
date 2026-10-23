---
id: hl-javaq-e-q24-say60
node: java-questions.e-jit-gc
type: qa
step: 33
---
## Q
用英文 60 秒回答：Besides GC, what else makes a JVM pause? What's a safepoint?

## A
结构：safepoint 的定义与用途 → 暂停两段（到达时间、操作时间）→ 日志实例（0.1 ms 加 1.5 ms）→ 并非所有尖刺都来自 JVM（页错误、THP、CPU 争用）→ 生产用隔离核、绑核、预触碰。

> "A safepoint is a point where every Java thread is parked in a known state so the VM can do work that needs a consistent view: GC, deoptimisation, class redefinition, thread dumps. The pause has two parts - the time to reach the safepoint, which a long loop without a poll can stretch, and the time spent in the operation. `-Xlog:safepoint` prints both; for a G1 young collection I saw roughly 0.1 ms to reach and 1.5 ms of work. And not every spike is the JVM: page faults, THP compaction, CPU contention and the scheduler all show up too, which is why production latency boxes use isolated cores, pinned threads and pre-touched memory."
