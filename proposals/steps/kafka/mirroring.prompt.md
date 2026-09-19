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
  "mirroring.architectures": ["<id shown first>", "…"],
  "mirroring.mirrormaker": ["<id shown first>", "…"],
  "mirroring.alternatives": ["<id shown first>", "…"]
}

## mirroring.architectures — 跨集群镜像的应用场景与多集群架构
理解跨数据中心复制的现实约束，以及星型、双活、主备、延展集群等多集群架构模式各自的适用场景。
- `kafka-mirroring-active-active-avoid-cyclic-mirror` Q: 在双活架构里，如果两个数据中心互相把对方的数据镜像过来，怎么防止同一个逻辑主题的数据被无休止地来回镜像（比如数据中心 A 把数据镜像给 B，B 又把这份数据镜像回 A，如此循环）？
  A: 常见做法是给每个数据中心的主题加上代表这个数据中心的命名空间前缀，为同一个「逻辑主题」在每个数据中心分别建一个带前缀的实际主题，比如逻辑主题 `users` 在旧金山数据中心叫 `SF.users`，在纽约数据中心叫 `NYC.users`。镜像进程只把 `SF.users`（本地产生的数据）单向镜像到 NYC，把 `
- `kafka-mirroring-active-active-conflict-challenge` Q: 双活架构（active-active，多个数据中心互相镜像、都能同时生产和消费数据）相比星型架构最大的性能和可用性优势是什么？它带来的最大挑战又是什么，有什么典型的化解思路？
  A: 优势：每个数据中心都具备完整功能，可以就近为用户提供服务、降低延迟，而且某个数据中心故障时只需把用户的网络流量重定向到另一个数据中心即可完成故障转移，简单透明，不像星型架构那样会因为数据只存在于某一个区域集群而出现「访问不到数据」的问题。最大挑战是**多数据中心异步读写之间的一致性冲突**：比如用户写入一个数据中心的数
- `kafka-mirroring-active-standby-tradeoff` Q: 主备架构（active-standby，用一个镜像进程把主集群数据完整复制到一个平时基本不用的备用集群）相比双活架构简单很多，不用处理访问路由和冲突问题。它的代价是什么？故障转移能不能保证零数据丢失、零重复？
  A: 最大代价是「浪费」——备用集群在绝大多数时间里什么正经工作都不做，只是等灾难发生时顶上，硬件和运维成本没有被充分利用（有些组织会让备用集群规模更小以节省成本，或者顺带承担一些只读工作负载，相当于退化成简化版的星型架构）。而且即使配置了主备架构，也无法做到完全不丢数据、也不出现重复数据的故障转移：因为镜像通常是异步的，备
- `kafka-mirroring-cross-dc-realities-principles` Q: 跨数据中心的网络通常具有高延迟、带宽有限、成本高这三个现实约束，Kafka 的默认超时和缓冲区配置又是按单数据中心内部低延迟高带宽的场景调优的。基于这些约束，设计多数据中心 Kafka 架构时应该遵循哪几条原则？
  A: 三条原则：1）每个数据中心至少要有自己的一个 Kafka 集群，而不是让一个集群跨广域网横跨多个数据中心（那样会撞上上面这些默认配置假设）；2）两个数据中心之间对同一个事件的复制要做到只发生一次（出错重试除外），避免同一条数据被重复搬运浪费带宽；3）如果确实需要跨数据中心传输数据，优先选择「从远程数据中心读取数据」而不
- `kafka-mirroring-star-architecture-limitation` Q: 星型架构（也叫 hub-and-spoke，多个区域集群单向镜像到一个中心集群）适合什么场景？它最大的局限是什么？用一个跨城市银行业务的例子说明这个局限会造成什么后果。
  A: 适合两种情况：需要访问全部数据的消费者集中部署在中心集群，或者每个数据中心的应用只需要访问本地数据。它的最大局限是**区域数据中心之间彼此完全隔离**——数据只会从区域集群单向镜像到中心集群，区域集群之间互相看不到对方的数据。比如一家银行在每个城市有独立的区域集群保存本市用户的账户数据，如果某用户到另一个城市的分行办理
- `kafka-mirroring-stretch-cluster-quorum` Q: 延展集群（stretch cluster，一个 Kafka 集群本身跨多个数据中心部署，靠 Kafka 内置的同步复制机制保持副本一致，而不是靠镜像进程）为什么通常要求至少 3 个数据中心而不是 2 个？它能防住什么级别的故障，防不住什么？
  A: 延展集群依赖的协调服务（ZooKeeper）要求集群节点数是奇数，且必须有「多数节点」存活集群才可用；如果只用 2 个数据中心，其中必然有一个数据中心包含了多数节点，一旦这个数据中心整体故障，ZooKeeper 和 Kafka 就会跟着一起不可用，起不到容灾效果。用 3 个数据中心分配节点，可以做到任何单个数据中心都不

## mirroring.mirrormaker — MirrorMaker：配置、拓扑与调优
掌握基于Kafka Connect构建的MirrorMaker如何配置复制拓扑、保障自身安全并针对生产环境调优。
- `kafka-mirrormaker-custom-partition-assignment` Q: MirrorMaker（Kafka 官方跨集群镜像工具，基于 Connect 框架构建）在给各个任务分配要镜像的分区时，为什么不直接复用 Kafka 标准的消费者群组管理协议（多个消费者共享同一个 `group.id` 自动分摊分区）？它自己采用的分配方式带来了什么额外好处？
  A: 标准消费者群组协议每当有新主题、新分区加入，或者消费者数量变化时都会触发一次再均衡（rebalance），再均衡期间所有消费者都要暂停处理、重新分配分区，这在跨数据中心镜像这种需要持续、稳定吞吐的场景里会造成延迟激增。为避免这个问题，MirrorMaker 没有用这套协议，而是让源集群每个分区的事件都固定镜像到目标集群
- `kafka-mirrormaker-deploy-near-target-remote-consume` Q: 把 NYC 数据中心的数据镜像到 SF 数据中心时，一般建议把 MirrorMaker 部署在 SF（目标端），让它跨广域网**远程消费** NYC 的数据、再**就近生产**到本地的 SF 集群，而不是反过来部署在 NYC 本地消费、再远程生产到 SF。这个选择背后的核心理由是什么？
  A: 跨数据中心的广域网连接远比数据中心内部网络更容易发生分区（断连）。如果 MirrorMaker 部署在目标端做远程消费，一旦跨数据中心网络中断，最坏情况只是消费者暂时读不到数据——数据依然安全地留在源集群里，网络恢复后照样能补读，不会丢。但如果反过来部署在源端本地消费、再远程生产到目标集群，一旦发生同样的网络中断，Mi
- `kafka-mirrormaker-offset-migration-safety` Q: MirrorMaker 支持自动把消费偏移量从源集群迁移到目标集群，让消费者切换到灾备集群后能从之前的位置继续处理数据。这个迁移机制在什么情况下会主动放弃覆盖目标集群里的偏移量，为什么要这样设计？
  A: 如果目标集群里某个消费者群组已经在正常使用（也就是说，这个消费者群组已经在目标集群里独立消费并提交自己的偏移量），MirrorMaker 就不会用迁移过来的偏移量去覆盖它。这是为了避免意外冲突：如果目标集群的消费者群组本来就在按自己的节奏读取数据，MirrorMaker 强行覆盖它的偏移量会打乱这个消费者群组本来的消费
- `kafka-mirrormaker-replication-lag-two-imperfect-methods` Q: 想知道 MirrorMaker 镜像的目标集群到底落后源集群多少，有两种基于偏移量差值的监控方式，但它们各自都不够精确。这两种方式分别是什么，各自的误差来源是什么？
  A: 第一种是检查 MirrorMaker **已经提交**到源集群的最新偏移量，与源分区最后一条消息的偏移量做差值——但 MirrorMaker 默认每分钟才提交一次偏移量，所以在这一分钟窗口内看到的延迟数字会先偏大、提交后又突然下降，并不反映真实的实时延迟。第二种是直接读取 MirrorMaker 内部消费者**已经读取
- `kafka-mirrormaker-tasks-max-tuning-approach` Q: 调优 MirrorMaker 单实例吞吐量时，为什么建议对 `tasks.max`（连接器可用的最大任务数）做一次「逐档递增」的压测（比如依次设成 1、2、4、8、16、24、32），而不是直接设一个很大的数值？
  A: 任务数越多、并行度越高，理论上吞吐量应该越大，但受限于硬件、网络带宽以及压缩/解压带来的 CPU 消耗，超过某个任务数之后性能反而会开始下降（而不是持续线性提升）——具体这个「拐点」在哪，完全取决于所用的硬件、数据中心或云服务商环境，无法凭经验直接给出一个通用数字。逐档递增压测（用性能压测工具在源集群制造负载、观察 M
- `kafka-mirrormaker-topic-write-acl-not-migrated` Q: MirrorMaker 会把源主题的配置信息和访问控制列表（ACL）一并迁移到目标主题，但源主题上关于「谁能写入这个主题」的 `Topic:Write` 权限，默认却不会被迁移到目标集群。这样设计的用意是什么？
  A: 如果把源主题原有的 `Topic:Write` 权限原样复制到目标集群，那么原本只能写源主题的那些生产者，理论上也会被允许直接写入目标主题（灾备/镜像集群），这就破坏了「目标集群上的数据只应该来自镜像流程本身」这个前提——万一有生产者绕过源集群直接写到目标主题，会造成目标集群数据与源集群不一致，且这类写入根本不会被再镜

## mirroring.alternatives — 其他跨集群镜像方案
了解uReplicator、Brooklin等替代方案相对MirrorMaker的定位与取舍。
- `kafka-mirroring-alt-brooklin-general-purpose` Q: Brooklin（LinkedIn 开发的镜像方案）和 MirrorMaker、uReplicator 有一个定位上的本质区别：它并不是一个专门为 Kafka 打造的镜像工具。它真正的定位是什么？这个定位让它除了跨集群镜像之外还能做哪些事情？
  A: Brooklin 是一个通用的**分布式数据摄取（data ingestion）服务**，设计目标是在各种异构的数据源和目标系统之间搬运数据，Kafka 只是它支持的众多场景之一。基于这个通用定位，Brooklin 除了可以作为「Kafka 跨集群镜像方案」使用之外，还能充当「数据桥」把不同数据源的数据接入流式处理系统
- `kafka-mirroring-alt-cluster-linking-no-connect` Q: 集群链接（cluster linking，Confluent Server 提供的跨集群复制特性）和 MirrorMaker 这类基于 Connect 的外部镜像工具相比，在实现方式和运维复杂度上有什么本质区别，带来了什么运维和性能上的好处？
  A: 集群链接不依赖任何外部组件（不需要单独搭建和运维 Connect 集群），而是直接扩展了 Kafka 集群内部原生的 broker 间复制协议，把这套本来只在同一个集群内部用于副本同步的协议直接用在跨集群复制上：目标集群的首领 broker 直接向源集群对应的首领拉取分区数据，目标集群的跟随者再用标准的集群内复制机制从
- `kafka-mirroring-alt-cluster-linking-no-sync-manual-failover` Q: 集群链接（cluster linking）虽然运维简单、效率高，但和多区域集群（MRC）比起来缺少哪个关键特性？这对客户端故障转移意味着什么？
  A: 集群链接**没有同步复制选项**，它做的是异步的跨集群复制，不像 MRC 那样可以选择让部分复制走同步路径来换取「发生故障时数据绝对不丢」的强保证。这也意味着集群链接不能像 MRC/延展集群那样提供「客户端无感知的透明故障转移」——当源集群发生故障需要切换到目标集群时，客户端应用需要手动重启才能连接到新的集群，不会自动
- `kafka-mirroring-alt-mrc-observer-auto-promote` Q: 多区域集群（MRC，multi-region cluster，Confluent Server 提供的一种延展集群变体）里的「观察者（observer）」副本是什么？为什么正常情况下它不会拖慢生产者，却又能在某个区域故障时自动帮上忙？
  A: 观察者是一种**不属于 ISR（in-sync replicas，同步副本集合）的异步副本**：它持续从首领异步复制数据，但即使生产者配置了 `acks=all`，broker 也不会等观察者确认，所以观察者的存在不会给生产者的写入延迟增加负担；同时它又能正常把消息发送给消费者，起到分担读流量、跨区域容灾的作用。当某个
- `kafka-mirroring-alt-replicator-vs-mirrormaker-diffs` Q: Confluent Replicator 和 MirrorMaker 都基于 Connect 框架构建，功能上有几处明显差异：在 ACL（访问控制列表）迁移、跨语言客户端的偏移量迁移，以及「本地/远程主题」概念上，Replicator 分别是怎么处理的？
  A: 在 ACL 迁移上，Replicator 完全**不支持**迁移 ACL，这一点和支持迁移 ACL 的 MirrorMaker 不同。在偏移量迁移上，Replicator 只支持 **Java 客户端**（通过时间戳拦截器实现），覆盖面比 MirrorMaker 更窄。在主题命名模型上，Replicator **没有*
- `kafka-mirroring-alt-ureplicator-helix-controller` Q: uReplicator（Uber 开发的旧版 MirrorMaker 替代品）用什么机制取代了旧版 MirrorMaker 里「消费者群组自动再均衡」来分配分区，从而避免因为新增主题、重启实例等操作触发长时间停顿？这个方案带来了什么额外代价？
  A: uReplicator 引入 Apache Helix 作为一个高可用的**中心控制器**，专门负责维护需要镜像的主题列表，并把分区显式分配给各个 uReplicator 实例；管理员通过 REST API 增删主题，Helix 控制器计算好分配方案后推送给各实例，实例之间不需要像标准消费者群组那样互相协调、协商谁该消
