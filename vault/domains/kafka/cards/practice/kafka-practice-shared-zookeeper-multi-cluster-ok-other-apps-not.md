---
id: kafka-practice-shared-zookeeper-multi-cluster-ok-other-apps-not
node: practice.sizing-tuning
type: qa
step: 4
source: kafka-2e
---
## Q
多个 Kafka 集群共用同一个 ZooKeeper 群组（各自用不同的 chroot 路径隔离元数据）通常是可以接受的做法，但为什么不建议再把这同一个 ZooKeeper 群组共享给其他非 Kafka 应用程序使用？

## A
Kafka 只在 broker、主题、分区或消费者群组这类元数据发生变化时才会写 ZooKeeper，正常情况下这部分流量很小，所以多个 Kafka 集群共用一个 ZooKeeper 群组通常不会造成明显压力。但 Kafka 对 ZooKeeper 的延迟和连接中断非常敏感：一旦与 ZooKeeper 群组的通信出现中断，多个 broker 可能会因此离线，导致它们负责的分区也跟着离线，还会给集群控制器（负责监督集群状态变更的特殊 broker 角色）带来额外压力。其他应用程序对 ZooKeeper 的使用方式和压力大小是不可控的，如果它们产生大量流量或做了不恰当的操作，就有可能拖慢或打断 ZooKeeper 群组的响应，进而间接引发 Kafka 集群出现难以预料的异常行为，所以更稳妥的做法是让其他应用程序使用自己独立的 ZooKeeper 群组。
