---
id: hl-javaq-rubric-g-os
node: java-questions.rubric
type: qa
step: 11
---
## Q
回答操作系统与 Linux 性能工具的问题时，强、一般、弱的答案各有什么特征？

## A
- **强**：区分进程 / 线程 / 虚拟线程，说出上下文切换的直接与间接成本；虚拟内存、缺页、page cache、RSS vs `-Xmx`（能列出堆外组成并说出 NMT）；排查流程自上而下（`top` → `vmstat` 每一列含义 → `iostat` / `ss` → `top -H` + `jstack` nid → `perf stat` / `perf record` → `strace -c`），知道 strace 开销大、perf 看 Java 需要符号方案；JVM 侧工具：`jcmd Thread.print`、`jstat`、`GC.class_histogram`、JFR；清楚说明哪些是亲手跑过的、哪些是知识。
- **一般**：知道 `top`、`vmstat`、`strace` 的名字和大意，能说出 CPU / 内存 / 磁盘 / 网络四类资源，但不会读 `vmstat` 列，也不会连到 JVM。
- **弱**：只会"看日志""重启"；把 `load average` 当 CPU 使用率；不知道 `jstack` / `jcmd`。
