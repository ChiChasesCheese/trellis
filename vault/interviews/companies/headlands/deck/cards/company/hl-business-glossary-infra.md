---
id: hl-business-glossary-infra
node: company.business
type: qa
step: 18
---
## Q
这几个词各一句话怎么定义：计算集群（compute farm）、co-location、NUMA 与 processor affinity、自营交易公司（prop firm）？

## A
- **compute farm**：一大批机器 + 作业调度，并行跑大量互相独立的作业（如回测）。
- **co-location**：把服务器放在交易所机房里，缩短物理距离。
- **NUMA**：多路 CPU 的内存分区，访问"远端"内存更慢。
- **processor affinity**：把线程绑在某个核上，减少调度抖动和缓存失效。
- **prop firm**：用自己的钱交易、没有客户的公司。

用 NUMA 和 affinity 回答"为什么延迟会抖"：线程在核之间迁移会丢掉缓存。
