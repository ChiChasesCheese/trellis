---
id: hl-javaq-g-q36-perf
node: java-questions.g-os
type: qa
step: 9
---
## Q
用 `perf` 分析 Java 进程要注意什么？`perf stat` 的 IPC 怎么解读？热线程怎么对应到 Java 代码？

## A
- **`perf stat`**：看 IPC（每周期指令数）——低 IPC（< 1）通常是等内存（缓存未命中）；另看 `cache-misses`、`branch-misses`、`context-switches`。
- **`perf record -g`** 采样调用栈，再 `perf report` 或画火焰图。
- **Java 的陷阱**：JIT 生成的代码在 perf 眼里没有符号。方案：`-XX:+PreserveFramePointer` + perf-map-agent，或 async-profiler；JDK 17+ 有 `jcmd <pid> Compiler.perfmap`（Linux 专属）。
- 其他：`perf c2c` 找伪共享；`perf sched` 看调度延迟；`perf trace` 类似 strace 但开销低。
- **线程对应**：`top -H` 里的线程号转十六进制 = `jstack` 里的 `nid=0x…`。
