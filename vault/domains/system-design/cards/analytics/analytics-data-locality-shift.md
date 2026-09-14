---
id: analytics-data-locality-shift
node: analytics.batch
type: qa
---
## Q
MapReduce's scheduler fought to place each task on the machine that already held its input block ("move computation to the data"); modern cloud batch stacks happily read everything from S3 over the network. What made data locality worth so much then, and what changed?

## A
Then: clusters ran on **spinning disks behind ~1 Gbps links**, so reading a block over the network was dramatically slower than reading it locally, and cross-rack bandwidth was scarce and shared. Co-locating compute with storage (HDFS datanodes = worker nodes) turned a network-bound job into a disk-bound one — locality was a first-class scheduling objective.

What changed:
- **Networks caught up**: tens-of-Gbps NICs and full-bisection datacenter fabrics made remote reads nearly as fast as local disk — the gap locality exploited collapsed.
- **Elasticity pays more than locality**: with storage disaggregated (S3/GCS), compute can scale to zero, burst for one job, or be preempted — impossible when every node is also a shard of the dataset that must stay up.
- Coupled clusters forced **scaling compute and storage together** and made maintenance (rebalancing on every node change) expensive; object storage is cheaper per TB and independently durable.

Residue: locality survives at a smaller scale — caching hot columns on local NVMe (warehouse caches, Alluxio) — but as an optimization, no longer an architecture.

## Q zh
MapReduce 的调度器竭力把每个任务放到已持有其输入块的机器上（"把计算搬到数据旁边"）；现代云上批处理栈却心安理得地全部通过网络读 S3。当年数据本地性（data locality）为什么那么值钱？后来什么变了？

## A zh
当年：集群跑在 **~1 Gbps 链路后面的机械磁盘**上，跨网络读一个块比本地读慢得多，跨机架带宽稀缺且共享。让计算和存储同机（HDFS datanode = worker 节点）能把网络瓶颈的作业变成磁盘瓶颈的作业——本地性因此是一等的调度目标。

变化在于：
- **网络追上来了**：几十 Gbps 的网卡和全等分带宽（full-bisection）的数据中心网络，让远程读几乎和本地磁盘一样快——本地性所利用的那个差距塌掉了。
- **弹性比本地性更值钱**：存储分离（S3/GCS）之后，计算可以缩到零、为单个作业突发扩容、甚至被抢占——而当每个节点同时是数据集的一个分片、必须常年在线时，这些都不可能。
- 耦合式集群迫使**计算和存储同步扩容**，维护也贵（每次节点变动都要 rebalance）；对象存储每 TB 更便宜，且持久性独立有保障。

残余：本地性在更小的尺度上仍然存在——把热列缓存到本地 NVMe（仓库缓存、Alluxio）——但只是一种优化，不再是一种架构。
