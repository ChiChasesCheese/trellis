---
id: hl-os-ipc-choose
node: foundations.os-processes-threads-ipc
type: qa
step: 19
---
## Q
通用跨机、同机简单、同机极端低延迟、需要持久化这四种需求，IPC 各选什么？

## A
- 通用、跨机器、延迟宽松 → **TCP**（或 gRPC 之类）；
- 同机、简单、吞吐不极端 → **Unix 域套接字或管道**；
- 同机、延迟 / 吞吐极端敏感（行情 → 策略 → 网关的进程间通道）→ **共享内存 + 无锁环形缓冲**；
- 要持久化（崩溃后能重放）→ **内存映射文件**（Chronicle Queue、Aeron Archive 的思路）。
