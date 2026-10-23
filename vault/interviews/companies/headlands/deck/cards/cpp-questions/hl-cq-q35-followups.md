---
id: hl-cq-q35-followups
node: cpp-questions.h-os
type: qa
step: 21
---
## Q
三个追问：NUMA 是什么？怎么降低网络路径上的内核开销？futex 是什么？

## A
- **NUMA**：挂在不同插槽上的内存延迟不同；要在同一个节点上分配和运行。
- **降低内核开销**：绕过内核的网络栈（DPDK、Solarflare Onload）、忙轮询（busy polling）、批处理、绑定中断（IRQ）到特定核。
- **futex**：快速用户态互斥原语；没有竞争时操作留在用户态，只有竞争时才进入内核。
