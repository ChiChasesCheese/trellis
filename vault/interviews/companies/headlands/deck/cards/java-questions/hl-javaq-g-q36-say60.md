---
id: hl-javaq-g-q36-say60
node: java-questions.g-os
type: qa
step: 16
---
## Q
用英文 60 秒回答：A Java service is slow in production. Walk me through how you would investigate with `top`, `vmstat`, `perf` and `strace`.

## A
结构：USE 方法自上而下 → 机器层（top、vmstat、iostat、ss）→ 热线程（top -H 对 jstack nid）→ perf（IPC、火焰图，Java 要符号方案）→ strace -c（futex 表示锁竞争，但开销大）→ 回到 JVM。

> "I'd go top-down using the USE method. First the machine: `top` for CPU split and load, `vmstat 1` to read the run queue, context switches, swap and I/O wait, `iostat -x` for disk and `ss -ti` for network retransmits. If it's CPU, `top -H` gives me the hot thread, and I map its hex id to the `jstack` nid. Then `perf stat` to see IPC and cache misses - low IPC means memory stalls - and `perf record -g` for a flame graph; for Java I need frame pointers or async-profiler to get JIT symbols. Then `strace -c -f` to see where syscalls go - a lot of `futex` means lock contention - remembering strace is intrusive, so in production I'd prefer `perf trace` or eBPF. Finally back into the JVM with JFR, GC logs and thread dumps."
