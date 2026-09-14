---
id: kafka-practice-cruise-control-scale-purpose
node: practice.kubernetes-strimzi
type: qa
source: kafka-2e
---
## Q
Cruise Control 最初是为了解决什么问题而设计的？除了这个最初目标，它后来还扩展支持了哪些运维能力？对多大规模的集群来说，使用它几乎是必需的？

## A
Cruise Control 最初是一种自动化的集群数据再均衡（rebalance，把数据/分区在 broker 之间重新分布得更均匀）解决方案，用来解决大规模集群里手动检查指标、手动做分区重分配这种运维方式难以为继的问题。在此基础上，它后来又扩展支持了异常检测和操作管理能力，比如自动化地添加和移除 broker。对于包含数百个集群、数千个 broker 这种规模的大型部署来说，人工维持集群均衡几乎不可行，Cruise Control 这类自动化工具就成了除测试集群之外几乎必备的运维工具。
