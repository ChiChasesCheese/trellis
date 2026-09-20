---
id: problems-lock-service-server-primitives-vs-client-recipes
node: problems.foundations.lock-service
type: qa
step: 2
tags: [grown]
---
## Q
In a Chubby/ZooKeeper/etcd-class coordination service design, why does the server API expose only generic primitives (create/delete/read/watch on hierarchical nodes, plus sessions) instead of dedicated lock() and electLeader() RPCs?

## A
Because locks, leader election, and group membership are recipes composed from those primitives (typically using ephemeral and sequential nodes) rather than server-level concerns, and different applications need different recipe semantics — fair queueing versus preemption, exclusive locks versus shared read/write locks. Baking one specific recipe's semantics into the server would force every application to accept that one choice. Keeping the server limited to a small set of primitives lets it stay simple enough to reason about and prove safe under consensus, while client libraries implement whichever recipe a given application actually needs on top of the same primitive API.

## Q zh
在一个 Chubby/ZooKeeper/etcd 类协调服务设计中，为什么服务端 API 只暴露一组通用原语（对分层节点的创建/删除/读取/watch，加上会话），而不是提供专门的 lock() 和 electLeader() 这类 RPC？

## A zh
因为锁、leader 选举、组成员管理都是由这些原语（通常配合临时节点和顺序节点）组合出来的配方，而不是服务端该关心的事情，而且不同应用需要不同的配方语义——公平排队还是抢占、独占锁还是共享读写锁。把某一种具体配方的语义写死进服务端，会强迫所有应用都接受那一种选择。把服务端限制在一小组原语上，能让它保持足够简单、足以在共识之下被证明安全；具体某个应用需要哪种配方，交给客户端库在同一套原语 API 之上各自实现。
