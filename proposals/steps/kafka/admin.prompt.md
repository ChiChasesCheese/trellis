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
  "admin.topic-ops": ["<id shown first>", "…"],
  "admin.consumer-group-ops": ["<id shown first>", "…"],
  "admin.dynamic-config": ["<id shown first>", "…"],
  …
}

## admin.topic-ops — 主题运维：AdminClient与命令行工具
掌握用AdminClient编程式管理主题的异步/最终一致性API模型，以及用命令行工具创建、扩容、删除主题和收发消息。
- `kafka-admin-adminclient-eventual-consistency` Q: 调用 AdminClient.createTopics 创建一个新主题，等它返回的 Future 完成（表示操作成功）后立刻调用 listTopics()，为什么返回的主题列表里有时还看不到这个刚创建的主题？
  A: Kafka 的管理操作（创建、删除、修改）都是发给集群控制器（controller，负责维护集群元数据的特殊 broker）处理的，AdminClient 的 Future 在**控制器**完成状态更新后就算完成，但控制器把这次变更同步给其他 broker 是一个异步过程。这时可能还有 broker 没收到最新元数据，
- `kafka-admin-cannot-decrease-partitions` Q: 为什么 Kafka 不支持直接减少一个主题的分区数量？如果业务上确实需要更少的分区，应该怎么做？
  A: 直接删掉某个分区，这个分区里保存的消息也会跟着被删除，造成客户端看到的数据不一致；即使想把这些消息重新分布到剩下的分区中，也很难保证消息原有的顺序，实现代价极高，因此 Kafka 干脆没有提供减少分区数的功能。如果确实需要更少的分区，建议的做法是整体删除并重建这个主题（会丢失原有数据），或者创建一个分区数合适的新主题（
- `kafka-admin-client-dns-lookup-modes` Q: 客户端连接配置参数 `client.dns.lookup` 有 `resolve_canonical_bootstrap_servers_only` 和 `use_all_dns_ips` 两个可选值，分别是为了解决什么部署场景下的连接问题？
  A: 场景一：用一个 DNS 别名（如 `all-brokers.hostname.com`）统一代表多个 broker 的真实主机名，并启用了 SASL 身份验证——客户端会拿别名去做服务器身份验证，但实际连上的 broker 主体却是它自己的主机名，名字不匹配会被 SASL 拒绝；这时配置 `resolve_canoni
- `kafka-admin-kafkafuture-nonblocking` Q: 在一个需要持续处理大量客户端请求的服务器里，用 AdminClient 的 describeTopics 之类方法查询 Kafka 状态时，为什么直接对返回结果调用 Future.get() 可能是个问题？应该怎么做？
  A: get() 会阻塞当前线程，直到 Kafka 真正返回响应或超时；如果这次调用发生在服务器处理请求的线程里，就意味着这个线程要一直等 Kafka 响应完才能继续处理别的客户端请求，拖慢整个服务的吞吐量。更好的做法是使用 AdminClient 返回的 KafkaFuture 提供的非阻塞接口（如注册 whenCompl
- `kafka-admin-keyed-topic-partition-increase` Q: 为什么建议一个消息带键（key）的主题在创建时就规划好分区数量，尽量避免后续用 kafka-topics.sh --alter 给它增加分区？
  A: Kafka 默认按消息键的哈希值对分区数取模，来决定一条消息该落到哪个分区。一旦增加了分区数量，同一个键的哈希取模结果会随之改变，导致这个键此后写入的新消息可能被路由到跟旧消息不同的分区，破坏了「相同键的消息始终落在同一分区、从而在这些消息之间保持顺序」的语义。这会让消费者看到的键与分区对应关系及消息顺序发生错乱，所以
- `kafka-admin-topic-deletion-caution` Q: 用 `kafka-topics.sh --delete` 删除一个主题，broker 端必须满足什么前置条件才会真的执行删除？为什么在大型集群里不建议连续、一次性删除很多个主题？
  A: broker 的配置参数 `delete.topic.enable` 必须设置为 true，否则删除请求会被直接忽略，主题不会被删除。即使条件满足，删除也是异步操作：主题先被打上删除标记，控制器（controller，负责维护集群元数据的特殊 broker）要等手头现有任务处理完才能通知各个 broker 让相关元数据

## admin.consumer-group-ops — 消费者群组管理与偏移量运维
掌握查看、修改消费者群组状态，以及手动管理其偏移量的运维操作。
- `kafka-admin-alter-offsets-requires-inactive-group` Q: 用 AdminClient 的 alterConsumerGroupOffsets（或命令行工具的偏移量重置功能）去修改一个消费者群组的偏移量时，为什么必须先确保这个群组里的所有消费者都已经关闭，否则操作可能失败或被覆盖？
  A: 消费者只有在启动时或被重新分配到新分区时才会去读取已提交的偏移量，运行过程中并不会感知偏移量在外部被修改，所以如果群组还活跃，消费者会继续按自己内存里的位置提交偏移量，把刚刚外部写入的新偏移量覆盖掉。更严重的是，如果消费者群组仍处于活跃状态，群组协调器（group coordinator，负责管理群组成员和偏移量提交的
- `kafka-admin-consumer-lag-calculation` Q: 想知道一个消费者群组在某个分区上「落后了多少条消息」（consumer lag，消费滞后），需要结合调用 AdminClient 的哪两类方法、分别取哪个值来计算？
  A: 先用 `listConsumerGroupOffsets` 拿到这个群组在每个分区上最近一次**提交的偏移量**（committed offset）；再用 `listOffsets` 并传入 `OffsetSpec.latest()`，拿到这个分区当前**最新消息的偏移量**（latest offset，即下一条要写入
- `kafka-admin-delete-group-requires-empty` Q: 用 `kafka-consumer-groups.sh --delete` 删除一个消费者群组时，如果群组里还有消费者在运行，会发生什么？
  A: 命令会直接失败，并抛出「群组不为空」的异常。删除消费者群组会把这个群组保存的所有已提交偏移量一并删除，所以 Kafka 要求必须先把群组里所有消费者都关闭，确保群组已经清空，才允许执行删除，避免在消费者还依赖这些偏移量的情况下把它们连同群组一起删掉。
- `kafka-admin-delete-offset-vs-reset-offset` Q: 想让一个消费者群组（consumer group，共同分摊读取同一批分区的一组消费者）重新从主题最开始的位置读取数据，为什么直接「删除」它已提交的偏移量（offset，消费者在某个分区里读到的位置）不是可靠的做法，而应该显式把偏移量「重置」为最早的偏移量？
  A: 删除偏移量只是让消费者在下次启动时找不到已提交的位置，此时它到底从最早位置开始读，还是直接跳到最新位置开始读，完全取决于消费者自身的 `auto.offset.reset` 配置——如果这个消费者配置的是跳到最新位置，删除偏移量反而会让它跳过所有历史数据。要保证消费者一定从头开始读，必须显式地把提交的偏移量改写成这个分
- `kafka-admin-offset-export-import-dry-run` Q: 用 `kafka-consumer-groups.sh --reset-offsets` 修改消费者群组偏移量前，为什么建议先加 `--dry-run` 参数导出一份 CSV 再修改导入，而不是直接执行重置命令？
  A: `--reset-offsets` 命令一旦不加 `--dry-run`，偏移量会被立即真实修改，这个操作没有撤销功能；先用 `--dry-run` 把当前每个主题分区对应的偏移量导出成 `<topic>,<partition>,<offset>` 格式的 CSV 文件，相当于对当前状态做了一份备份和可视化确认。修改前
- `kafka-admin-reset-offset-stateful-app-pitfall` Q: 一个统计「今天商店卖出多少双鞋」的流式处理应用，如果发现凌晨3点到8点的输入数据有错误，只是简单地把消费者群组的偏移量重置回凌晨3点、让它重新消费这段数据，会带来什么问题？
  A: 重置偏移量只是让消费者重新读取这段消息，但应用程序在这几个小时里已经把统计结果累加进了自己保存的状态（state，比如「已售出数量」这个累加值）里；重新消费同一批消息时，这些累加操作会在原有状态基础上再执行一遍，导致凌晨3点到8点这段时间卖出的每双鞋都被重复计数。所以重置偏移量之前必须同时对保存的状态做相应修正（比如回

## admin.dynamic-config — 动态配置变更
理解如何在不重启的情况下覆盖主题、客户端/用户与broker的默认配置，以及如何查看和移除这些覆盖。
- `kafka-admin-alterconfigop-types` Q: 用 AdminClient 的 incrementalAlterConfigs 修改配置时，每个修改操作都要指定一个操作类型（AlterConfigOp.OpType），Kafka 支持四种：{{c1::SET（设置一个新值）}}、{{c2::DELETE（删除该配置值，重置为默认值）}}、{{c3::APPEND（仅用于 List 类型配置，向列表追加值）}}、{{c4::SUBTRACT（仅用于 List 类型配置，从列表移除值）}}；APPEND 和 SUBTRACT 的意义在于不用每次都把整个列表重新发送给 Kafka。
- `kafka-admin-client-id-vs-group-naming` Q: Kafka 里客户端 ID（client ID）和消费者群组名字（consumer group name）是两个独立的标识，可以不一样；给消费者设置客户端 ID 时如果用能体现所属群组的命名方式，这样做有什么好处？
  A: 客户端 ID 主要用于配额（quota）管理和日志追踪，而配额和大部分运维配置都是按客户端 ID 或用户来设置的；如果同一个消费者群组里的消费者用了能体现群组归属的客户端 ID（比如带上群组名作为前缀），就可以方便地把配额统一配置给整个群组共享，而不需要给群组里每个消费者实例单独设置；同时在排查问题、查日志时，也能一眼
- `kafka-admin-describe-shows-overrides-only` Q: 用 `kafka-configs.sh --describe` 查看一个主题的配置时，输出里只列出了 `retention.ms=3600000` 这一行，这是不是说明这个主题只有 retention.ms 这一个配置项，其余配置都是空的？如果要做自动化脚本读取主题的完整有效配置，这一点意味着什么？
  A: 不是。`--describe` 命令只显示被**动态覆盖**过的配置，主题上其它所有沿用集群默认值的配置项根本不会出现在这份输出里，而且这个命令本身也无法动态查到 broker 级别的默认值是什么。这意味着如果自动化流程只依赖这个命令的输出去判断某个主题「实际生效」的完整配置，会遗漏所有走默认值的参数；要拿到完整有效配
- `kafka-admin-describeconfigs-isdefault` Q: 用 AdminClient 的 describeConfigs 查询一个主题的配置后，怎么判断某个具体配置项是使用集群默认值，还是被人为覆盖过？
  A: describeConfigs 返回的每一条 ConfigEntry（配置条目）都带有一个 isDefault() 方法：调用它返回 false，说明这个配置要么在主题级别被单独覆盖过，要么继承了 broker 级别的非默认值；返回 true 才说明它就是集群本身的默认配置。因此想找出「哪些配置被改动过」，只需要对 d
- `kafka-admin-quota-throttle-per-broker` Q: 给某个生产者客户端配置了 10 MBps 的生产配额（quota，限制客户端能使用多少资源），在一个有 5 个 broker 的集群里，这个客户端实际能达到的总生产速率是多少？为什么答案取决于分区首领（leader）的分布？
  A: 配额是按「客户端 - broker」这一对关系分别节流的，不是全局限制：客户端向每一个 broker 最多能以配置的速率（这里是 10 MBps）写入数据。如果这个客户端要写入的所有分区的首领均匀分布在 5 个 broker 上，它就能同时对每个 broker 都打满 10 MBps，总吞吐量可达 50 MBps；但如
- `kafka-admin-unclean-leader-election-tradeoff` Q: broker 的动态配置参数 `unclean.leader.election.enable` 允许一个没有跟上首领进度的副本（不在 ISR 里）被选为新首领，这本质上是拿什么去换取什么？什么场景下适合临时开启？
  A: 这个参数是用「可能丢失部分尚未同步到该副本的数据」去换取「集群能更快恢复可用性」：正常情况下 Kafka 只允许在 ISR（同步副本集合）内选举新首领以保证不丢数据，但如果 ISR 中的副本全部不可用，分区就会一直处于离线、不可写状态。当业务能够接受这段时间的数据丢失，或者集群已经发生了不可恢复的数据丢失、必须尽快让分

## admin.partition-reassignment — 分区管理与应急操作
掌握首选首领选举、副本重分配、日志片段转储等分区管理手段，以及移动控制器、强制删除主题等不安全但必要时使用的应急操作。
- `kafka-admin-cancel-reassignment-risk` Q: 用 kafka-reassign-partitions.sh 的 `--cancel` 选项取消一个正在进行中的分区重分配，会把副本集合恢复成什么状态？为什么这在某些场景下有风险？
  A: 取消操作会把分区的副本集合恢复到这次重分配开始之前的状态。但如果这次重分配本来就是为了把副本从一个已经失效或过载的 broker 上移走，取消操作意味着又把这些副本的职责放回给这个本就有问题的 broker，可能让集群回到一个非预期、依旧存在问题的状态；而且取消后恢复出来的副本集合顺序也不能保证和重分配之前完全一致，这
- `kafka-admin-force-move-controller` Q: Kafka 集群的控制器（controller，负责监督分区状态变更等集群级操作的特殊 broker 角色）出现异常但主机进程还在运行、没有真正宕机，导致集群操作不正常时，如何在不关闭这台机器的情况下强制把控制器角色转移给别的 broker？
  A: 正常情况下控制器角色是通过在 ZooKeeper 上抢占一个临时节点 `/admin/controller` 来选举产生的，控制器所在 broker 一旦断开连接，这个临时节点会被自动删除，其他 broker 就会去竞争成为新控制器。要在不关闭这台主机的情况下强制换控制器，可以手动删除这个 `/admin/contro
- `kafka-admin-manual-topic-delete-requires-full-shutdown` Q: 如果集群禁用了主题删除功能（`delete.topic.enable=false`），需要手动从 ZooKeeper 元数据里删掉一个主题时，为什么必须先关闭集群中**所有** broker，而不能在集群还在运行时直接改 ZooKeeper？
  A: broker 依赖 ZooKeeper 里保存的元数据来判断集群当前有哪些主题、分区分布在哪里；如果集群还在运行的时候直接从 ZooKeeper 删除主题相关节点，正在运行的 broker 手上缓存的元数据和 ZooKeeper 里的真实状态就会突然不一致，可能引发难以预料的集群不稳定甚至崩溃。因此手动删除的正确顺序是
- `kafka-admin-preferred-vs-unclean-leader-election` Q: Kafka 支持「首选首领选举（preferred leader election）」和「不彻底的首领选举（unclean leader election）」两种首领选举方式，它们分别用来解决什么问题？为什么不彻底的首领选举有风险？
  A: 每个分区的副本清单里，排在最前面的那个副本被指定为「首选首领」；正常情况下首领可能因为 broker 重启等原因转移给了别的副本，首选首领选举是把首领**换回**这个首选副本，目的是让各 broker 上的首领数量重新变得均衡，属于轻量、低风险操作，一般不会造成负面影响。不彻底的首领选举则用在极端情况：某个分区的首领副
- `kafka-admin-reassignment-throttle` Q: 用 kafka-reassign-partitions.sh 做分区副本重新分配时，为什么建议搭配 `--throttle` 参数限制复制速率，而不是让重分配尽快跑完？
  A: 副本重新分配的本质是把大量数据从旧副本所在的 broker 通过网络复制到新副本所在的 broker，这个过程会占用大量网络带宽和磁盘 I/O，还会打乱操作系统内存缓存页的命中模式，从而挤占集群正常处理生产者/消费者请求所需要的资源，拖慢正常的读写延迟。`--throttle`（以字节/秒为单位）把重分配的复制速率限制
- `kafka-admin-restart-broker-before-decommission` Q: 计划把一个 broker 的所有分区都搬走、然后把它从集群里移除时，有一个技巧：先重启这个即将被移除的 broker，再执行分区重分配，为什么这样能显著提升重分配的效率？操作时要注意什么？
  A: broker 重启（关闭）的过程会让它上面所有的分区首领自动转移给其他 broker；如果不这么做，重分配开始时这个 broker 往往还持有大量分区的首领，首领所在 broker 要承担该分区全部的读写和向其它副本复制数据的流量，会成为整个重分配过程的瓶颈。提前把首领转移出去后，原本集中在一台机器上的复制流量就被分摊
