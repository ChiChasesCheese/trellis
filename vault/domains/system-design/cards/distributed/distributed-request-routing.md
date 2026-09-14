---
id: distributed-request-routing
node: distributed.partitioning.rebalancing
type: qa
---
## Q
A client holds a key — how does the request find the right partition's node? Give the three routing approaches and where the partition map lives.

## A
- **Ask any node**: nodes share the map (gossip) and forward misdirected requests — no extra infra, one possible extra hop (Cassandra, Riak).
- **Routing tier**: a partition-aware proxy in front forwards requests (Mongo's `mongos`, Vitess's `vtgate`).
- **Partition-aware client**: the client library caches the map and connects directly — fewest hops, smartest clients (Kafka producers, Redis Cluster clients).

The map must be authoritative somewhere: either a **coordination service** (ZooKeeper/etcd — HBase, Kafka historically) that notifies routers on rebalancing, or **gossip + version numbers** so stale routers learn the truth from the nodes they hit. The failure mode to mention: routing on a stale map during a rebalance.

## Q zh
客户端手上有一个 key——这个请求是怎样找到正确的分片所在的节点的？给出三种路由方式，以及分区映射表存在哪里。

## A zh
- **问任意一个节点**：节点之间共享映射表（通过 gossip），把发错的请求转发出去——不需要额外基础设施，可能多付出一跳（Cassandra、Riak）。
- **路由层**：前面放一个感知分区的代理来转发请求（Mongo 的 `mongos`、Vitess 的 `vtgate`）。
- **感知分区的客户端**：客户端库自己缓存映射表并直接连接——跳数最少，客户端最"聪明"（Kafka 的 producer、Redis Cluster 的客户端）。

这份映射表必须在某处是权威的：要么是一个**协调服务**（ZooKeeper/etcd——历史上的 HBase、Kafka），在再平衡时通知各路由器；要么是**gossip + 版本号**，让过时的路由器从它们碰到的节点那里学到真相。值得一提的失败模式：在再平衡期间按一份过时的映射表路由。
