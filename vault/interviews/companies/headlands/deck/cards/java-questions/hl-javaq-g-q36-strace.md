---
id: hl-javaq-g-q36-strace
node: java-questions.g-os
type: qa
step: 10
---
## Q
`strace -c -f -p PID` 怎么用？它有什么风险？输出里 `futex`、`write`、`fsync`、`epoll_wait` 占比大分别意味着什么？

## A
- 用法：`-c` 按系统调用汇总次数与时间；`-f` 跟随线程；`-T` 显示每个调用耗时；`-e trace=network` / `file` 过滤。
- **风险**：strace 用 `ptrace`，会把目标进程拖慢**一个数量级**，生产上谨慎，优先 `perf trace` 或 eBPF。
- 典型发现：
  - `futex` 占比大 → **锁竞争**；
  - `write` 小而多 → 缺批量 / Nagle 问题；
  - `fsync` 慢 → 存储问题；
  - `epoll_wait` 占比高但 CPU 低 → 其实在等 I/O。
