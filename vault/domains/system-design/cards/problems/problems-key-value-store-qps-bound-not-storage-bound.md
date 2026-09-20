---
id: problems-key-value-store-qps-bound-not-storage-bound
node: problems.foundations.key-value-store
type: qa
step: 1
tags: [grown]
---
## Q
In a Dynamo-style key-value store design sized for 555,556 peak client QPS and 3.6 TB of replicated data (N=3), why does the cluster end up sized at roughly 167 nodes driven by QPS rather than 7.2 nodes driven by storage capacity?

## A
Because a coordinator sends every read and write to all N=3 replicas in a key's preference list (not just one), the load each physical node absorbs is the client-facing QPS multiplied by the replication factor: 555,556 × 3 ≈ 1,666,667 node-level ops/sec. At an assumed 10,000 ops/sec per node, that needs ≈167 nodes — about 23× more than the ≈7.2 nodes a 500 GB/node capacity would need to just hold 3.6 TB of data. The design lever is therefore per-node operation throughput under replication fan-out, not raw byte count.

## Q zh
在一个为峰值 555,556 客户端 QPS、3.6TB 三副本（N=3）数据设计的 Dynamo 风格键值存储中，为什么集群规模最终由 QPS 决定为约 167 台节点，而不是由存储容量决定为约 7.2 台？

## A zh
因为协调节点会把每次读写都发给一个 key 偏好列表上的全部 N=3 个副本（而不是只发给一个），所以每台物理节点承受的负载是客户端 QPS 乘以复制因子：555,556 × 3 ≈ 1,666,667 次/秒的节点级操作。假设单节点能承受 10,000 次/秒，就需要约 167 台节点——比按 500GB/节点容量只需装下 3.6TB 数据所需的约 7.2 台节点多出约 23 倍。设计杠杆是复制扇出下的单节点操作吞吐，而不是原始字节数。
