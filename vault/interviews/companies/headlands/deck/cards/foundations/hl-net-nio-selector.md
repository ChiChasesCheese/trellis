---
id: hl-net-nio-selector
node: foundations.networking-basics
type: qa
step: 31
---
## Q
阻塞 I/O 为什么撑不住大量连接（C10K）？`Selector` 怎么解决，底层用什么机制？

## A
阻塞的 `Socket.getInputStream().read(...)` 调用后线程睡眠直到有数据。服务 N 个连接要 N 个线程（每个 1 MB 栈、上下文切换）。**C10K 问题**（1999）：怎么在一台机器上处理 1 万个并发连接？答案是 **I/O 多路复用**：一个线程同时监视很多套接字，哪个有数据就处理哪个。

`Selector` 封装 OS 的多路复用：Linux 的 **epoll**、macOS / BSD 的 **kqueue**（更老的 `select` / `poll`）。循环：`selector.select()` 睡到至少一个通道就绪 → 对每个就绪 key 分情况：可接受（accept 并设为非阻塞、注册可读）、可读（读数据）、可写（写剩余数据）。
