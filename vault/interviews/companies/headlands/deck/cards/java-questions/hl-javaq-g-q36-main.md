---
id: hl-javaq-g-q36-main
node: java-questions.g-os
type: qa
step: 7
---
## Q
一个 Java 服务线上变慢，你怎么用 `top`、`vmstat`、`perf`、`strace` 一步步排查？
A Java service is slow in production. Walk me through how you would investigate with `top`, `vmstat`, `perf` and `strace`.

## A
一句话：先看全局再下钻，用 **USE 方法**（对每种资源看利用率、饱和度、错误）。

1. **机器层面**：`top`（load、`%us %sy %wa %st`）、`vmstat 1`、`iostat -x 1`（磁盘 util、await、队列）、`ss -s / ss -ti`（连接数、重传、rtt、拥塞窗口）→ 判断是 CPU、内存、磁盘还是网络。
2. **进程 / 线程**：`top -H -p PID` 找热线程。
3. **热点**：`perf top -p PID` / `perf record -g` / `perf stat`。
4. **系统调用**：`strace -c -f -p PID`、`strace -T`。
5. **回到 JVM**：`jcmd PID Thread.print`、JFR、GC 日志。
