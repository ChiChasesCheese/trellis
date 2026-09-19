---
id: kafka-internals-partition-allocation-goals
node: internals.storage-segments
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka 在创建一个新主题时，要把它的所有分区副本分配到集群里的各个 broker 上。这个分配过程要同时满足哪几个目标？

## A
三个目标：1）**broker 间副本数量均衡**——比如 6 个 broker、10 个分区、复制系数（replication factor）3，一共 30 个副本，理想情况下每个 broker 分到 5 个；2）**同一分区的多个副本不能落在同一个 broker 上**——否则那个 broker 一旦下线，这个分区就同时丢了首领和某个跟随者，起不到容错作用；3）**如果配置了机架信息（rack.id），同一分区的副本要尽量分散到不同机架**——这样一个机架整体离线也不会导致某个分区完全不可用。这三条共同保证了单个 broker 或单个机架故障时，数据和可用性不会集中受损。
