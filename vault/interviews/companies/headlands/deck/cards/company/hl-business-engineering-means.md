---
id: hl-business-engineering-means
node: company.business
type: qa
step: 13
---
## Q
交易公司为降低延迟，在语言、机房位置、操作系统和时钟上通常采取哪些工程手段？

## A
- **语言**：生产系统用 **C++**，不用 Python / R / Matlab。
- **co-location**：把服务器放进交易所机房，缩短物理距离。
- **Linux 调优**：processor affinity（把线程绑在某个核上）、NUMA（多路 CPU 的内存分区）感知，减少抖动。
- **时钟同步**：不同机器的时间戳要能互相比较。

这些手段大多属于 C++ 热路径岗；Java 岗不负责这条链路，但要听得懂这些词。
