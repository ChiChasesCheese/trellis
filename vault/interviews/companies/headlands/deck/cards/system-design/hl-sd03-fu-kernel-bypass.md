---
id: hl-sd03-fu-kernel-bypass
node: system-design.sd03-low-latency-trading
type: qa
step: 36
---
## Q
追问：内核旁路是什么？Java 怎么用？

## A
绕过内核协议栈，应用直接轮询网卡环形队列：省系统调用（约 0.1–1 µs）、中断、内核 / 用户拷贝、调度唤醒；典型内核栈单跳几 µs–十几 µs，旁路约 1 µs 或更低（量级）。实现：DPDK 轮询驱动、Solarflare OpenOnload / ef_vi 一类用户态栈。

代价：独占核心 100% 忙等、特殊网卡驱动、调试困难、功能受限（防火墙、`tcpdump` 等工具）。Java：多数通过对 socket 透明的用户态栈（`LD_PRELOAD`）或 JNI / FFM 调本地库；普通内核栈下用 NIO `Selector` + `TCP_NODELAY`。

可以说：「旁路省的是内核这一跳，不是网线；Java 用透明的用户态栈最省事。」
