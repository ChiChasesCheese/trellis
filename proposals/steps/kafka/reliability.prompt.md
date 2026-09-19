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
  "reliability.guarantees": ["<id shown first>", "…"],
  "reliability.broker-config": ["<id shown first>", "…"],
  "reliability.producer-reliable": ["<id shown first>", "…"],
  …
}

## reliability.guarantees — Kafka的可靠性保证及其边界
理解Kafka在顺序、至少一次/精确一次等方面提供的保证，以及这些保证成立所依赖的前提条件。
- `kafka-reliability-committed-not-flushed-to-disk` Q: Kafka 判定一条消息「已提交」的标准，是要求它被写到磁盘上吗？如果不是，判定标准是什么？
  A: 不是。Kafka 认为消息「已提交」的条件是它已经被写入该分区**全部同步副本（ISR）**，而不要求这些副本已经把数据从操作系统缓存冲刷（flush）到磁盘上——落不落盘是操作系统按自己的策略决定的时机问题，Kafka 主要靠多副本复制而不是靠强制刷盘来保证持久性。生产者可以通过 `acks` 配置选择自己关心的确认
- `kafka-reliability-follower-isr-three-conditions` Q: 一个跟随者副本（follower replica）要被算作同步副本、留在 ISR（in-sync replicas，同步副本集合）里，必须同时满足哪三个条件？只要有一个不满足会怎样？
  A: 三个条件：1）与 ZooKeeper 保持活跃会话，也就是最近 6 秒（可配置）内向 ZooKeeper 发送过心跳；2）最近 10 秒（可配置）内从首领那里复制过消息；3）不仅复制过消息，而且是复制到了**最新**的消息——单纯「还在复制，但一直追不上最新进度」超过 10 秒同样不合格。只要有一条不满足（比如与 Zo
- `kafka-reliability-four-core-guarantees` Q: Kafka 对可靠性做出的四条基本保证是：{{c1::分区内消息有序（同一个生产者写入同一分区，先写的消息偏移量更小，消费者按此顺序读取）}}；{{c2::消息只有被写入分区的全部同步副本（ISR，in-sync replicas）后才算「已提交」，不要求先落盘}}；{{c3::只要还有一个副本存活，已提交的消息就不会丢失}}；{{c4::消费者只能读取到已提交的消息}}。这四条是 Kafka 能力的边界，本身并不等于「系统整体可靠」，还需要围绕它们做进一步的配置权衡。
- `kafka-reliability-guarantee-vs-full-reliability` Q: Kafka 官方文档列出了几条关于顺序、提交和持久性的「保证」。为什么说仅凭这些保证本身，并不能让一个基于 Kafka 构建的系统自动变得「可靠」？
  A: 「保证」只是描述系统在各种环境下会始终如一表现出的行为边界（就像关系数据库的 ACID：原子性、一致性、隔离性、持久性描述事务行为的边界），它告诉你系统承诺了什么、没承诺什么。但把这些保证真正落实成一个可靠系统，需要开发者和管理员根据业务需求主动去配置和取舍：例如愿意为更强的持久性牺牲多少可用性、吞吐量、延迟或硬件成本
- `kafka-reliability-lagging-isr-vs-out-of-isr-tradeoff` Q: 一个「已经在 ISR（同步副本集合）里但复制略微滞后」的副本，和一个「已经被移出 ISR、彻底不同步」的副本，二者分别会给生产者/消费者带来什么不同的代价？
  A: 只要还留在 ISR 里，无论复制多滞后，只要没被移出，客户端在等待「所有同步副本都确认」时就必须等这个较慢的副本，因此它会拖慢生产者和消费者的整体速度。而一旦这个副本被判定为不同步、移出了 ISR，Kafka 就不再要求它确认，性能上不再受它拖累；但代价是有效的复制系数（同时保持同步的副本数）变小了，一旦此时再发生宕机

## reliability.broker-config — broker层可靠性配置
掌握复制系数、不彻底的首领选举（unclean leader election）与最少同步副本（min.insync.replicas）如何共同决定可用性与数据丢失风险之间的取舍。
- `kafka-reliability-flush-to-disk-vs-replication` Q: Kafka 通常不会要求消息在确认写入成功之前先被冲刷（flush）到磁盘，而是靠多副本复制来保证持久性。为什么这被认为已经足够安全？如果还是想更频繁地强制刷盘，可以调哪些参数？
  A: 理由是：把数据复制到 3 台分布在不同机架或可用区的机器上，比只把消息刷到首领这一台机器的磁盘上更安全，因为两个不同机架/可用区同时发生故障的概率非常低——多副本本身就是一种更强的持久性手段。broker 默认只在重启前、日志片段被写满关闭（默认 1 GB）或操作系统页面缓存写满时才把消息刷盘。如果仍然希望更主动地控制
- `kafka-reliability-lag-timeouts-tuning` Q: Kafka 2.5.0 把 `zookeeper.session.timeout.ms` 的默认值从 6 秒调大到 18 秒，把 `replica.lag.time.max.ms` 的默认值从 10 秒调大到 30 秒，动机是什么？把这两个超时调得更大，分别会带来什么正面和负面影响？
  A: 动机是提高云环境下集群的稳定性：云上网络延迟波动更大，过短的超时容易把仅仅是短暂抖动（网络波动、垃圾回收停顿）的副本误判为「不同步」而移出 ISR，造成不必要的抖动。调大 `zookeeper.session.timeout.ms`（允许 broker 不发心跳的最长时间）能减少这种误判，但代价是真正宕机的 broke
- `kafka-reliability-min-insync-replicas` Q: 一个复制系数为 3 的主题把 `min.insync.replicas`（最少同步副本数）设置为 2。如果集群里有 2 个副本同时变得不可用，只剩 1 个同步副本，broker 会怎么处理这时候的生产请求和消费请求？为什么这样设计？
  A: broker 会拒绝生产者的写入请求，抛出 `NotEnoughReplicasException`（同步副本不足异常）；但消费者仍然可以继续读取分区里已有的数据，也就是说这个分区实质上变成了**只读**状态，要等两个不可用副本中至少一个恢复并重新追上同步状态，才能恢复可写。这样做是因为如果只剩 1 个同步副本时还允许
- `kafka-reliability-rack-awareness` Q: Kafka 保证一个分区的多个副本会分布在不同的 broker 上，但为什么还建议额外配置 `broker.rack`（机架/可用区标识）？只保证「不同 broker」为什么不够？
  A: 如果一个分区的所有副本恰好落在同一个机架里的不同 broker 上，那么只要这个机架的交换机发生故障，这些 broker 就会同时不可达，不管复制系数设得多高，这个分区照样整体不可用——「分散到不同 broker」防不住「整机架一起挂」这种相关性故障。配置 `broker.rack` 告诉 Kafka 每个 broke
- `kafka-reliability-replication-factor-tradeoffs` Q: 把一个主题的复制系数（replication factor，参数 `replication.factor`）从 3 提到 5，能多容忍几个 broker 同时失效仍可读写？这个提升是「免费」的吗，会带来哪些额外代价？
  A: 复制系数为 *N* 时，最多可以容忍 *N*-1 个 broker 失效而分区仍可读写；从 3 提到 5，能多容忍 2 个 broker 同时失效（从容忍 2 个提升到容忍 4 个）。但这不是免费的：1）需要至少 *N* 个 broker，且每份数据占用 *N* 倍磁盘空间——本质是用硬件换可用性；2）每增加一个副本都
- `kafka-reliability-unclean-leader-election-tradeoff` Q: 某分区唯一的同步副本（首领）也宕机了，此时只剩下几个滞后已久的不同步副本可以顶上。`unclean.leader.election.enable`（不彻底的首领选举）参数默认是 `false`，这个默认选择意味着系统在这种极端情况下会怎么表现？把它改成 `true` 又会带来什么风险？
  A: 默认 `false` 时，Kafka 拒绝让任何不同步副本当选新首领，宁可让这个分区保持**不可用**，直到原来的首领（最后一个同步副本）恢复上线为止——这可能持续数小时，但保证不丢已提交数据、也不会让消费者看到不一致的结果。改成 `true` 后，Kafka 允许某个不同步（数据落后）的副本当选新首领，分区可以立刻恢

## reliability.producer-reliable — 在可靠系统中配置生产者
掌握为保证可靠传递而设置的发送确认与重试策略，以及需要额外处理的错误场景。
- `kafka-reliability-acks-all-needs-exception-handling` Q: 把 `acks` 设为 `all` 之后，是不是就自动保证生产者不会丢消息了？一个典型的反例是什么？
  A: 不是。`acks=all` 只保证「如果消息被确认成功，那么它一定已经写入所有同步副本」，但它不负责处理「消息还没被确认成功」时发生的异常。一个典型的反例：生产者发消息时分区首领刚好崩溃、新首领还在选举中，broker 会向生产者返回「首领不可用」这类错误响应；如果生产者的代码没有正确捕获这个异常并重试，消息就直接丢了
- `kafka-reliability-acks1-silent-loss-scenario` Q: 集群配置了 3 个副本、关闭了不彻底的首领选举，生产者的 `acks` 设为 `1`。生产者发消息给首领，首领写入成功并回了「写入成功」，随后首领崩溃，而这条消息还没被跟随者副本复制。这条消息会丢失吗？生产者和消费者各自会不会「察觉」到问题？
  A: 会丢失：新首领是从没收到这条消息的跟随者中选出的，这条消息就此消失。奇怪的是双方都「察觉不到」——消费者看不到任何异常，因为这条消息本来就没有被写入所有同步副本，从未被判定为「已提交」，消费者本来就不该读到它，所以从消费者视角系统仍然一致；但生产者却已经收到了「写入成功」的确认，它并不知道这条消息其实丢了。这说明只要 
- `kafka-reliability-idempotence-dedupes-retries` Q: 开启生产者重试后，消息可能因为「响应丢失导致误判失败并重发」而被写入两次。Kafka 提供了什么参数来消除这种因重试造成的重复，而不需要应用自己去做去重？
  A: 把 `enable.idempotence` 设为 `true` 即可。开启后，生产者会在每条消息（准确说是每个批次）里附带额外的标识信息，broker 能据此识别出「这其实是刚才那次请求的重发」，从而跳过重复写入，只保留一份。这样，生产者的重试机制既能保证消息不因为网络抖动而丢失，也不会因为重试而产生重复，二者不再是
- `kafka-reliability-manual-error-handling-categories` Q: 即使已经用好了生产者内置的自动重试机制，开发者仍需要自己在代码里处理哪几类错误？为什么这些错误不能靠「多重试几次」解决？
  A: 主要有四类：1）不可重试的 broker 错误（如消息体积超限、身份验证失败）——问题在请求本身，重试无意义；2）消息发送**之前**就发生的错误（如序列化失败）——请求根本没到 broker，broker 的重试机制管不到；3）生产者达到重试次数上限、或缓存待重试消息占用的内存达到上限时报出的错误——说明重试本身的资
- `kafka-reliability-retry-config-at-least-once` Q: 如果目标是「绝不丢消息」（至少一次交付，at-least-once），生产者的重试相关参数应该怎么配置？这样配出来能保证「只交付一次」吗？
  A: 建议把重试次数保持默认（几乎是无限次，整型最大值），改为用 `delivery.timeout.ms` 控制「愿意为一条消息的最终交付等待多久」——生产者会在这个总时限内持续重试可重试错误，超时才放弃。这样配置能保证消息「至少被保存一次」，但换来的代价是**可能重复**：如果一次请求其实已经在 broker 端成功写入
- `kafka-reliability-retryable-vs-nonretryable-errors` Q: 生产者收到 broker 返回的错误后，Kafka 客户端会自动重试某些错误，但另一些错误重试也没用。用 `LEADER_NOT_AVAILABLE`（首领不可用）和 `INVALID_CONFIG`（配置无效）两个错误码举例，说明二者的区别及原因。
  A: `LEADER_NOT_AVAILABLE` 是**可重试错误**：分区首领可能只是暂时缺失（正在选举新首领），过一会儿再发一次，新首领选出来后请求就能成功，所以客户端会自动重试。`INVALID_CONFIG` 是**不可重试错误**：问题出在请求本身的配置有误，不管重试多少次，只要配置不改，结果都会一样失败，重试纯

## reliability.consumer-reliable — 在可靠系统中配置消费者
理解消费者的可靠性配置与手动提交偏移量的时机如何避免消息丢失或重复处理。
- `kafka-reliability-auto-commit-risk` Q: 使用 `enable.auto.commit=true`（自动提交偏移量）最省心，但它有一个主要缺点，具体是什么场景？为什么这种场景必须改用手动提交？
  A: 自动提交按 `auto.commit.interval.ms`（默认 5 秒）定期提交，如果消费者在两次自动提交之间处理了一些消息后就被关闭，这段还没来得及被自动提交覆盖的处理量在重启后会被重复处理——这本身是自动提交「重复处理数量不可控」的固有代价。更严重的是当处理逻辑变复杂时，比如把消息交给另一个后台线程异步处理：
- `kafka-reliability-auto-offset-reset-tradeoff` Q: 一个消费者第一次启动，或者它请求的偏移量在 broker 上已经不存在了（比如超过保留期被删除）。`auto.offset.reset` 参数的 `earliest` 和 `latest` 两个取值，分别会让消费者怎么读，各自的代价是什么？
  A: 设为 `earliest` 时，消费者会从分区**最开始**的位置读取，好处是尽量不漏掉任何数据，代价是可能会重复处理大量早已存在的历史消息。设为 `latest` 时，消费者从分区**末尾**（也就是当前最新位置）开始读，好处是不会处理旧的重复数据，代价是很可能**错过**在它开始读之前就已经写入、还没被消费过的消息
- `kafka-reliability-commit-after-processing-rule` Q: 在手动管理偏移量提交时，有一条黄金规则是「一定要在处理完消息之后再提交偏移量」。如果违反这条规则——提交了已经读取但还没处理完的消息的偏移量——会造成什么后果？
  A: 提交偏移量的含义是「向 Kafka 声明：这个偏移量之前的消息我都已经处理好了，之后可以从这里往后接着读」。如果消息其实还没处理完就提交了它的偏移量，一旦此时消费者崩溃或触发再均衡（rebalance，分区被重新分配给群组内其它消费者），接手的消费者会直接从这个已提交的偏移量之后开始读，那些「已提交但未真正处理完」的消
- `kafka-reliability-commit-frequency-tradeoff` Q: 手动提交偏移量时，「每处理一条消息就提交一次」和「攒很多条消息处理完才提交一次」相比，各自的优劣是什么？和生产者 `acks=all` 有什么类比之处？
  A: 每条消息提交一次能把「重复处理的消息数」压到最低（哪怕消费者随后崩溃，最多只重复处理最后一条），但提交本身需要额外的网络往返开销，而且同一个消费者群组的提交请求都发往同一个 broker，提交太频繁可能把这个 broker 压垮，这种额外开销与生产者设 `acks=all`（要等所有同步副本确认才返回）导致延迟升高是类
- `kafka-reliability-consumer-retry-patterns` Q: 消费者从 Kafka 读到一批消息，其中某一条（比如要写入的目标数据库暂时不可用）处理失败，需要稍后重试，但不能因此不管后面成功处理的消息。为什么不能简单地「先跳过失败的这条、照常提交后面消息的偏移量」？有哪两种可行的处理模式？
  A: 不能这么做的原因是：Kafka 提交偏移量不像传统消息队列那样是对单条消息的「确认（ack）」，而是「这个偏移量之前的消息全部处理完了」的整体声明。如果第 30 条处理失败、第 31 条处理成功就提交第 31 条的偏移量，等于向 Kafka 宣称第 30 条也已经处理完，之后不会再有人重新处理它。有两种可行模式：1）遇
- `kafka-reliability-groupid-full-vs-subset-read` Q: 同一个 `group.id`（消费者群组标识）下的多个消费者订阅同一个主题时，各自能读到主题的全部消息吗？如果想让某个消费者独立读到主题里的每一条消息，应该怎么配置？
  A: 不能。同一个 group.id 下的消费者会分摊主题各分区，每个消费者只读到分配给自己的那部分分区，也就是整体消息的一个子集；只有把这个群组里所有消费者的读取结果合起来，才等于主题的全部消息。如果希望某一个消费者单独完整地读到主题的每一条消息（而不是被分摊），就要给它配一个在集群里唯一、不与任何其他消费者共享的 `gr

## reliability.validation — 验证系统可靠性
掌握通过配置校验、应用程序测试与生产环境监控三个层面持续验证可靠性保证的方法。
- `kafka-reliability-app-fault-injection-testing` Q: 验证了 broker/客户端配置没问题之后，为什么还需要单独对应用程序做集成测试？针对哪些故障场景做测试，测试的关键方法是什么？
  A: 配置验证只能证明「Kafka 这套配置本身能达到预期行为」，不能证明「应用程序自己写的错误处理逻辑、偏移量提交方式、再均衡监听器代码」是否正确地利用了这些配置——这些逻辑千差万别，只能靠针对性测试。建议测试的故障场景包括：客户端与服务器断连、客户端与服务器间高延迟、磁盘写满、磁盘挂起（掉电）、首领选举，以及对 brok
- `kafka-reliability-consumer-lag-metric` Q: 消费者端最重要的可靠性监控指标是「消费者滞后（consumer lag）」，它衡量的是什么？为什么这个指标即使系统一切正常也会有波动，配置告警时要注意什么？
  A: 消费者滞后指的是「消费者当前处理到的位置」和「分区里最新（已提交）消息的偏移量」之间的差距，理想值是 0，即消费者始终读的是最新消息。但实际中 `poll()` 方法每次会一次性返回一批消息，消费者需要花时间把这批处理完才会去拉下一批，所以这个差距会随着每次批量读取和处理而正常波动，不代表出了问题。配置告警时真正要关心
- `kafka-reliability-endtoend-and-broker-error-metrics` Q: 除了单独看生产者和消费者各自的指标，还需要监控什么，才能确认「数据从生成到被消费，整个链路是端到端可靠、及时的」？broker 侧又提供了哪两个可以用来发现异常的指标？
  A: 需要监控**端到端的数据流**：让生产者记录自己每秒生成的消息数量，消费者记录自己每秒读取的消息数量以及「消息生成时间戳（Kafka 从 0.10.0 起会给每条消息打时间戳）与被读取时间」之间的差值，再用一个系统把两边的数据汇总比对，确认没有消息在中途丢失、且生产到消费的时间差落在业务可接受的范围内——这类端到端监控
- `kafka-reliability-monitor-producer-error-retry` Q: 在生产环境里持续监控生产者的可靠性时，最重要的两个指标是什么？除了看这两个聚合指标，还建议关注哪些日志信息？
  A: 最重要的两个指标是生产者的**错误率**和**重试率**（都是聚合后的指标）——这两个指标一旦上升，说明系统出了问题。除此之外还建议关注生产者日志中 `WARN` 级别的报错（比如某次发送出错、正在重试、还剩几次重试机会的记录），一旦看到「剩余重试次数为 0」，说明这条消息已经没有自动重试的余地了；`ERROR` 级别
- `kafka-reliability-three-validation-levels` Q: 把生产者、broker、消费者都按可靠性需求配置好之后，还要从三个层面持续验证系统真的可靠：{{c1::验证配置（用工具单独测试 broker/客户端配置，不涉及应用逻辑）}}、{{c2::验证应用程序（对错误处理、偏移量提交、再均衡监听器等做集成测试，模拟故障场景）}}、{{c3::在生产环境中监控可靠性（持续观察客户端指标、消费者滞后和端到端数据流）}}。三者缺一不可：配置对不代表代码写对，代码在测试环境里对也不代表生产环境长期正常。
- `kafka-reliability-verifiable-producer-consumer` Q: Kafka 自带的 `VerifiableProducer` 和 `VerifiableConsumer` 这两个命令行工具是用来做什么的？为什么要用它们而不是直接上线跑真实的业务生产者/消费者来验证可靠性配置？
  A: `VerifiableProducer` 会按你配置的 `acks`、`retries`、`delivery.timeout.ms` 等参数，持续发送一串编号从 1 到指定数字的消息，并把每条消息成功/失败的结果打印出来；`VerifiableConsumer` 负责读取这些消息，按读取顺序打印出来，同时打印偏移量和再
