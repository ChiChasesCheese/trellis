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
  "eos.idempotent-producer": ["<id shown first>", "…"],
  "eos.transactions": ["<id shown first>", "…"],
  "eos.transactions-perf": ["<id shown first>", "…"]
}

## eos.idempotent-producer — 幂等生产者的工作原理与局限性
理解幂等生产者依靠生产者ID与序列号去重的机制，以及它仅保证单个生产者会话内单分区幂等的局限。
- `kafka-eos-idempotent-broker-failover-state-transfer` Q: 分区首领所在的 broker 崩溃、跟随者副本接任新首领后，新首领是怎么知道每个生产者「已经写到哪个序列号」的，从而能继续正确校验新收到的消息，不需要重新等待或出错？
  A: 首领每次收到新消息，都会把该生产者最近的序列号信息更新进内存里的「生产者状态」；跟随者副本在从首领复制消息的同时，也会同步更新自己内存里的这份状态。所以当跟随者被提升为新首领时，它内存里本来就有最新的序列号记录，可以无缝、无延迟地继续校验后续消息，不会误判乱序或漏检重复。如果旧首领后来又恢复上线，它重启后内存状态是空的
- `kafka-eos-idempotent-limit-app-level-duplicate-send` Q: 如果应用代码里因为一个 bug，对同一条业务消息调用了两次 `producer.send()`，幂等生产者能识别并去掉其中一条吗？为什么？
  A: 不能。幂等生产者的去重逻辑只针对「生产者内部因为网络/broker 错误而自动发起的重试」——同一次逻辑发送在底层因为没收到确认而重发，才会被识别为重复。而应用代码主动调用两次 `send()`，在生产者看来就是两条独立、需要各自处理的正常请求，生产者无法判断这两条内容相同的消息「原本应该是同一条」，因此不会去重。这也
- `kafka-eos-idempotent-limit-multiple-producer-instances` Q: 一个从文件目录读取数据、并把每行记录发送到 Kafka 的应用，不小心跑了两个实例，都在读取同一批文件并各自发送记录到 Kafka。开启幂等生产者能防止这种情况下出现的重复消息吗？
  A: 不能。幂等生产者的去重范围是「同一个 PID（生产者 ID）内部因重试导致的重复」，而这里是**两个不同的生产者实例**（各自有自己的 PID）分别独立地发送了内容相同的消息——从 Kafka 的角度看，这就是两条来自不同生产者、序列号也各自独立递增的正常消息，没有理由被判定为重复。要避免这种「多实例重复处理同一份数据
- `kafka-eos-idempotent-out-of-order-seq-error` Q: 启用幂等生产者后，如果 broker 期望收到序列号 3，却直接收到了序列号 27，broker 会返回什么错误？这个错误说明了什么潜在问题，值得怎么排查？
  A: broker 会返回「乱序（out of order）」错误；如果没有开启事务，这个错误可能被生产者忽略，生产者仍会继续正常运行。但这个现象本身通常意味着**序列号 3 到 26 之间的消息发生了丢失**——broker 既然从 2 跳到了 27，中间那些理应发生的写入并没有真正落到这个 broker 上。看到这类日志
- `kafka-eos-idempotent-pid-sequence-dedup` Q: 开启幂等生产者（`enable.idempotence=true`）之后，broker 是靠什么信息识别出「这条消息其实是刚才那条消息的重发」，从而拒绝写入重复数据的？
  A: 每条消息都会带上生产者在启动时申请到的**生产者 ID（PID）**和一个按序递增的**序列号**；PID + 序列号再加上目标主题和分区，就能唯一标识一条消息。broker 会为每个分区记住来自每个生产者的最近 5 条消息的序列号（生产者要把 `max.in.flight.requests`——同时未确认的在途请求数
- `kafka-eos-idempotent-producer-restart-blindspot` Q: 一个开启了幂等性（但没开事务）的生产者崩溃后被重启（或被一个新实例取代），继续发送在崩溃前可能已经发送成功的消息。幂等生产者这时候还能检测出重复吗？为什么？
  A: 检测不出来。只要没启用事务，生产者每次初始化都会重新申请一个**全新的 PID**，新生产者和旧生产者拥有不同的 PID，即使它们发送的是内容完全相同的消息，broker 也会把二者当成两个不同生产者发出的不同消息，不会去重。这也意味着，即便那个旧生产者其实并没有真的死掉、只是被挂起后又恢复了活动（俗称「僵尸」），它和

## eos.transactions — 事务：应用场景、隔离与实现原理
掌握事务如何跨多个分区实现原子写入、事务ID与隔离级别的作用，以及事务能解决与不能解决的问题。
- `kafka-eos-transactions-atomic-multipartition-write` Q: Kafka 事务用「原子多分区写入」来实现流式处理的精确一次性语义，具体指的是把哪两个原本独立的写入操作绑定成「要么都成功、要么都不成功」？为什么这样才能避免重复处理？
  A: 指的是「把处理结果写入输出主题」和「把消费偏移量写入内部的 `consumer_offsets` 主题」这两个写操作。正常情况下这是两次独立的写入，中间可能发生崩溃导致只完成一个（比如结果写了，偏移量没提交）；Kafka 事务把它们打包进同一个事务，只要事务成功提交，两者必定同时生效，只要事务中止或未提交，两者都不生效
- `kafka-eos-transactions-external-side-effects-not-covered` Q: 一个开启了精确一次性语义的流式处理应用，在处理消息的过程中还会调用外部 REST 接口、发送电子邮件，或者写文件。如果这次处理最终因为事务被中止而「回滚」，那封已经发出去的邮件、已经调用成功的 REST 请求会被撤销吗？
  A: 不会。Kafka 事务的原子性只覆盖「写入 Kafka 本身的记录」这一件事——包括处理结果和偏移量提交；它对调用外部系统产生的副作用（发邮件、调用 REST API、写本地文件等）完全没有约束力，也没有任何撤销机制。也就是说，即使事务因为某种原因被中止、相关 Kafka 写入全部作废，之前已经真实发生的外部副作用依然
- `kafka-eos-transactions-isolation-level-tradeoff` Q: 消费者的 `isolation.level` 参数在 `read_committed` 和默认的 `read_uncommitted` 之间怎么选？选 `read_committed` 会带来什么代价？
  A: `read_uncommitted`（默认）会把所有消息都返回给消费者，包括还在执行中、甚至最终会被中止的事务里的消息；`read_committed` 只返回已经成功提交的事务里的消息，以及所有非事务方式写入的消息，不会返回执行中或已中止事务的消息。要获得精确一次性保证，消费者必须配置成 `read_committe
- `kafka-eos-transactions-two-phase-commit-mechanism` Q: Kafka 事务在提交时是怎么保证「跨多个分区的写入」要么全部生效、要么全部作废的？如果**事务协调器**（负责这个事务提交流程的 broker）在只给部分分区写完提交标记后就崩溃了，会发生什么？
  A: Kafka 用一个内部主题 `__transaction_state` 记录事务日志，采用两阶段提交：先把「打算提交（或中止）这个事务」的**意图**写进事务日志——一旦这个意图被记录下来，最终结局就已经确定（要么提交、要么中止）；然后事务协调器再依次向这个事务涉及的**所有分区**写入「提交标记（commit mar
- `kafka-eos-transactions-why-needed-duplicates` Q: 在「消费—处理—生产」型流式处理应用（从 Kafka 读消息、处理后把结果写回 Kafka、再提交消费偏移量）里，即使生产者本身是幂等的，仍有两类场景会造成结果被重复写入：{{c1::应用把处理结果写入输出主题之后、还没来得及提交消费偏移量就崩溃——触发再均衡后新消费者会从上一次提交的偏移量重新读取并重新处理这批消息，导致同一批结果被写两次}}；{{c2::「僵尸」应用实例——它读到一批消息后被挂起或断连，心跳超时后分区被再均衡给了新实例并处理完毕，随后旧实例又恢复运行，在不知道自己已被替换的情况下继续把同一批消息的处理结果写出去}}。这两种情况都是「Kafka 事务」机制要解决的问题，而不是单靠幂等生产者能覆盖的。
- `kafka-eos-transactions-zombie-fencing-epoch` Q: 使用事务性生产者时，配置的 `transactional.id`（事务 ID，跨重启保持不变）是怎么配合 epoch（每次初始化递增的代数）来阻止「僵尸」实例（已经被判定死亡、但自己不知道、还在继续写数据的旧实例）写入重复结果的？
  A: 事务性生产者每次调用 `initTransactions()` 初始化时，broker 都会把这个 `transactional.id` 对应的 epoch 加一。之后凡是带着**同一个** `transactional.id` 但 epoch 比当前值小的发送、提交、中止请求，都会被 broker 拒绝并返回 `Pr

## eos.transactions-perf — 事务的性能开销
理解启用事务后在延迟和吞吐上引入的额外开销，以及如何权衡精确一次语义与性能。
- `kafka-eos-txn-perf-batch-amortizes-overhead` Q: 生产者使用事务时的额外开销，是按「每条消息」摊还是按「每个事务」摊的？这对「一个事务里应该塞多少条消息」这个选择有什么指导意义？
  A: 事务带来的额外开销（事务 ID 注册、分区加入事务的注册、提交请求、提交标记写入）本质上是按**每个事务**发生一次，与这个事务里装了多少条消息无关。因此，一个事务里包含的消息越多，这份固定开销被摊薄到每条消息头上的比例就越小，需要同步等待的次数（每个事务一次提交）相对总消息数也就越少，整体吞吐量反而更高。也就是说，想
- `kafka-eos-txn-perf-consumer-latency-not-throughput` Q: 在 `read_committed` 隔离级别下，事务给消费者带来的性能影响主要体现在**延迟**还是**吞吐量**上？为什么消费者不需要为「还没提交的事务消息」做额外的缓冲工作，也就不会拖慢它的吞吐？
  A: 主要体现在**延迟**上：消费者读取提交标记本身只有很小的开销，真正的影响是 `read_committed` 隔离级别下消费者读不到还未提交的事务消息，事务提交的时间间隔越长，消费者要等待才能看到这批消息，端到端延迟就越高。至于吞吐量，之所以基本不受影响，是因为 broker 一开始就不会把属于未提交事务的消息返回给
- `kafka-eos-txn-perf-producer-overhead-sources` Q: 启用事务的生产者，额外开销主要来自这几个环节：{{c1::事务 ID 注册——在生产者整个生命周期中只发生一次}}；{{c2::分区注册到事务——每个分区第一次加入某个事务时发生一次}}；{{c3::提交事务时的提交请求，以及事务协调器随后向该事务涉及的每个分区写入的一条额外「提交标记」消息}}。其中事务初始化请求和提交请求都是**同步**的：生产者必须等它们成功、失败或超时才能继续发送后续数据，这进一步拉高了开销。
- `kafka-eos-txn-perf-short-vs-long-transaction-tradeoff` Q: 在给流式处理应用设置「多久提交一次事务」时，选「事务开得短、提交得频繁」和「事务开得长、攒够更多消息再提交」，分别是把系统往哪个方向优化，牺牲的是什么？
  A: 事务开得短、提交频繁：因为消费者要等事务提交后才能读到里面的消息，提交越勤，消费者看到新数据的延迟就越低；但生产者这边事务 ID 注册、分区加入事务、提交请求与提交标记这些固定开销是按「每个事务」产生的，事务越小越频繁，这份固定开销被摊到的消息数就越少，相对开销升高，牺牲的是生产者侧的吞吐量。反过来，事务开得长、一次装
