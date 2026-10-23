---
id: hl-os-calc-syscall-cpu
node: foundations.os-processes-threads-ipc
type: qa
step: 41
---
## Q
估算：一个服务每秒处理 100 万条消息，每条一次系统调用（600 ns），系统调用占多少 CPU？批量处理能降到多少？

## A
10⁶ × 600 ns = 0.6 秒 / 秒，即一个核的 **60%**。如果批量处理 100 条才调一次系统调用，降到 **0.6%**。
