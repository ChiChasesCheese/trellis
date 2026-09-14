---
id: kafka-internals-kraft-active-standby-controller
node: internals.kraft-mode
type: qa
source: kafka-2e
---
## Q
在 KRaft 架构下，多个控制器节点组成一个 Raft 仲裁（quorum）。这些控制器节点里谁负责真正处理请求？为什么控制器发生故障转移（failover，故障后切换到另一节点）时能很快恢复，而不像传统架构那样需要重新从头加载？

## A
Raft 选出的首领节点被称为**主控制器（active controller）**，只有它负责处理所有来自 broker 的 RPC（远程调用）请求；其余控制器节点是**跟随者控制器**，持续从主控制器复制元数据日志，充当热备。因为跟随者控制器本来就在实时同步、掌握最新状态，一旦主控制器故障需要切换，新的主控制器几乎不需要额外加载——它早已具备最新状态，因此故障转移可以很快完成，不像传统 ZooKeeper 控制器那样要等重新从 ZooKeeper 拉取全部元数据。
