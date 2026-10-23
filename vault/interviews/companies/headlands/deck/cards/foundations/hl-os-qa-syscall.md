---
id: hl-os-qa-syscall
node: foundations.os-processes-threads-ipc
type: qa
step: 37
---
## Q
面试题：什么是系统调用，为什么要尽量少？

## A
推荐答法：「用户态通过 syscall 指令请求内核服务，要切模式、保存恢复寄存器、校验参数，Meltdown 缓解的内核上还要切页表，再加缓存污染。macOS 上最轻的 `write` 约 600 ns，不进内核的 libc 调用只要几 ns。优化：批量、聚集 I/O、`Selector`、共享内存、内核旁路。」
