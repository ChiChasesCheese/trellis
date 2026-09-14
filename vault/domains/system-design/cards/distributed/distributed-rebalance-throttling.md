---
id: distributed-rebalance-throttling
node: distributed.partitioning.rebalancing
type: qa
---
## Q
Why is fully automatic, unthrottled rebalancing a well-known way to turn a small failure into an outage — and what are the standard guards?

## A
Rebalancing consumes exactly the resources you are short of: disk IO, network, and page cache, **at the moment the cluster is already degraded**. The cascade: a node is falsely declared dead (GC pause, slow disk) → the cluster starts re-replicating its data → the extra load slows *other* nodes past the failure detector's threshold → they're declared dead too → more rebalancing. This death spiral has taken down real clusters that never lost a machine.

Guards:

- **Rate limits**: cap stream throughput and concurrent recoveries (Cassandra `stream_throughput_outbound`, Elasticsearch `cluster.routing.allocation.node_concurrent_recoveries` and the recovery byte budget).
- **Delay before acting**: don't move data until the node has been gone for N minutes (Elasticsearch `index.unassigned.node_left.delayed_timeout`, default 1m) — most node absences are restarts.
- **Human in the loop**: automatic *proposal*, operator-approved *execution*, for the largest moves.

## Q zh
为什么完全自动、不加限流的再平衡是一种众所周知的、能把小故障变成大事故的方式？标准的防护手段有哪些？

## A zh
再平衡消耗的正好是你此刻最短缺的资源：磁盘 IO、网络、page cache，而且恰恰是在**集群已经处于降级状态的时刻**。级联过程是这样的：一个节点被误判为死亡（GC 暂停、磁盘变慢）→ 集群开始重新复制它的数据 → 额外的负载让*其他*节点也变慢，超过了故障检测器的阈值 → 它们也被判定为死亡 → 触发更多再平衡。这种死亡螺旋曾经拖垮过真实的、从未真正丢失过一台机器的集群。

防护手段：

- **限流**：限制流传输吞吐量和并发恢复数（Cassandra 的 `stream_throughput_outbound`，Elasticsearch 的 `cluster.routing.allocation.node_concurrent_recoveries` 以及恢复字节预算）。
- **动手前先延迟**：节点消失 N 分钟之前不要开始搬数据（Elasticsearch 的 `index.unassigned.node_left.delayed_timeout`，默认 1 分钟）——大多数节点消失只是重启。
- **人在回路中**：对于最大规模的搬迁，自动*提出方案*，由运维人员审批*执行*。
