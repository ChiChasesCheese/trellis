---
id: distributed-fixed-partition-count
node: distributed.partitioning.rebalancing
type: cloze
---
The fixed-partition trick: create far more logical partitions than nodes up front (say 1024 partitions on 10 nodes) and rebalance by {{c1::reassigning whole partitions to different nodes — the key-to-partition function never changes, only the partition-to-node map}}. Adding a node then means {{c2::stealing a few partitions from every existing node, and only the partitions being moved are in flight; reads/writes keep going against the old owner until the handover completes}}. The permanent cost is that the partition count is effectively {{c3::fixed for the life of the dataset, so it caps the maximum number of nodes (one partition per node) and sets a floor on per-partition overhead (memory, files, repair units) when the cluster is small}}. Elasticsearch's per-index shard count and Kafka's per-topic partition count are the same design — which is why {{c4::increasing partitions later requires a reindex/split, and for Kafka breaks key-to-partition ordering for existing keys}}.

## zh
固定分区数这一招：一开始就建出远多于节点数的逻辑 partition（比如 10 个节点上开 1024 个 partition），rebalance 时{{c1::把整个 partition 原样重新分配到别的节点——key 到 partition 的映射函数从不改变，变的只是 partition 到节点的映射表}}。于是加一个节点就意味着{{c2::从每个已有节点各偷走几个 partition，而且只有正在搬迁的那几个 partition 处于迁移中；在交接完成之前，读写照旧打到原来的 owner}}。永久性的代价是 partition 数实际上{{c3::在数据集的整个生命周期里都是固定的，因此它给节点数封了顶（最多一个节点一个 partition），也在集群规模还小的时候给每个 partition 的固定开销（内存、文件、修复单元）设了下限}}。Elasticsearch 每个 index 的 shard 数、Kafka 每个 topic 的 partition 数都是同一个设计——这也正是为什么{{c4::事后想加 partition 就得 reindex/split，在 Kafka 里还会打破已有 key 的 key-to-partition 顺序}}。
