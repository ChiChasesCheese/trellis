---
id: hl-cq-q35-linux-tools-sys-net
node: cpp-questions.h-os
type: qa
step: 20
---
## Q
Linux 上排查：（1）负载、上下文切换、运行队列；（2）网络；（3）文件或端口被谁占用——各用什么命令？常见的抖动（jitter）来源有哪些？

## A
- **负载、上下文切换、运行队列**：`top` / `htop`、`vmstat 1`、`mpstat -P ALL 1`、`pidstat -w 1`（每进程切换数）。
- **网络**：`ss -tanp`、`ip -s link`、`tcpdump`、`ethtool -S`。
- **文件 / 端口被谁占用**：`lsof -p PID`、`lsof -i :端口`。
- **抖动来源**：调度器抢占、中断、缺页、频率调节、NUMA。
