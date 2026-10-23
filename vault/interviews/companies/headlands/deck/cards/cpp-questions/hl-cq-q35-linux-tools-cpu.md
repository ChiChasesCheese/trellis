---
id: hl-cq-q35-linux-tools-cpu
node: cpp-questions.h-os
type: qa
step: 19
---
## Q
Linux 上排查性能：（1）CPU 花在哪；（2）缓存未命中 / 分支预测失败 / IPC；（3）进程在做什么系统调用——各用什么命令？

## A
- **CPU 花在哪**：`perf top`，或 `perf record -g` + `perf report`，也可以画火焰图。
- **缓存未命中、分支预测失败、IPC**：`perf stat -e cache-misses,branch-misses,instructions,cycles ./prog`。
- **系统调用，卡在哪**：`strace -c -p PID`（统计）、`strace -f -tt`（时间线）。
