---
id: hl-javaq-a-q03-follow-ups
node: java-questions.a-speed
type: qa
step: 13
---
## Q
追问：怎么证明热路径不分配？为什么不干脆给堆开很大并关掉 GC？`System.gc()` 或类加载造成的停顿怎么办？
How do you prove the hot path doesn't allocate? Why not just give the heap a huge size and disable GC?

## A
- **证明不分配**：`ThreadMXBean.getThreadAllocatedBytes` 在热路径前后取差；JFR 的分配事件；`-Xlog:gc` 里看不到 young GC。要靠测量，不靠直觉。
- **为什么不关 GC**：可以用 Epsilon GC（`-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC`，只分配、不回收），但只适合**短命进程或基准测试**；长跑进程堆耗尽就崩。
- **`System.gc()` 与类加载停顿**：属于"被打断"类尾部来源（GC 之外的 JVM 暂停：safepoint、类加载、页错误、OS 调度），用 `-Xlog:safepoint` 找；不要靠 `System.gc()`，`-XX:+DisableExplicitGC` 视情况使用。
