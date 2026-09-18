---
title: TS02 · Kafka / 事件流
aliases:
  - TS02
  - Kafka 事件流
tags:
  - interview/stack
  - stack/kafka
stories: [S11, S1]
---

# 02 · Kafka / 事件流（Kafka / Event Streaming）

> 知识层（想更深时去哪）：[[Kafka MOC|kafka]]：[[core.topics-partitions]] · [[core.offsets]] · [[core.replication-isr]] · [[consumer.groups-rebalance]] · [[consumer.offset-commit]] · [[consumer.seek-and-replay]] · [[eos.idempotent-producer]] · [[eos.transactions]] · [[connect.pipeline-design]] · [[monitoring.lag-e2e]]；[[System Design MOC|system-design]]：[[async.log]] · [[async.delivery.guarantees]] · [[async.delivery.exactly-once]] <!-- domain-links -->
> 适用于：JD 上出现 Kafka / 事件驱动架构 / 消息队列 / 流处理 的岗；被问"讲讲你的 Kafka 经验"、"你们怎么保证消息不丢/不重"、"两个系统之间怎么同步数据"。
> 不适用于：Kafka Streams/ksqlDB 这类流处理框架的调优（我们没用，见第 5 节）；Broker 运维、分区扩容、ZooKeeper/KRaft 迁移这类基础设施侧问题（我们是消费方/管道使用方，不是集群运营方，同样见第 5 节）。

---

## 0. 这个栈在 JD 里到底在问什么

JD 上写 "Kafka" 时，面试官心里通常在问三件事之一：

1. **你懂不懂这东西的物理模型**——分区、offset、副本、ISR 到底是什么，为什么消息队列这么设计。这是纯知识题，第 1 节回答。
2. **你在真实系统里怎么用它**——消费什么、发布什么、怎么保证不丢不重、出问题怎么办。这是系统设计+深挖题，第 2 节回答，也是这份文章的重点，因为我的 Kafka 经验主要是**消费端**（consumer）而不是生产端调优或集群运维。
3. **你对"exactly-once"这个词有多诚实**——很多人把它当成一个可以打勾的 feature，真正的工程师会告诉你它是一句需要拆开验证的复合承诺。第 1.3/1.4 节专门讲这个。

---

## 1. 来龙去脉

### 1.1 没有它的时候，人们怎么做，痛在哪

设想一个电商系统：订单服务下单后，要通知库存服务扣库存、通知物流服务生成运单、通知财务服务记账。最朴素的做法是订单服务在一次请求里同步调用这三个下游的 API。这立刻带来三个问题：

- **耦合**：订单服务的可用性变成了自己 AND 库存 AND 物流 AND 财务的可用性乘积，任何一个下游慢或挂，下单就跟着挂。
- **扩展成本线性增长**：明天要加一个"通知会员积分服务"，就要改订单服务的代码、重新部署、重新测试整条调用链。
- **没有回放能力**：如果财务服务因为一个 bug 把过去一小时的账都记错了，唯一的补救办法是让订单服务重新调用一次——但订单服务早就把这批订单处理完、状态也变了，"重放历史"这件事在同步调用模型里根本没有一等公民的位置。

传统消息队列（如 ActiveMQ、RabbitMQ）解决了前两个问题——发布者把消息丢进队列就返回，消费者各自异步处理，耦合被打断。但队列模型有一个致命假设：**消息被消费后就从队列里删除了**。这意味着：

- 只能有一个逻辑消费者组消费一条消息一次（或者要为每个消费者单独复制一份队列），"多个下游各自独立消费同一批事件"很别扭。
- 一旦消费者处理出错或者需要重新跑一遍历史数据（比如财务口径变了要重算过去 30 天），消息已经被删了，没法回放。
- 消息的顺序保证很弱，一旦引入多个 consumer 并行消费同一个队列，顺序基本没法保证。

Kafka 的出发点不是"造一个更快的队列"，而是**换一个数据结构**：不删除、只追加的日志（log），彻底放弃"消费=删除"这个前提。

### 1.2 核心抽象

Kafka 的核心抽象是**分区化的、仅追加（append-only）的持久化日志**：

- **Topic**：一个逻辑上的事件流名字，比如"某商户交易结算事件"。
- **Partition**：Topic 被切成若干个分区，每个分区内部是一个严格有序、按 offset 递增编号、只能在末尾追加的日志文件。分区是 Kafka **并行度的最小单位**——多少个分区，理论上就有多少路可以并行读写；同时也是**顺序保证的边界**——Kafka 只保证同一分区内消息有序，不保证跨分区有序。这一点常被面试问到:"Kafka 保证顺序吗?"标准答案是"分区内保证，Topic 级别不保证",这直接决定了你选 partition key 时要把"必须严格有序的实体"(比如同一笔交易的所有事件)哈希到同一个分区。
- **Offset**：消费者在某个分区里"读到哪了"的位置，是一个单调递增的整数,由消费者自己持有和管理(Kafka broker 侧存的是消费者提交的最后位置,不是"这条消息被谁消费过"这种状态)。这是 Kafka 和传统队列最大的模型差异——**消息不会因为被消费而消失**,不同的消费者组各自维护自己的 offset,互不干扰,同一批数据可以被无数个下游各自独立地、以各自的进度消费。回放历史,本质上就是把 offset 往回拨。
- **Replication / ISR (In-Sync Replica)**：每个分区有一个 leader 副本和若干 follower 副本,生产者/消费者只和 leader 交互,follower 异步(但要跟上)从 leader 拉数据。**ISR 是"目前追得上 leader 进度"的副本集合**——只有在 ISR 里的副本,才有资格在 leader 挂掉时被选为新 leader。这解决了"复制"最核心的权衡:一个已经掉队太久的副本(可能因为磁盘慢、网络抖动)会被踢出 ISR,防止用一个数据不全的副本去接任 leader 造成数据丢失。`acks=all` 的真实含义是"等到所有当前 ISR 成员都确认写入",而不是"等到所有副本都确认"——这也是为什么 ISR 集合大小会变化时,持久性保证的实际强度也在变化。

### 1.3 关键权衡：Kafka 买到了什么，代价是什么

- **买到**：极高的顺序写入/顺序读取吞吐(日志结构对磁盘顺序 I/O 友好)、多消费者独立回放、天然的解耦和缓冲(下游可以慢,不会拖垮上游)、消息保留期内可重放历史。
- **代价**：
  - **没有"删除单条消息"的概念**,只有整个分区按时间/大小滚动删除最旧的日志段(retention),想做"某条消息处理完就立刻从存储里清掉"这种队列语义,Kafka 天然做不到。
  - **顺序只在分区内成立**,如果你的业务需要跨分区的全局顺序,要么接受做不到,要么把所有相关消息强制路由到同一分区(牺牲并行度)。
  - **消费侧的复杂度从 broker 转移到了消费者自己身上**:offset 什么时候提交、提交失败了怎么办、消费者挂了重启后从哪接着读——这些在传统队列里由 broker 托管的语义,在 Kafka 里都是消费者应用要自己想清楚的问题(第 2 节会看到我们的系统怎么处理这个)。

**Delivery semantics 阶梯,以及"exactly-once"到底是什么意思**——这是这个技术里最容易被讲错的地方:

1. **At-most-once**:消费者先提交 offset,再处理消息。如果处理过程中挂了,这条消息就永远丢了,但绝不会重复处理。
2. **At-least-once**:消费者先处理消息,处理成功后再提交 offset。如果提交之前挂了,重启后会从上一个已提交的 offset 重新拉取,导致同一条消息被处理两次。这是工程实践里最常见的默认选择,因为"丢消息"通常比"重复消息"更难接受,而重复可以用幂等消费(见下)来兜底。
3. **"Exactly-once"**:Kafka 从 0.11 开始提供的幂等生产者(idempotent producer)和事务(transactions)能保证的,严格来说是"**生产端**不会因为重试而产生重复消息"和"**consume-transform-produce**这个模式里,消费、处理、再生产这三步要么全部提交要么全部不提交(原子性)"。它**不保证**:
   - 消费者处理消息后产生的**外部副作用**(写数据库、调第三方 API、发一封邮件)是幂等的——如果处理逻辑本身不是幂等的,"exactly-once 语义"的 Kafka 事务照样能让你在数据库里插入两条记录。
   - 端到端(从最初的事件源头到最终所有下游)的"恰好一次"——那是无数个环节各自幂等叠加出来的结果,不是 Kafka 一个 flag 能替你保证的性质。

  所以更准确的说法是**"effectively-once"**——通过"消息层面不重复投递(幂等生产者/事务)" + "业务层面的幂等处理(唯一键、去重表)"两层叠加,达到"业务效果上看起来像恰好发生了一次"的效果,而不是 Kafka 单方面提供的一个开关。第 2 节会讲我们系统实际选的是哪一层。

### 1.4 演化到今天

- **早期(0.8 之前)**:offset 存在 ZooKeeper 里,consumer 每次提交都是一次 ZK 写,规模一大就是瓶颈。之后 offset 迁移到一个内部 Kafka topic(`__consumer_offsets`)自己管理,吞吐和可靠性都好得多——"用 Kafka 自己的日志能力来存 Kafka 自己的元数据"这个自举思路,后来在 KRaft(用 Kafka 日志取代 ZooKeeper 存集群元数据)上被推到了极致。
- **0.11 引入幂等生产者 + 事务**,是"Kafka 只是消息总线"到"Kafka 可以支撑金融级流处理"叙事转变的关键版本。
- **Kafka Connect** 把"往 Kafka 里搬数据/从 Kafka 往外搬数据"标准化成 source/sink connector 配置,而不是每个团队各写一套生产者/消费者胶水代码——这也是本文第 2.2 节 Funding→Snowflake CDC 管道能"零应用代码"落地的原因:用的是 Snowflake 官方 Kafka Connector,不是手写消费者。
- **今天的默认选择**是:分区数按目标吞吐和消费并行度反推(不是越多越好,分区数太多会拖慢 leader 选举和 controller 元数据量);至少 3 副本 + `min.insync.replicas=2` 是生产环境的常见底线;消费侧默认 at-least-once + 应用层幂等,而不是无脑上事务(事务有明确的吞吐代价,见 [[eos.transactions-perf]])。

---

## 2. 在我们这套系统里它怎么用

**先说清楚我的 Kafka footprint 的性质**:我没有运维过 Kafka broker、没有做过分区扩容或 ISR 调优、也没有配置过 Kafka Connect worker 集群本身。我的经验是**消费侧应用代码**(`pricing` 服务用 Spring Kafka 消费上游事件)和**管道设计的下游消费者**(Snowglobe 侧接收 Funding 经 Kafka CDC 同步来的数据)。下面讲的是这两条真实存在的生产链路,系统全貌为主,我自己做的部分在 2.3 单独标出。

### 2.1 架构位置

Kafka 在这套 pricing/snowglobe/funding 系统里是**两条独立通路的骨架**,服务不同目的:

**通路一:`pricing` 消费上游事件,计算 BT Fee(Braintree Fee)**

```
Gateway/Arbiter 等上游系统
   │  Kafka topics: transaction-events / dispute-events / EBB events ...
   ▼
pricing 服务(Spring Kafka @KafkaListener,批量消费)
   │  TransactionEventConsumer / DisputeEventConsumer 等,按事件类型各自一个 consumer + 独立 group id
   ▼
落库 PostgreSQL(Transaction 表等)+ 计算 BT Fee
   │  Kafka topic: 内部 bt-fee 事件(BTFeeProducer 发布)
   ▼
下游 funding partners 订阅这个内部 topic
```

真实代码在 `pricing/src/main/kotlin/com/braintree/pricing/events/`,按事件类型分包:`transactions/TransactionEventConsumer.kt`、`disputes/DisputeEventConsumer.kt`,以及 `schemefee/`、`interchangefee/`、`valueadded/`、`fraud/` 等同构的其他事件包。发布端在 `pricing/src/main/kotlin/com/braintree/pricing/worker/btfees/BTFeeProducer.kt`。

**通路二:Funding → Snowflake 的 Kafka CDC 管道**

```
funding(Ruby on Rails,PostgreSQL)
  表: pricing_schedules / pricing_schedule_fees
   │  Kafka CDC(Snowflake Kafka Connector)
   ▼
Snowflake 原始落地表(snowglobe 侧 Terraform 定义)
   │  Stream + Task + Procedure(与 Amex GRRCN 摄入是同一套模式:见 03-snowflake-warehouse.md §2)
   ▼
snowglobe 侧 FUNDING_PRICING_SCHEDULES / FUNDING_PRICING_SCHEDULE_FEES 表
```

这条通路记录在 `snowglobe-terraform` 仓库的 `modules/cdc/main.tf`(单文件近 4000 行)里,注释直接引用了 funding 仓库的具体 commit SHA(如 `036bf5c...` 对应 `pricing_schedules` 表、`2b63648f...` 对应 `pricing_schedule_fees` 表),两组表分别配了平行的 stream/UDTF/procedure/task 结构。这条路径和 `pricing → funding` 之间那条基于 gRPC 的定价方案同步(见 `pricing.proto` 的 `CreatePricingSchedule`)是**两条独立通路**:gRPC 那条是"pricing 是权威源、实时创建/查询",Kafka CDC 这条是"funding 库里存量的历史定价明细表批量搬迁进 Snowflake,供 Snowglobe 侧的费用计算读取"——服务目的不同,不要混为一谈。

（背景补充:Gateway → Snowglobe 的交易事件摄入,走的也是 Kafka topic `events_entity_transaction_global` → Snowflake Kafka Connector(Snowpipe Streaming)→ `EVENTSTREAM_TRANSACTION_STATUS_EVENTS` 落地表,这是同一套 Snowflake Kafka Connector 基础设施的第三个使用场景,但不是这份文章要深挖的两条主线,详见 `03-snowflake-warehouse.md`。）

### 2.2 关键 feature 与设计决策

**(1) 批量消费 + 手写错误日志表,而不是 Kafka DLQ topic**

`pricing` 的每个 consumer(如 `TransactionEventConsumer`)用 `@KafkaListener` 的**批量监听**模式(`ConcurrentKafkaListenerContainerFactory.isBatchListener = true`),一次拉一批 `ConsumerRecord` 处理。`KafkaConsumerConfiguration.kt` 里的关键配置:

```kotlin
ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG to true,
ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG to 100,
```

出错处理用 Spring Kafka 的 `DefaultErrorHandler` + `FixedBackOff(5000L, 2L)`(失败后等 5 秒重试,最多重试 2 次),并显式声明一组"不可重试异常"(`DataIntegrityViolationException`、`IllegalStateException`、`InvalidProtocolBufferException`)——命中这些异常直接放弃重试,调 `messageErrorHandler` 把 `topic/partition/offset/key/groupId/error` 写进一张自建的 `kafka_message_log` 数据库表。

**替代方案与取舍**:标准做法是配一个 Kafka DLQ topic,失败消息发到那,由专门的消费者或人工重放。这里选的是"写关系型数据库表",代价是失败记录脱离了 Kafka 的 offset/分区语义,好处是可以直接用 SQL 查询、按业务字段(而不是 offset)检索失败原因,并且天然支撑第(3)点的应用层重放机制——这是一个"用自己已经很熟悉的存储(PostgreSQL)替代 Kafka 原生机制"的真实取舍,不是教科书最优解,但工程上够用。

**(2) 消费侧幂等:靠数据库存在性检查,不是 Kafka 事务**

`TransactionEventConsumer.save()` 在批量插入前先查 `transactionRepository.findExistingTransactionIdsInBatches(txnIds)`,过滤掉已经存在的 `publicId`,再 `saveAll`;如果并发场景下还是撞了唯一约束(`DataIntegrityViolationException`),退化成逐行插入、单行冲突就跳过并打点计数(`status=skipped, error=transaction already received`)。

这是第 1.3 节讲的"业务层幂等"的具体落地:**这套系统的消费端是 at-least-once(自动提交、批量处理、允许重复投递),幂等性完全靠下游存储的唯一键 + 存在性检查来兜底,而不是依赖 Kafka 的幂等生产者或事务**。生产端(`BTFeeProducer` / `EventProducer.sendAndFlush`)同样没有配置 `enable.idempotence` 或 `transactional.id`,只有 `ProducerConfig.RETRIES_CONFIG = 10`——也就是说,这套系统里 Kafka 的"exactly-once"能力(幂等生产者/事务,见 [[eos.idempotent-producer]] · [[eos.transactions]])**在生产代码里实际上没有被启用**,真正的正确性保证在应用层。这一点在面试里比"我们用了 Kafka 事务"更值得讲——因为它诚实地展示了"知道这个 feature 存在、也知道为什么这里选择不用"。

**(3) 应用层的 seek-and-replay 工具,而非 consumer.seek() 的临时脚本**

`pricing` 有一套专门的重放框架(`pricing/src/main/kotlin/com/braintree/pricing/events/replay/`):抽象基类 `Consumer<K,V>` 定义了 `replayMessageListener(startingOffset, endingOffset, offsetsToProcess, ...)`,配合一个 `Coordinator` 和命令行入口 `KafkaReplayJob`。用法是传 `consumer_group_id` + `days_lookback`(按时间窗口重放某个 group 过去 N 天该处理但需要重跑的消息),或者更精确地传 `partition + min_offset + max_offset` 定点重放一段 offset 区间。它的实现方式是绑定一个只处理指定 offset 区间的 `MessageListener`,逐条调用对应 consumer 的 `consume()`,并在 `kafka_message_log` 表里把重放过的消息标记 `processed = true`。

**为什么不直接用 `KafkaConsumer.seek(topicPartition, offset)` 写一次性脚本**:因为这套框架要处理的是"生产环境里某个具体 group 在某个时间窗口/offset 区间出过问题,需要精确重放,同时不能影响该 group 当前正常消费的位点"——每个 consumer 的重放走独立的 container/factory,不与生产消费者共享 offset 提交,靠 `kafka_message_log` 表(而不是 Kafka 自己的 `__consumer_offsets`)记录"这段区间哪些消息已经重放成功过",这样重放操作本身也是幂等的、可以安全地重复执行。

### 2.3 我做的部分 `[me]`

我在 `pricing` 仓库里的贡献止步于**4 个 2024 实习期 PR**,pricing 不是我的主战场领域(全仓库贡献者排名约第 30),上面 2.1/2.2 描述的 consumer/replay 框架是团队既有代码,不是我设计的。

我在 Kafka 这个技术上真正有实据的贡献,是在**Snowglobe 侧作为 Funding→Snowflake CDC 管道的下游消费者和使用者**:第一节讲的 Amex GRRCN 摄入管道(`STAGE_AMEX_GRRCN_FILE` → append-only stream → 6 个 processor procedure,详见 `03-snowflake-warehouse.md` §2.2)虽然物理上是 S3 文件摄入而非直接消费 Kafka topic,但下游的 stream/task 消费模式与 `modules/cdc/main.tf` 里 Funding CDC 管道的落地表消费模式是同构的——我在 Quality-Check/Trigger-Status 框架(见 `03-snowflake-warehouse.md` §2.2)里设计的"配置驱动 + 幂等 MERGE"模式,直接服务于这些 CDC 落地表的下游正确性校验。

**没做过、不装懂的部分**:没有写过 Kafka Producer/Consumer 的 JVM 代码上生产、没有调过 `pricing` 服务里任何一个 `KafkaListener` 的并发度或 backoff 策略、没有运维过 Kafka broker 或 Kafka Connect worker。这些如果被追问细节,我会直接说清楚,见第 5 节。

---

## 3. stripe kit 考到的点

Stripe 的机考/系统设计题里,Kafka 的知识很少被直接考"你说说 Kafka 架构",而是**藏在题目的约束里**——一道看起来是普通 CRUD/状态机的题,加一句"上游可能重复投递事件"或"处理失败需要允许安全重试",本质就是在考"消息层面不保证恰好一次、你怎么在业务逻辑里补上幂等性"这件事。

- [[s10-event-stream-reversal|S10 事件流与撤销/冲正]]:题目建模一个只能追加、不能修改历史记录的事件流,用"冲正事件(reversal event)"而不是原地修改来撤销之前的操作——这正是 Kafka 日志"仅追加、不可变"这个核心抽象在业务建模层面的直接映照,和第 1.2 节讲的"为什么是日志而不是可变状态"是同一个道理。
- [[s11-idempotency-dedup|S11 幂等 / 去重]]:直接对应第 2.2 节"消费侧幂等靠数据库存在性检查"的真实做法——用一个唯一键(idempotency key / 业务主键)去重,是"at-least-once + 应用层幂等"这套组合拳在代码层面的具体实现,面试现场写代码时可以直接复用这个思路(先查是否已处理,再写,写入操作本身也要考虑并发下的唯一约束兜底)。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| Kafka 怎么保证消息不丢? | Producer 端 `acks=all` 等 ISR 全部确认;Broker 端多副本 + 足够的 `min.insync.replicas`;Consumer 端处理成功后再提交 offset(而不是先提交再处理) | 结合 1.2 节 ISR 的定义解释"all"到底指哪些副本 |
| 你们系统里 Kafka 是恰好一次吗? | 不是——是 at-least-once(自动提交)+ 应用层幂等(DB 唯一键存在性检查),生产端也没开幂等生产者/事务 | 2.2 节的 `findExistingTransactionIdsInBatches` 具体代码路径,以及"为什么这里没用 Kafka 事务" |
| 消费者挂了怎么办,消息会丢吗? | 自动提交模式下,已提交但未真正处理完的消息理论上可能在特定时序下"看起来丢了"(下一次从已提交 offset 之后开始读) | 这正是第 1.3 节"at-least-once vs at-most-once"权衡的真实体现——自动提交 + 短提交间隔(100ms)让这套系统更偏 at-most-once 一端,依赖幂等消费兜底是不够的,真正防丢靠的是上游系统的重试和这套系统自己的对账/健康检查(见 03 文章里的 trigger-status 框架) |
| 如果某个 topic 的消费突然落后很多怎么排查? | 先看是消费能力不足(并发度、单条处理耗时)还是生产端突增(比如上游重放了历史数据);pricing 这边并发度是配置项(`concurrency`),可以临时调大;监控上要能看到 lag 随时间的曲线而不只是瞬时值 | 【未验证:pricing/snowglobe 生产环境具体用什么监控 Kafka consumer lag——Sentry/Datadog 确认在用于应用层错误和指标,但 lag 监控的具体 dashboard/告警规则未在本地材料中核实到,面试如被细问需要如实说"这部分我没有直接的一手经验"】 |
| **(第三层追问)** 如果分区数不够、消费能力已经拉满还是追不上,你怎么办? | 短期加分区没用(现有 consumer 数已经等于或超过分区数时,加 consumer 不会提速);要么增加分区数(伴随重新分配、可能打乱分区内顺序假设)、要么优化单条处理耗时、要么把处理拆成"快速确认收到 + 异步慢处理"两阶段 | 这里的陷阱是"加机器"不总是有效——Kafka 的并行度上限就是分区数,面试官很爱在这里追问"那你怎么知道该加多少分区" |
| **(第三层追问)** 你们的重放工具(`KafkaReplayJob`)会不会重复处理导致数据错乱? | 不会,因为下游写入本身是幂等的(唯一键 + MERGE/存在性检查),重放只是"再触发一次已经具备幂等性的写入路径",而不是假设"重放=安全"这件事本身天然成立 | 这正是"幂等消费"设计的意义所在——它不只是防生产环境的重复投递,也让"人工重放历史数据"这种高风险操作变得低风险,是同一套机制的两个应用场景 |

---

## 5. 我的边界

**边界一:没有运维过 Kafka broker/集群**。我没有做过分区扩容、副本数调整、ISR 相关的故障排查、Kafka Connect worker 集群本身的部署或调优。
**我怎么说**:"我的 Kafka 经验是应用层的生产/消费和管道下游消费,broker 运维这块我没有一手经验,这通常是平台/基础设施团队的职责范围。"
**接到哪去**:能接到我确实做过的——Quality-Check/Trigger-Status 这套配置驱动的下游正确性校验框架(见 03 文章 §2.2),是"消费方如何在不控制上游/broker 的前提下,依然把数据正确性这件事做扎实"的真实案例。

**边界二:没有在生产代码里配置过 Kafka 事务或幂等生产者**。虽然我在第 1.3/2.2 节能讲清楚 `eos.idempotent-producer`/`eos.transactions` 的原理,但这套系统的生产代码实际选择的是"at-least-once + 应用层幂等",我没有亲手调试过一个真正开启了 Kafka 事务的 consume-transform-produce 流程。
**我怎么说**:"这套系统的正确性保证选择放在应用层——数据库唯一键和存在性检查,而不是 Kafka 事务,这是我能讲清楚原理但没有一手调试经验的部分。"
**接到哪去**:接到"为什么这个选择是合理的"——Kafka 事务有明确的吞吐代价(见 [[eos.transactions-perf]]),而这套系统的写入路径本来就要落到一个支持唯一约束的关系型/列式存储,应用层幂等的边际成本几乎是零,不需要为了"理论上更强的保证"多引入一层分布式事务协调的复杂度。

**边界三:没有做过 Kafka Streams / ksqlDB 这类流处理框架的开发**。我们的"流处理"全部是"consumer 消费 + 存库 + 下游 SQL(存储过程/task)"这种更朴素的模式,没有用过带状态的流处理拓扑、窗口聚合这些 Kafka Streams 的能力。
**我怎么说**:"我们的流处理需求相对简单——收事件、落库、按业务规则算 fee,没有走到需要 Kafka Streams 这种有状态流处理框架的复杂度,这块我没有实际经验。"
**接到哪去**:接到 Snowflake 里等价的能力——Snowglobe 用 Stream + Task(Snowflake 原生的 CDC + 增量处理机制)在 SQL 层实现了类似"消费变化、增量处理"的效果,只是发生在数据仓库而不是消息中间件里,详见 03 文章。

**边界四:没有做过 Kafka 消费延迟(lag)相关的监控大盘搭建**。第 4 节的追问表里已经标注,具体的 lag 监控实现细节我没有一手核实到。
**我怎么说**:"我知道 lag 监控该看什么(consumer 提交位点和分区最新 offset 的差值、随时间的趋势而非瞬时值),但这套系统具体的监控大盘是谁搭的、告警阈值怎么定的,我没有直接参与,不清楚细节。"
**接到哪去**:接到我确实核实过在用的可观测性工具——Sentry(638 处代码命中,覆盖 `pricing/build.gradle.kts`、整个 `pricing/oncall/` 运维文档)和 Datadog 两者并存,用于应用层错误捕获和指标,这是我能确认的部分。

---

## 6. 往深里看

- [[core.topics-partitions]]——想搞清楚"分区数怎么定、加分区会不会打乱顺序"这类问题时去读,是理解本文 §1.2/§4 的物理基础。
- [[core.offsets]]——想理解"offset 到底存在哪、谁在维护它"时去读,是理解 §2.2 幂等消费设计动机的前提。
- [[core.replication-isr]]——想搞清楚 `acks=all` 精确含义、ISR 收缩对可用性的影响时去读。
- [[consumer.groups-rebalance]]——想理解"多个消费者实例怎么分摊分区、扩容/重启时会发生什么"时去读,补 §2.1 里 `concurrency` 参数背后的机制。
- [[consumer.offset-commit]]——想深挖"自动提交 vs 手动提交、提交时机怎么选"时去读,直接对应 §2.2 里 `AUTO_COMMIT_INTERVAL_MS=100` 这个具体配置的取舍。
- [[consumer.seek-and-replay]]——想系统性理解"按时间戳查找位置、如何设计一个安全的重放工具"时去读,是 §2.2 `KafkaReplayJob` 设计动机的理论背景。
- [[eos.idempotent-producer]] · [[eos.transactions]]——想搞清楚"Kafka 真正能保证什么、这套系统为什么没用"时去读,直接支撑 §1.3 和 §5 边界二的论证。
- [[connect.pipeline-design]]——想理解"用 Kafka Connect 搬数据 vs 自己写消费者"该怎么选时去读,对应 §2.1 通路二的 Snowflake Kafka Connector 用法。
- [[monitoring.lag-e2e]]——想理解"lag 监控该看哪些指标、端到端监控和单点监控的区别"时去读,补 §5 边界四没讲透的部分。
- [[async.log]] · [[async.delivery.guarantees]] · [[async.delivery.exactly-once]]——system-design 域里更抽象的版本,想脱离 Kafka 具体实现、单纯从"异步系统设计"的角度重新理解这些权衡时去读。

本栈相关的 readings/drills/cards:`vault/domains/kafka/readings/`、`vault/domains/kafka/cards/`,以及练习入口见 `vault/domains/kafka/BUILD.md`。
