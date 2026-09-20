---
id: problems-message-queue-tiered-storage-10x-evolution
node: problems.foundations.message-queue
type: qa
step: 8
tags: [grown]
---
## Q
In a Kafka-class message queue where broker storage capacity (not write throughput) is the binding constraint on cluster size for a long-retention event topic, why does scaling DAU 10x (which grows 7-day-retention, 3x-replicated storage from 504TB to 5,040TB) eventually force a shift to tiered storage, and how does an architecture like Pulsar/BookKeeper avoid needing this shift?

## A
When each broker owns its partition replicas on local disk, growing storage 10x means adding either far more brokers or far bigger disks per broker, and the latter eventually hits the physical limit on disk slots per machine -- at that point the fix is tiered storage: splitting segments by age into a hot tier on local disk (serving page-cache reads and catch-up consumers) and a cold tier offloaded to object storage. Pulsar/BookKeeper architectures need this fix less urgently because they separate the serving layer (stateless brokers) from the storage layer (BookKeeper bookies) from the start: a ledger's entries are striped across an ensemble of bookies rather than fully replicated onto whichever broker happens to be the partition leader, so storage capacity scales independently of broker count by simply adding bookies.

## Q zh
在一个 Kafka 一类消息队列里，如果 broker 存储容量（而不是写入吞吐）是限制一个长保留期事件主题集群规模的约束，为什么 DAU 增长 10 倍（把 7 天保留、三副本的存储量从 504TB 推高到 5,040TB）最终会迫使系统转向分层存储（tiered storage）？Pulsar/BookKeeper 这类架构又是怎么从一开始就不那么急迫需要这个转变的？

## A zh
当每个 broker 在本地磁盘上直接拥有自己的分区副本时，存储量增长 10 倍意味着要么加更多 broker，要么给每台 broker 配更大的盘，而后者最终会撞上单机磁盘槽位数量的物理上限——到那时的解法是分层存储：按数据年龄把 segment 拆成本地磁盘上的「热」层（服务 page cache 读取和追赶中的消费者）和卸载到对象存储的「冷」层。Pulsar/BookKeeper 这类架构对这次转变没那么迫切，是因为它们从一开始就把服务层（无状态的 broker）和存储层（BookKeeper 的 bookie）分离开：一个 ledger 的条目是条带化分布存储在一组 bookie（ensemble）上的，而不是完整复制到恰好是分区 leader 的那台 broker 上，所以存储容量可以只靠增加 bookie 数量来独立扩展，不受 broker 数量的限制。
