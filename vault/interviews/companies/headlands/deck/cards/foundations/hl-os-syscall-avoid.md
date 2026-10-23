---
id: hl-os-syscall-avoid
node: foundations.os-processes-threads-ipc
type: qa
step: 14
---
## Q
怎样减少系统调用？vDSO 是什么？用什么工具观察系统调用？

## A
减少系统调用：
- **批量**读写（一次 `read` 64 KB 而不是 64 次 1 KB）、`BufferedOutputStream`；
- `writev` / `readv` **聚集**；
- NIO `Selector` 一次问许多连接；
- **绕过内核**：共享内存读写不需要系统调用，内核旁路网络。

**vDSO**：Linux 把 `clock_gettime`、`gettimeofday` 映射成用户态可直接调用的代码，所以 `System.nanoTime()` 在 Linux 上约 20 ns，不是真的陷入内核。

观察工具：`strace -c -f -p <pid>`（统计次数和时间）、`perf trace`、`strace -T`（每次耗时）；macOS 用 `dtruss`。
