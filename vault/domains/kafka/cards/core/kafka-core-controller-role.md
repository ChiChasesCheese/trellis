---
id: kafka-core-controller-role
node: core.cluster-roles
type: qa
step: 2
source: kafka-2e
---
## Q
一个 Kafka 集群由多个 broker 组成，为什么其中需要有一个 broker 兼任「控制器」（controller）角色？它是固定指定的吗？

## A
控制器负责集群级别的管理工作，包括把分区分配给各个 broker，以及监控 broker 的存活状态。控制器不是固定指定某台机器，而是从当前存活的集群成员中自动选举产生的；如果控制器所在的 broker 失效，集群会自动选出新的控制器，从而保证集群管理功能不因单点故障而中断。
