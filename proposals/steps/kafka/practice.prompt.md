You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "practice.sizing-tuning": ["<id shown first>", "…"],
  "practice.cloud-deployment": ["<id shown first>", "…"],
  "practice.other-clients": ["<id shown first>", "…"],
  …
}

## practice.sizing-tuning — 容量规划与生产环境调优
掌握磁盘吞吐/容量、内存、网络、CPU等硬件选型依据，以及操作系统调优与GC选择对生产环境稳定性的影响。
- `kafka-practice-g1gc-small-heap-tuning` Q: Kafka broker 通常只需要几 GB 的堆内存（大部分系统内存要留给页面缓存），在这种「堆内存不大、垃圾回收效率本身就比较高」的前提下，为什么建议把 G1GC 的 `MaxGCPauseMillis`（目标停顿时间，默认200毫秒）和 `InitiatingHeapOccupancyPercent`（触发新一轮回收的堆占用率阈值，默认45%）都调得比默认值更小？
  A: G1GC 会根据配置的目标停顿时间和堆占用率阈值自动决定每一轮垃圾回收的频率和范围；Kafka 使用堆内存的方式清晰、待回收的垃圾对象处理效率本身就比较高，不需要等默认阈值触发再进行大规模回收。把 `InitiatingHeapOccupancyPercent` 调低（比如从45调到35），意味着堆内存使用率更低的时候
- `kafka-practice-network-10gbe-fanout` Q: 为什么给 Kafka broker 配网卡时建议至少用 10 GbE（万兆网卡），而不是老式的 1 GbE 网卡？这和 Kafka 支持多消费者这个特点有什么关系？
  A: 网络吞吐量和磁盘存储是制约 Kafka 集群整体伸缩能力的两个主要因素。因为 Kafka 支持同一份数据被多个独立的消费者客户端各自完整读取一遍，流出（读取）方向的网络流量往往是流入（写入）方向的好几倍——比如一个生产者每秒写入 1 MB 数据，如果同时有多个消费者在读，加上集群复制和跨集群镜像本身也要占用带宽，流出带
- `kafka-practice-rack-awareness-new-partitions-only` Q: 给 broker 配置 `broker.rack` 参数启用「机架感知」（rack awareness）后，Kafka 会确保新分区的各个副本不会全部落在同一个机架上。但如果之后又对已有分区做了分区重分配（partition reassignment），机架感知的保证还能持续维持吗？
  A: 不能自动维持。`broker.rack` 只影响**新创建**的分区在分配副本时的机架分布，Kafka 集群本身不会持续监控现有分区是否仍然满足机架感知（比如某次分区重分配之后，副本可能被意外集中到了同一个机架），也不会自动纠正这种情况。因此要长期维持机架感知带来的容灾效果（避免整个机架断电或故障时一个分区的全部副本同
- `kafka-practice-shared-zookeeper-multi-cluster-ok-other-apps-not` Q: 多个 Kafka 集群共用同一个 ZooKeeper 群组（各自用不同的 chroot 路径隔离元数据）通常是可以接受的做法，但为什么不建议再把这同一个 ZooKeeper 群组共享给其他非 Kafka 应用程序使用？
  A: Kafka 只在 broker、主题、分区或消费者群组这类元数据发生变化时才会写 ZooKeeper，正常情况下这部分流量很小，所以多个 Kafka 集群共用一个 ZooKeeper 群组通常不会造成明显压力。但 Kafka 对 ZooKeeper 的延迟和连接中断非常敏感：一旦与 ZooKeeper 群组的通信出现中
- `kafka-practice-ssd-vs-hdd-choice` Q: 给 Kafka broker 选磁盘时，什么场景下机械硬盘（HDD）是更合适的选择，什么场景下应该选固态硬盘（SSD）？
  A: 机械硬盘查找和随机访问速度慢，但单块容量大、价格便宜，适合「存储量很大、但不经常被频繁访问」的集群，比如长期保留大量历史数据、访问频率较低的场景，还可以用多块机械硬盘做多数据目录或磁盘阵列来弥补单盘吞吐的不足。固态硬盘查找和访问速度都快得多，能提供更好的性能，适合「有大量客户端并发连接、需要频繁读写」的场景——因为生产
- `kafka-practice-vm-swappiness-one-not-zero` Q: 配置 Kafka 所在 Linux 主机的内存交换行为时，为什么推荐把内核参数 `vm.swappiness` 设置为 1，而不是像早期建议的那样设置为 0？
  A: Kafka 大量依赖操作系统的页面缓存（page cache）来加速消费者读取——如果虚拟内存被交换到磁盘，就意味着已经没有足够内存留给页面缓存使用，会明显拖累 Kafka 各方面的性能，所以要尽量避免内存交换。`vm.swappiness` 早期在 Linux 内核 3.5 之前，数值 0 的含义是「除非发生内存溢出

## practice.cloud-deployment — 在云端运行Kafka
理解在主流云平台上部署和运行Kafka时需要额外考虑的因素。
- `kafka-practice-aws-i2-d2-tradeoff` Q: 如果一个 Kafka 集群在 AWS 上既需要保留大量历史数据，又需要很高的磁盘吞吐量，m4（网络存储、容量大但吞吐一般）和 r3（本地 SSD、吞吐高但容量有限）都无法同时满足，这时候可以考虑什么实例类型？代价是什么？
  A: 可以考虑 i2 或 d2 这类同时配备了大容量本地存储和较高吞吐能力的实例类型，它们能在数据量和吞吐量两方面都提供比 m4、r3 更好的表现。代价是这类实例的价格要比 m4、r3 贵很多，所以只有在业务确实同时对「保留大量数据」和「高吞吐量」都有硬性要求、且预算能够承受时，才值得选择这类更贵的实例类型。
- `kafka-practice-aws-m4-vs-r3-instance` Q: 在 AWS 上部署 Kafka broker 时，m4 实例和 r3 实例是两种常见选择，它们在存储方式和适用场景上有什么本质区别？
  A: m4 实例基于弹性块存储（EBS，一种独立于计算实例的网络挂载存储），可以保留更多、更长时间的数据，但磁盘吞吐量相对较低，因为读写都要经过网络访问远端存储。r3 实例配备了本地固态硬盘，直接挂载在计算实例上，吞吐量高得多，但受限于本地磁盘的物理容量，能保留的数据量有限。所以，如果业务更看重能长期保留大量数据、对吞吐量要
- `kafka-practice-azure-disk-tier-sla` Q: 在 Azure 上为 Kafka broker 选托管磁盘时，托管机械磁盘、高级固态硬盘（Premium SSD）、超级固态硬盘（Ultra SSD）这几档存储在价格、性能和可用性保证（SLA）上有什么区别？
  A: 托管机械磁盘价格相对便宜，但微软没有为它提供明确的可用性 SLA（服务级别协议）承诺；高级固态硬盘或超级固态硬盘价格更贵，但读写速度快得多，而且微软为它们提供了99.99%的可用性 SLA。因此，如果业务要求非常低的延迟或需要明确的可用性保证，应该选择高级/超级固态硬盘；如果对延迟不敏感、更看重成本，托管机械磁盘或者甚
- `kafka-practice-azure-managed-vs-ephemeral-disk` Q: 在 Azure 上自己搭建 Kafka 集群时，为什么强烈建议给 broker 使用 Azure 托管磁盘（managed disk），而不是虚拟机自带的临时磁盘（ephemeral disk）？
  A: Azure 里虚拟机和磁盘是分开管理的，临时磁盘的生命周期和这台虚拟机实例绑定在一起——一旦这台虚拟机因为底层维护、故障迁移等原因被移动到另一台物理主机，挂载在原实例上的临时磁盘数据就会丢失，这意味着这个 broker 保存的所有消息数据都可能凭空消失。使用 Azure 托管磁盘则可以独立于具体虚拟机实例持久化保存，即
- `kafka-practice-managed-kafka-integration-depth` Q: 选择托管 Kafka 平台时，Amazon MSK、Azure HDInsight 这类「只托管核心 Kafka 集群」的平台，和 Confluent Cloud 这类「整合了模式注册表、REST 代理、客户端库等一整套周边组件」的平台，在使用体验上有什么本质区别？该怎么根据这个区别做选型？
  A: Amazon MSK 和 Azure HDInsight 只负责托管 Kafka 集群本身，模式注册表、REST 代理等周边组件需要用户自己搭建或依赖社区工具（比如 MSK 建议用户自行采用 Cruise Control、Burrow 等社区工具，但平台本身不提供支持服务），集成度较低，但换来的是更贴近原生 Kafka

## practice.other-clients — 非JVM语言客户端生态
了解除Java官方客户端外，其他语言客户端库的生态与选型考量。
- `kafka-practice-go-two-client-options` Q: 在 Go 语言生态里，接入 Kafka 至少有两种不同性质的客户端库可选：一种是 Confluent 支持、基于 librdkafka 封装的 Go 客户端，另一种是 Sarama（Shopify 开发、MIT 许可）。这两者在实现方式上有什么本质区别？
  A: 基于 librdkafka 封装的 Go 客户端底层调用的是 C 语言实现的 librdkafka 库，Go 代码只是一层绑定，运行时依赖这个 C 库；Sarama 则是完全用 Go 语言原生实现的 Kafka 客户端，不依赖任何外部 C 库，从协议层到应用层都是纯 Go 代码，并采用 MIT 许可发布。两者代表了「复
- `kafka-practice-librdkafka-reused-by-other-langs` Q: librdkafka 是用 C 语言实现的 Kafka 客户端库，被认为是性能最好的 Kafka 客户端实现之一。为什么 Confluent 支持的 Go 语言、Python 和 .Net 客户端都选择基于它做封装，而不是各自用原生语言重新实现一遍 Kafka 协议？
  A: librdkafka 已经用 C 语言把 Kafka 客户端协议实现到了很高的性能水平，其他语言想要达到同等的性能和协议正确性，与其在自己的语言里从零重新实现一遍完整的 Kafka 客户端协议（工作量大、还要独自跟进协议演进和修复各类边界问题），不如直接给这个已经过验证、性能优异的 C 库套一层本语言的绑定（bindi
- `kafka-practice-python-two-client-options` Q: 在 Python 生态里，同样存在两种不同性质的 Kafka 客户端：Confluent 支持、基于 librdkafka 封装的 Python 客户端，和 kafka-python（原生 Python 实现，Apache 2.0 许可）。这组对比和 Go 生态里 librdkafka 封装客户端与 Sarama 的对比是同一种模式吗？
  A: 是同一种模式：基于 librdkafka 的 Python 客户端本质上是给 C 语言实现的 librdkafka 库套一层 Python 绑定，运行时依赖这个底层 C 库；kafka-python 则是完全用 Python 原生实现的 Kafka 客户端，不依赖 librdkafka，采用 Apache 2.0 许可
- `kafka-practice-rest-proxy-language-agnostic-alt` Q: 除了为某种编程语言选择一个原生的 Kafka 客户端库（或封装 librdkafka 的绑定），还有什么方式可以让缺乏成熟原生客户端支持的语言或环境接入 Kafka？这种方式的好处是什么？
  A: 可以使用 REST 代理（REST proxy，比如 Confluent、Strimzi 或 Karapace 提供的实现），它把 Kafka 的生产和消费能力通过标准的 HTTP 接口暴露出来。这样一来，任何能发送 HTTP 请求的编程语言或工具都可以接入 Kafka，不需要这个语言生态里存在专门维护的原生 Kafk

## practice.kubernetes-strimzi — 在Kubernetes上运行Kafka（Strimzi）
理解Strimzi等Kubernetes Operator如何把Kafka集群的部署、扩缩容与升级声明式地管理起来。
- `kafka-practice-akhq-vs-conduktor-oss-vs-proprietary` Q: AKHQ 和 Conduktor 都是用来查看和操作 Kafka 集群的图形化工具，但在开源属性和支持范围上有明显差异，分别是什么？
  A: AKHQ 是一个开源的 GUI 工具，支持配置管理（包括用户和 ACL 配置），也能对接模式注册表、Kafka Connect 等组件，并提供数据操作能力，可以作为 Kafka 命令行工具的图形化替代品。Conduktor 则不是开源的桌面工具，但同样流行，它支持多个不同的托管平台（包括 Confluent、Aiven
- `kafka-practice-cruise-control-scale-purpose` Q: Cruise Control 最初是为了解决什么问题而设计的？除了这个最初目标，它后来还扩展支持了哪些运维能力？对多大规模的集群来说，使用它几乎是必需的？
  A: Cruise Control 最初是一种自动化的集群数据再均衡（rebalance，把数据/分区在 broker 之间重新分布得更均匀）解决方案，用来解决大规模集群里手动检查指标、手动做分区重分配这种运维方式难以为继的问题。在此基础上，它后来又扩展支持了异常检测和操作管理能力，比如自动化地添加和移除 broker。对于
- `kafka-practice-julieops-gitops-vs-akhq-gui` Q: JulieOps（之前叫 Kafka 拓扑构建器）和 AKHQ 都可以用来管理 Kafka 的主题和 ACL，但它们背后的管理模型完全不同，分别是什么？
  A: JulieOps 基于 GitOps 模型工作：把主题、模式、ACL 等配置以声明式的方式写在代码/配置文件里（类似「期望状态即代码」），交由 JulieOps 对比当前实际状态和期望状态、自动完成变更，所有配置变更都能像代码一样被版本控制、评审和追溯。AKHQ 则是一个图形界面（GUI）管理和交互工具，管理员通过界面
- `kafka-practice-strimzi-bridge-no-schema-registry` Q: Strimzi 提供的 Strimzi Kafka Bridge 是什么类型的组件？为什么它目前还不支持模式注册表（schema registry，用于管理和校验消息格式模式的组件）这项能力？
  A: Strimzi Kafka Bridge 是一个基于 Apache 2.0 许可发布的 REST 代理（REST proxy）实现，它把 Kafka 的生产和消费能力通过 HTTP 接口暴露出来，方便那些不方便直接使用原生 Kafka 客户端协议的场景接入。目前它还不支持模式注册表功能，原因是出于许可方面的考虑——常见
- `kafka-practice-strimzi-operator-not-managed-service` Q: 在 Kubernetes 上想要运行自己的 Kafka 集群（而不是用某个云厂商的全托管 Kafka 服务）时，Strimzi 扮演的是什么角色？它和一个「全托管 Kafka 平台」的根本区别是什么？
  A: Strimzi 提供的是一个 Kubernetes Operator（一种通过声明式的 Kubernetes 自定义资源来自动化管理某个应用生命周期的模式）：用户只需要用 Kubernetes 资源描述期望的 Kafka 集群状态（比如多少个 broker、用什么配置），Strimzi 就会在公有云或私有云的 Kube
