---
id: distributed-coordination-service-primitives
node: distributed.consensus
type: qa
---
## Q
ZooKeeper and etcd are "consensus in a box." Which small set of primitives do they expose, and how do those compose into the classic recipes (distributed lock, leader election, group membership)?

## A
- **Linearizable writes / compare-and-set**: every update goes through total order broadcast, so a conditional write ("create if absent", "set if version = n") is a race with exactly one winner.
- **Ephemeral nodes / leases**: a key bound to a client session, deleted automatically when the session's heartbeats stop — liveness tied to data.
- **Watches**: subscribe to a key and get notified on change — no polling.
- **Sequence numbers**: creations get monotonically increasing ids (usable as fencing tokens).

Recipes: *leader election* = all contenders try to create the same ephemeral key; the winner leads, its session death deletes the key, watchers race again. *Lock* = same, plus sequential nodes to queue waiters fairly. *Membership* = one ephemeral key per live node; watchers see joins/leaves.

Why outsource: you get consensus-grade safety through a *key-value API*, and your own fleet stays stateless-ish — a handful of ZK/etcd nodes coordinate thousands of clients that never run consensus themselves.

## Q zh
ZooKeeper 和 etcd 是"盒装共识"。它们暴露的是哪一小组原语？这些原语如何组合出经典配方（分布式锁、leader 选举、成员管理）？

## A zh
- **线性一致写 / compare-and-set**：所有更新都经过 total order broadcast，因此条件写（"不存在才创建"、"version = n 才设置"）是一场恰好只有一个赢家的竞赛。
- **Ephemeral 节点 / lease**：绑定到客户端会话的 key，会话心跳一停就自动删除——把存活性和数据绑在一起。
- **Watch**：订阅一个 key，变更时收到通知——无需轮询。
- **序列号**：每次创建获得单调递增的 id（可用作 fencing token）。

配方：*leader 选举* = 所有竞争者尝试创建同一个 ephemeral key；成功者当 leader，它的会话一死 key 即被删除，watch 者再次竞争。*锁* = 同上，再加 sequential 节点让等待者公平排队。*成员管理* = 每个存活节点一个 ephemeral key；watch 者能看到加入/离开。

为什么外包：你通过一个*键值 API* 获得共识级别的安全性，自己的服务群则保持近乎无状态——几台 ZK/etcd 节点就能协调成千上万个从不自己跑共识的客户端。
