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
  "core.pubsub-why": ["<id shown first>", "…"],
  "core.topics-partitions": ["<id shown first>", "…"],
  "core.offsets": ["<id shown first>", "…"],
  …
}

## core.pubsub-why — 发布/订阅模型与Kafka的定位（为何选择Kafka）
理解发布订阅消息系统与传统消息队列的区别，以及Kafka凭借基于磁盘的持久化、伸缩性和高吞吐成为首选的原因。
- `kafka-core-consumer-group-shared-once` Q: 消费者群组（consumer group，共享同一消息流的一组消费者）读取一个主题时，Kafka 如何在群组内部实现「整个群组只处理一次给定消息」，同时又允许不同群组的消费者各自看到全部消息？
  A: 这取决于消费者是否属于同一个群组：同一群组内的消费者共享该主题的分区，Kafka 保证每个分区只被群组内的一个消费者读取，因此群组整体上对每条消息只处理一次；而分属不同群组（或不使用群组）的消费者各自独立读取整条消息流，彼此不影响。这样 Kafka 既能像传统队列一样把任务分摊给多个 worker，又能像广播一样让多个
- `kafka-core-consumer-independence-vs-traditional-queue` Q: 在传统消息队列系统中，一条消息一旦被某个客户端读取，其他客户端就再也读不到它了。Kafka 的多消费者模型与此有何不同？
  A: Kafka 允许多个消费者（consumer）各自独立地从同一个消息流读取数据，彼此互不影响：某个消费者读取了一条消息，并不会让这条消息对其他消费者「消失」。这与传统队列里消息一旦被拿走即失效、只能被一个客户端消费的语义不同，任何订阅了该主题的消费者都能各自按自己的进度读取到全部消息。
- `kafka-core-disk-retention-benefit` Q: 一个消费者应用需要停机维护几个小时，或者曾因流量突增而处理跟不上进度。Kafka 的哪个特性保证它重启后不会丢失这段时间产生的消息？
  A: Kafka 把消息提交到磁盘，并按每个主题设置的保留策略（retention policy）持久化保存一段时间，而不是像很多消息队列那样消息一旦被读取或超时就立刻丢弃。这意味着消费者可以离线、变慢甚至被重启，只要消息还在保留期内，就能从上次中断的位置继续读取，不会因消费者一侧的问题而丢失数据或反过来堵塞生产者。
- `kafka-core-multi-producer-unified-topic` Q: 一个网站由多个微服务组成，每个微服务都会产生「页面访问」事件。如果都写入 Kafka 的同一个主题（topic，消息的分类单位），消费者端会遇到格式混乱的问题吗？Kafka 的多生产者支持是如何避免这一点的？
  A: 只要各个微服务约定用同一种消息格式写入同一个主题，消费者读到的就是格式统一的页面访问事件流。这是因为 Kafka 原生支持多个生产者（producer）同时、独立地向同一个主题写入数据，消费者不需要协调或区分数据来自哪个生产者，就能获得统一格式的数据，不必为不同格式各写一套适配逻辑。
- `kafka-core-pubsub-vs-pointtopoint` Q: 一个数据发布者最初直接连接单个接收者传输监控指标；随着接收系统越来越多，点对点连接开始变得难以维护。发布与订阅系统（pub/sub messaging system）用什么方式解决了这个问题？
  A: pub/sub 系统在发布者和接收者之间加入一个独立的中间层，通常称为 broker（消息中转服务器）。发布者（publisher）不再直接把消息发给某个具体接收者，而是把消息发给 broker；订阅者（subscriber）按需向 broker 订阅特定类型的消息。这样发布者和订阅者互不感知对方的存在（解耦），新增一
- `kafka-core-scalability-no-downtime` Q: 为什么说 Kafka 从一开始就被设计成「可以从单个 broker 平滑扩展到上百个 broker 的集群」？这种扩容会影响正在运行的集群吗？
  A: Kafka 的伸缩性（scalability）体现在：开发阶段可以只用单个 broker（一台 Kafka 服务器），随着数据量增长逐步扩展到包含上百个 broker 的生产集群，扩容过程不影响整体可用性——即使集群中个别 broker 失效，其余 broker（在配置了足够复制系数的前提下）仍能继续为客户端提供服务。

## core.topics-partitions — 主题（topic）、分区（partition）与数据模型
掌握主题如何被划分为分区以获得并行度和顺序保证，以及消息、批次、模式（schema）在其中的角色。
- `kafka-core-batch-latency-throughput-tradeoff` Q: Kafka 把同一主题、同一分区的多条消息打包成一个批次（batch）再发送，而不是逐条发送。这样做要在什么和什么之间做权衡？
  A: 要在延迟和吞吐量之间权衡：批次越大，单位时间内能处理的消息数量（吞吐量）越高，因为减少了每条消息单独走一次网络的开销；但单条消息要等凑够一批才被发出，导致这条消息自身的传输延迟变长。此外批次通常会被压缩以提升传输和存储效率，但压缩本身又需要额外的计算开销。
- `kafka-core-message-key-partition-routing` Q: 生产者发送消息时可以附带一个可选的键（key，也是字节数组）。键有什么作用？两条键相同的消息一定会被分到同一个分区吗？
  A: 键本身对 Kafka 没有特殊含义，但可以用来控制消息被写入哪个分区（partition，主题下的一段仅追加日志）：常见做法是对键计算一致性哈希值，再对主题的分区数取模，得到目标分区。只要分区数量不变，相同的键就会被哈希到同一个分区；但一旦分区数发生变化，同一个键就可能被路由到不同分区，所以「键相同必进同一分区」只在分
- `kafka-core-partition-ordering-scope` Q: Kafka 保证「消息按顺序处理」，但这个顺序保证的范围有多大？一个包含4个分区的主题，能保证跨分区的消息也按发送顺序被读到吗？
  A: 不能。Kafka 只保证消息在单个分区内的顺序：分区本质上是一段仅追加（append-only）的提交日志，消息按写入顺序追加到分区尾部，并按先入先出（FIFO）的顺序被读取。但一个主题通常包含多个分区，可能分布在不同服务器上被并行读写，因此同一主题内不同分区之间的消息没有全局顺序保证。
- `kafka-core-partitions-enable-scale` Q: 主题（topic，消息的分类单位，类似数据库里的表）为什么要被划分成多个分区（partition）？这对 Kafka 的横向扩展能力有什么帮助？
  A: 分区是 Kafka 实现数据冗余和横向伸缩的手段：一个主题的多个分区可以分布在不同的服务器上，使该主题的总吞吐量不受限于单台服务器的性能，多台机器可以并行处理不同分区的读写；同时，同一分区可以有多个副本保存在不同服务器上，防止某台服务器故障导致数据丢失。分区数量越多，理论上可并行参与该主题读写的服务器和消费者也越多。
- `kafka-core-schema-avro-vs-json` Q: Kafka 里的消息只是无结构的字节数组。如果生产者和消费者之间没有约定好的模式（schema，描述消息内容结构的规范），会带来什么问题？为什么很多 Kafka 用户选择 Apache Avro 而不是 JSON/XML？
  A: 没有共同模式时，消息的读写会紧密耦合：发布者一改格式，所有订阅者都得先升级才能兼容，反过来也一样，格式演进很脆弱。JSON、XML 这类模式简单易读，但缺乏强类型检查、版本兼容性差。Avro 把模式和消息体分开存储，格式紧凑，并同时支持向前和向后兼容的模式演化（schema evolution）——模式变化时读写双方都

## core.offsets — 偏移量（offset）：仅追加日志中的位置
理解偏移量作为分区内消息位置标识的语义，及其对消费进度追踪的意义。
- `kafka-core-offset-not-strictly-sequential` Q: 在同一个分区里，后写入的消息一定比先写入的消息偏移量大，但需要注意偏移量「不一定是严格单调递增」。这是什么意思？
  A: 这是指相邻消息的偏移量不保证是连续整数（不保证一定是 100、101、102…这样紧挨着），中间可能存在跳跃，但先后顺序关系是保证的：写入越晚的消息，偏移量一定越大。因此不能把偏移量当成「消息计数」来推算分区里一共有多少条消息，只能把它当成一个严格递增的位置标记来判断消息先后顺序。
- `kafka-core-offset-tracks-consumer-progress` Q: 一个消费者进程被重启后，为什么通常能从上次读到的地方继续处理，而不是重新从头读整个分区？
  A: 消费者会针对它读取的每个分区保存一个「下一个要读取的偏移量」，这份进度信息通常保存在 Kafka 自身当中。消费者关闭或重启并不会丢失这份记录，恢复后可以直接从保存的偏移量继续读取，从而实现断点续读，而不必每次都从分区最开始重新消费一遍。
- `kafka-core-offset-uniqueness-per-partition` Q: 偏移量的「唯一性」是在什么范围内成立的？两个不同分区里能不能出现相同的偏移量数值？
  A: 偏移量只在同一个分区内保证唯一：给定分区里每条消息的偏移量都不同，且越往后的消息偏移量越大。但偏移量不是全局唯一的，不同分区各自独立计数，所以分区 A 的偏移量 100 和分区 B 的偏移量 100 是完全独立的两条消息，彼此没有关系。
- `kafka-core-offset-vs-key` Q: 消息的「键」（key）和消息的「偏移量」（offset）都是和 Kafka 消息相关的元数据，二者的作用有什么本质区别？
  A: 键是生产者可选设置的字节数组，用于决定消息被路由到哪个分区（例如相同键的消息落到同一分区），它与消息的业务内容有关，由生产者控制；偏移量则是 Kafka 在消息成功写入某个分区后自动分配的递增整数，只用来标识这条消息在该分区日志里的位置，与业务内容无关，完全由 broker（Kafka 服务器节点）维护，消费者只能读取
- `kafka-core-offset-what-is` Q: Kafka 会给分区（partition，主题下的一段仅追加日志）里的每一条消息附加一个「偏移量」（offset）。这个偏移量到底标识的是什么？
  A: 偏移量是 Kafka 在消息写入分区时附加的一个不断递增的整数元数据，用来标识这条消息在该分区内的位置，类似日志文件里「第几行」的编号。它不是消息内容的一部分，而是 Kafka 系统自己维护的位置标记，消费者靠它来定位和追踪自己读到了哪里。

## core.replication-isr — 副本、首领/追随者与同步副本集合（ISR）
掌握分区副本的首领-追随者模型，以及ISR如何界定哪些副本被视为已同步。
- `kafka-core-follower-reads-latency-tradeoff` Q: KIP-392 引入了「从跟随者副本读取数据」的特性，让消费者可以从地理上更近的副本读取而不总是从首领读。这样做要付出什么代价？
  A: 为了保证从跟随者读到的消息也是已提交（committed）的，首领要把当前的高水位标记（最近一次成功提交的偏移量）随数据一起发给跟随者，跟随者据此才能对外暴露已提交的消息，这个传递过程带来额外延迟。所以从跟随者副本读到数据会比直接从首领副本读取更晚出现；如果业务对消费延迟敏感，应继续从首领读取，只有当降低网络成本（如跨
- `kafka-core-isr-definition` Q: 跟随者副本要满足什么条件才会被算作「同步副本」，从而留在 ISR（in-sync replicas，同步副本集合）里？
  A: 跟随者副本会像消费者一样不断向首领发送 Fetch 请求来拉取消息，首领据此判断每个跟随者已经复制到了哪个偏移量、落后了多少。如果一个跟随者持续按时发来请求，且与最新消息的差距没有超过 replica.lag.time.max.ms 参数设定的时间阈值（例如 30 秒），它就被视为同步副本，留在 ISR 中；否则会被标
- `kafka-core-isr-leader-election-eligibility` Q: 首领所在的 broker 突然崩溃，Kafka 会从哪些副本里选出新首领？为什么一个长期落后的跟随者副本不能被选为新首领？
  A: Kafka 只会从 ISR（同步副本集合）里的副本中选举新首领，因为只有同步副本才能保证已经拥有首领此前确认过的全部消息。一个长期落后、不在 ISR 内的跟随者副本数据落后于首领，如果被选为新首领会导致部分已确认的消息「消失」，所以这类不同步副本没有资格参选，必须先追上首领、重新进入 ISR 才行。
- `kafka-core-leader-follower-roles` Q: 一个分区（partition）的多个副本（replica）分布在不同 broker 上时，为什么所有生产者的写请求都只能发给其中一个副本，而不能随便发给任意一个？
  A: 每个分区的多个副本中只有一个是首领副本（leader replica），其余都是跟随者副本（follower replica）。为了保证一致性，所有生产者的写请求以及默认的消费者读请求都必须经过首领副本；跟随者副本的任务是不断从首领那里复制消息，让自己的状态与首领保持一致，而不直接处理客户端的写请求。如果首领所在的 b
- `kafka-core-preferred-leader-rebalance` Q: 每个分区除了「当前首领」，还有一个「首选首领」（preferred leader）的概念，这是什么？为什么 Kafka 默认会定期把首领切回首选首领？
  A: 首选首领是创建主题时按均衡原则选定的那个副本，也就是分区最初分配到的、能让各个 broker 承担的首领数量大致均衡的副本。如果之后发生过故障转移，当前首领可能变成了别的副本，导致某些 broker 承担过多首领职责、负载不均衡。auto.leader.rebalance.enable 默认为 true 时，Kafka

## core.cluster-roles — broker、集群与多集群架构中的角色分工
理解broker、集群与生产者/消费者的职责边界，以及为何会出现多集群架构。
- `kafka-core-broker-role-capacity` Q: 在 Kafka 集群里，「broker」具体指什么？它承担哪些职责？
  A: 一个 broker 就是一台独立运行的 Kafka 服务器。它接收生产者发来的消息，为消息分配偏移量（offset）并提交到磁盘保存；同时响应消费者的读取请求，把已发布的消息返回给它们。根据硬件配置不同，单个 broker 可以轻松处理数千个分区、每秒百万级的消息量，是 Kafka 存储和服务能力的基本单位。
- `kafka-core-controller-role` Q: 一个 Kafka 集群由多个 broker 组成，为什么其中需要有一个 broker 兼任「控制器」（controller）角色？它是固定指定的吗？
  A: 控制器负责集群级别的管理工作，包括把分区分配给各个 broker，以及监控 broker 的存活状态。控制器不是固定指定某台机器，而是从当前存活的集群成员中自动选举产生的；如果控制器所在的 broker 失效，集群会自动选出新的控制器，从而保证集群管理功能不因单点故障而中断。
- `kafka-core-mirrormaker-architecture` Q: Kafka 提供的 MirrorMaker 工具是如何把一个集群的数据复制到另一个集群的？它的核心组件是什么？
  A: MirrorMaker 的核心是一对通过队列相连的消费者和生产者：消费者从源集群读取消息，生产者再把这些消息写入目标集群。典型用法是先把多个「本地」集群的数据汇聚到一个「聚合」集群，再把聚合集群的数据复制到其他数据中心，以此实现跨数据中心的数据同步，弥补 Kafka 副本机制无法跨集群工作的限制。
- `kafka-core-multicluster-reasons` Q: 随着 broker 数量增多，为什么建议使用多个 Kafka 集群，而不是一直把单一集群做大？
  A: 主要有三个理由：一是数据类型分离，让不同用途的数据跑在不同集群上互不干扰；二是安全需求隔离，不同敏感级别的数据用独立集群实现权限隔离；三是多数据中心的灾难恢复需求——如果业务分布在多个数据中心，需要让在线应用能访问到各站点汇总后的数据（例如用户在任一数据中心修改资料后，其他数据中心也要能看到更新）。
- `kafka-core-replication-scoped-to-single-cluster` Q: 如果业务同时运行在多个数据中心、需要用到多个 Kafka 集群，能不能依靠 Kafka 内置的分区复制机制（replication）把数据从一个集群复制到另一个集群？
  A: 不能。Kafka 的分区复制机制只能在单个集群内部把数据复制到不同的 broker 上（用于容错），不支持跨集群复制。要在多个集群之间同步数据，需要使用专门的工具（如 MirrorMaker），不能依赖普通的副本机制。
