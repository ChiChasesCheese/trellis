---
id: hl-net-kernel-bypass
node: foundations.networking-basics
type: qa
step: 30
---
## Q
内核旁路（kernel bypass）是什么？标准路径慢在哪，旁路怎么做，有哪些代表技术和代价？

## A
标准路径：网卡中断（或轮询）→ 内核协议栈 → socket 缓冲区 → 你调 `read` / `recv`（系统调用）→ 内核拷贝到你的缓冲区。每步微秒量级，外加一次内核 / 用户态切换和一次拷贝。

**内核旁路**让用户态程序直接操作网卡：把网卡收发环形队列映射到用户态内存，程序**轮询**队列、在用户态解析协议，没有内核、没有系统调用、没有中断、没有拷贝，每包处理从几微秒降到几百纳秒甚至更低。

代表：**DPDK**、Solarflare / AMD 的 **OpenOnload** 与 `ef_vi`（Onload 用 `LD_PRELOAD` 拦截 socket 调用，普通程序不改代码即可）、NVIDIA 的 **VMA**、Linux 的 **AF_XDP**；`io_uring` 不是旁路，是减少系统调用。

代价：独占 CPU 核做 100% 忙轮询、特定网卡、失去 `tcpdump` / `iptables` 等常规工具、运维复杂。Java 通过 JNI / FFM 调 C 库，或用对 socket API 透明的 Onload。
