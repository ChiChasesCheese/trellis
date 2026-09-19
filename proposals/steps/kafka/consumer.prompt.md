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
  "consumer.groups-rebalance": ["<id shown first>", "…"],
  "consumer.client-basics": ["<id shown first>", "…"],
  "consumer.poll-config": ["<id shown first>", "…"],
  …
}

## consumer.groups-rebalance — 消费者群组（consumer group）与再均衡（rebalance）
理解消费者群组如何分摊分区、再均衡的触发时机，以及再均衡监听器与群组固定成员（static membership）如何减少不必要的再均衡。
- `kafka-consumer-eager-vs-cooperative-rebalance` Q: 「主动再均衡」（eager rebalance）和「协作再均衡」（cooperative/incremental rebalance）在处理分区重新分配时有什么根本区别？为什么协作再均衡对大型消费者群组更友好？
  A: 主动再均衡要求所有消费者先放弃自己拥有的全部分区、重新加入群组，再统一获得新分配，整个群组在此期间完全停止消费（「停止世界」式停顿）。协作再均衡只把需要转移的那部分分区从原消费者手里收回、分配给别的消费者，其余消费者对未被重新分配的分区可以继续正常读取，不受影响。群组规模越大，一次完整的再均衡通常耗时越长，协作再均衡通
- `kafka-consumer-group-partition-sharing` Q: 一个主题有4个分区，消费者群组（consumer group，共同读取同一主题、分摊分区的一组消费者）里只有1个消费者时它读取全部4个分区；如果群组扩到5个消费者会发生什么？
  A: 群组里的消费者数量在不超过分区数时，Kafka 会把分区尽量均衡地分给各个消费者，比如4个消费者对4个分区时每人正好一个；但一旦消费者数量超过了分区数量（比如5个消费者对4个分区），多出来的消费者就分不到任何分区，会处于空闲状态、收不到任何消息，因为一个分区在同一时刻只能被群组内的一个消费者读取。
- `kafka-consumer-heartbeat-session-timeout-death-detection` Q: 消费者群组协调器（group coordinator，负责管理某个消费者群组成员关系的 broker）是靠什么机制判断一个消费者是否还「活着」，进而决定要不要触发再均衡？
  A: 消费者会通过一个后台线程持续向群组协调器发送心跳（heartbeat），只要按时发送心跳就被认为存活。如果消费者在足够长的时间内没有发心跳（比如进程崩溃、无法继续处理），它的会话就会超时，协调器判定它「死亡」并触发一次再均衡，把它原本负责的分区转移给群组里其他消费者；而如果消费者是被正常关闭的，它会主动通知协调器离开群
- `kafka-consumer-multiple-groups-full-data` Q: 如果两个不同的应用程序都需要读取同一个主题的全部消息，应该让它们共用一个消费者群组，还是各自使用独立的群组？
  A: 应该各自使用独立的消费者群组。同一个群组内的消费者是分摊分区、共享消息流的，一条消息只会被群组内一个消费者处理；而不同群组之间相互独立，各自都能收到主题的全部消息。所以只要给每个需要完整数据的应用程序分配自己专属的群组 ID，它们就能各自完整地读取整个主题、互不影响，即使群组内部又通过多个消费者来分摊负载也不影响这一点
- `kafka-consumer-rebalance-listener-commit-before-revoke` Q: 消费者即将因为再均衡而失去某个分区的所有权之前，为什么最好在 `onPartitionsRevoked()` 回调里主动提交偏移量，而不是等下一次常规的自动/手动提交？
  A: `onPartitionsRevoked()` 会在消费者真正放弃分区所有权之前被调用，这是提交该分区最后处理进度的最后机会：一旦所有权转移给了群组里的其他消费者，新的所有者会从上一次提交的偏移量开始读取。如果没有在放弃所有权之前及时提交，新消费者可能会从一个更旧的偏移量重新开始，导致部分消息被重复处理；因此把提交偏移
- `kafka-consumer-static-membership-avoids-rebalance` Q: 给消费者配置一个唯一的 `group.instance.id`，让它成为群组的「固定成员」（static membership），这样做能避免什么开销？什么场景下特别有用？
  A: 默认情况下消费者的群组成员身份是临时的，一旦离开群组（比如重启）就会失去原来的分区、重新加入时要走一次完整的再均衡流程重新分配分区。而固定成员被关闭后不会立即离开群组，只要在 `session.timeout.ms` 规定的时间内重新加入，就能拿回之前持有的原班分区，完全不触发再均衡。这对那些为分区维护了本地状态或缓存

## consumer.client-basics — 创建消费者、订阅与轮询循环
掌握消费者的创建、订阅主题、轮询（poll）循环的线程安全约束，以及如何优雅退出轮询。
- `kafka-consumer-graceful-shutdown-wakeup` Q: 消费者的轮询循环通常写成一个无限循环，要怎样才能从另一个线程安全地让它优雅退出？为什么不能直接从其他线程调用 `poll()` 之外的方法？
  A: 应该在另一个线程（比如关闭钩子 ShutdownHook）里调用 `consumer.wakeup()`——这是消费者唯一一个可以从其他线程安全调用的方法。调用它会让正在阻塞的（或者下一次调用的）`poll()` 抛出 `WakeupException`，主线程捕获这个异常后跳出循环，并调用 `consumer.clo
- `kafka-consumer-one-thread-per-consumer-rule` Q: 能不能在同一个线程里跑多个属于同一个消费者群组的 KafkaConsumer？能不能让多个线程共享同一个 KafkaConsumer 实例？
  A: 都不行。Kafka 消费者的使用规则是「一个消费者对应一个线程」：既不能在同一线程里同时运行多个属于同一群组的消费者，也不能保证多个线程安全地共享同一个消费者对象去并发调用它的方法。如果应用要在同一个消费者群组里跑多个消费者做并行处理，正确做法是把每个消费者的逻辑封装起来，各自独立运行在自己的线程中（比如用 Execu
- `kafka-consumer-poll-liveness-requirement` Q: 为什么消费者必须持续、频繁地调用 `poll()`，而不能只在有需要处理消息时才偶尔调一次？如果太久没调用会发生什么？
  A: `poll()` 不仅仅是拉取数据的接口，消费者靠不断调用它来向群组证明自己还「活跃」；如果超过 `max.poll.interval.ms` 没有调用 `poll()`，群组协调器会认为这个消费者已经「死亡」，把它负责的分区转移给群组里的其他消费者（触发再均衡）。所以轮询循环里不能有可能长时间阻塞的操作，否则即使消费
- `kafka-consumer-required-config` Q: 创建一个 KafkaConsumer 对象至少需要设置哪三个属性？另外一个虽非严格必须、但几乎总会用到的第四个属性是什么？
  A: 必须设置 `bootstrap.servers`（连接 Kafka 集群的地址列表，作用同生产者）、`key.deserializer` 和 `value.deserializer`（分别把字节数组还原成键和值的 Java 对象，与生产者的序列化器相对应）。此外，`group.id` 虽然严格来说不是必需的（也可以创建
- `kafka-consumer-subscribe-regex-tradeoff` Q: 用正则表达式（如 `test.*`）而不是明确的主题列表订阅主题，有什么好处？在包含大量分区的大集群上这样做又要付出什么代价？
  A: 用正则表达式订阅的好处是灵活：只要有新创建的主题名字匹配这个正则，消费者就会自动被纳入订阅、触发一次再均衡去读取它，适合读取多个主题或类型不确定数据的场景（比如跨系统复制数据、流式处理应用）。代价是主题过滤在客户端完成，消费者需要定期向 broker 请求所有已订阅主题及分区的元数据；如果集群分区数量巨大（比如三万个以

## consumer.poll-config — 拉取与存活相关配置
理解fetch.min.bytes、max.poll.records等拉取参数与session.timeout.ms、heartbeat.interval.ms等存活检测参数如何共同影响吞吐与故障检测速度。
- `kafka-consumer-auto-offset-reset-choices` Q: 消费者要读取一个没有已提交偏移量、或者偏移量已经因为长时间离线而失效的分区时，`auto.offset.reset` 的三个可选值 latest、earliest、none 分别会发生什么？
  A: `latest`（默认值）让消费者从这个分区里最新写入的位置开始读，也就是只处理消费者启动之后新产生的消息；`earliest` 让消费者从分区最开始的位置读起，会读到所有仍保留在分区里的历史消息；`none` 则完全不做自动处理，遇到无效偏移量直接抛出异常，把决定权交给应用程序自己处理。
- `kafka-consumer-fetch-max-bytes-vs-partition-fetch-bytes` Q: 要限制消费者一次 `poll()` 拉取数据占用的内存，为什么建议优先用 `fetch.max.bytes`（限制单次响应的总字节数）而不是 `max.partition.fetch.bytes`（限制每个分区返回的字节数）？
  A: 用 `max.partition.fetch.bytes` 控制内存会很麻烦，因为消费者没法预知 broker 这次响应里会包含多少个分区的数据——分区数一多，即使每个分区都不超限，总数据量依然可能很大，内存占用变得不可控。而 `fetch.max.bytes` 直接限制整个响应的总字节数，能更直接地限制消费者用于缓存
- `kafka-consumer-fetch-max-wait-ms-with-fetch-min-bytes` Q: 如果同时设置了 `fetch.min.bytes=1MB` 和 `fetch.max.wait.ms=100`，broker 在什么情况下会提前返回数据，而不是一直等到凑够1MB？
  A: 这两个参数是「哪个条件先满足就按哪个来」的关系：只要累计数据达到 `fetch.min.bytes` 指定的量（这里是1MB），broker 就会立刻返回；如果一直没攒够，最多等到 `fetch.max.wait.ms` 指定的时间（这里是100毫秒）后，也会把当前已有的数据（哪怕不到1MB）返回给消费者。这样 `fe
- `kafka-consumer-fetch-min-bytes-tradeoff` Q: `fetch.min.bytes`（默认1字节）指定 broker 要凑够多少数据才把响应返回给消费者的拉取请求。把它调大对吞吐量和延迟分别有什么影响？
  A: 把 `fetch.min.bytes` 调大，会让 broker 在主题流量不大时等到攒够足够多的数据才响应，减少了消费者和 broker 之间来回传输的次数，从而降低双方的 CPU 和网络负载，适合流量高峰期或消费者数量很多、想给 broker 减负的场景。代价是在低吞吐量时段，消费者要多等一会儿才能拿到数据，读取延
- `kafka-consumer-max-poll-interval-ms-purpose` Q: 消费者的心跳是由一个后台线程发送的，即使主线程卡在处理某条消息的死循环或死锁里，后台线程也可能继续正常发心跳。这种情况下，Kafka 是靠什么参数发现这个消费者其实已经不干活了？
  A: 靠 `max.poll.interval.ms`（默认5分钟）。这个参数限制了消费者两次调用 `poll()` 之间最多能间隔多久；如果主线程长时间被卡住、迟迟不再调用 `poll()`，即使心跳仍在正常发送，超过这个阈值后台线程也会主动向 broker 发送「离开群组」的请求并停止发心跳，让协调器把这个消费者标记为死
- `kafka-consumer-session-timeout-heartbeat-interval-ratio` Q: `session.timeout.ms`（消费者可以多久不发心跳仍被认为存活，默认10秒）和 `heartbeat.interval.ms`（消费者发送心跳的频率）之间通常应该保持什么比例关系？把 `session.timeout.ms` 调小或调大分别有什么后果？
  A: 通常把 `heartbeat.interval.ms` 设置为 `session.timeout.ms` 的三分之一左右（例如会话超时3秒、心跳间隔1秒），这样在真正超时之前至少能有几次心跳发送机会，避免网络抖动导致误判。把 `session.timeout.ms` 设置得比默认值小，可以更快检测到消费者崩溃并把它的分

## consumer.offset-commit — 提交与偏移量管理
掌握自动提交与手动同步/异步提交组合的权衡，以及如何提交特定偏移量。
- `kafka-consumer-auto-commit-duplicate-window` Q: 把 `enable.auto.commit` 设为 true（默认值）后，消费者每隔 `auto.commit.interval.ms`（默认5秒）自动提交一次偏移量。如果消费者在两次自动提交之间的第3秒崩溃，会发生什么？调小提交间隔能不能彻底避免这个问题？
  A: 接管这个分区的新消费者会从最后一次自动提交的偏移量开始读取，但那个偏移量已经落后了大约3秒，所以这3秒内处理过的消息会被重新读取一遍、重复处理。调小 `auto.commit.interval.ms` 能缩短这个「重复处理窗口」的长度，但没办法彻底消除，因为提交本身仍然是按固定时间间隔进行的，而不是每处理一条就提交一次
- `kafka-consumer-commit-async-then-sync-on-shutdown` Q: 为什么消费者关闭之前，通常建议在循环体内一直用 `commitAsync()` 提交，但在真正退出循环、关闭消费者之前额外调用一次 `commitSync()`？
  A: 循环体内偶尔一次 `commitAsync()` 提交失败通常不是大问题，因为很快就会有下一次提交把偏移量追上来；但如果这是消费者关闭前的最后一次提交，就没有「下一次」去补救了，一旦这次失败，进度就真丢了。所以在退出循环前额外调用一次 `commitSync()`，利用它会持续重试直到成功或遇到不可恢复错误的特性，确保
- `kafka-consumer-commit-offset-duplicate-vs-loss` Q: 如果最后一次提交的偏移量小于消费者实际处理到的位置，会有什么后果？如果提交的偏移量反而大于实际处理到的位置呢？
  A: 如果提交的偏移量偏小（落后于实际处理进度），一旦发生再均衡、由新消费者接管这个分区，它会从这个偏小的偏移量重新开始读取，导致两个偏移量之间的消息被重复处理。反过来，如果提交的偏移量偏大（超前于实际处理进度，比如消息还没处理完就提交了），新消费者会跳过这段还没被真正处理过的消息，造成消息丢失。这就是为什么「提交哪个偏移量
- `kafka-consumer-commit-specific-offset-mid-batch` Q: `poll()` 一次可能返回一大批消息，如果只在处理完整批消息后才调用 `commitSync()`/`commitAsync()`（它们只会提交这批消息里的最后一个偏移量），万一处理到一半发生再均衡，重复处理的消息范围会有多大？有什么办法缩小这个范围？
  A: 如果只在处理完整批之后才提交，一旦处理到中途发生再均衡，新的所有者会从上一批提交的偏移量开始读，导致这一整批已经处理过一部分的消息全部要重新处理一遍，重复范围等于整批数据。为了缩小这个范围，可以在批次处理过程中，针对某个具体分区调用带参数的 `commitSync(offsets)` / `commitAsync(of
- `kafka-consumer-commitsync-vs-commitasync` Q: `commitSync()` 和 `commitAsync()` 都能手动提交偏移量，二者最主要的区别是什么？为什么 `commitAsync()` 遇到提交失败时不会像 `commitSync()` 那样自动重试？
  A: `commitSync()` 会阻塞，直到 broker 确认提交成功或者抛出异常，如果失败就持续重试，可靠但限制吞吐量；`commitAsync()` 发出提交请求后立刻返回、不等待响应，吞吐量更高，但失败时默认不重试。不重试的原因是：如果一次异步提交（比如偏移量2000）因为网络问题延迟到达，而在这期间又有一次更晚
- `kafka-consumer-offset-commit-meaning` Q: Kafka 不像传统的 JMS 队列那样要求消费者对每条消息单独发送确认（ACK）。Kafka 消费者是靠什么机制来记录「已经处理到哪里了」？「提交偏移量」具体提交的是什么？
  A: Kafka 消费者靠更新自己在每个分区读取位置的「偏移量」来追踪消费进度，这个动作叫偏移量提交，做法是向 Kafka 内部的 `__consumer_offsets` 主题写入一条包含分区和偏移量的消息。提交并不是逐条确认，而是提交「已成功处理的最后一条消息」的偏移量（严格说是它的下一个位置），并假定这条消息之前的所有

## consumer.seek-and-replay — 定位读取位置：seek、按时间戳查找与重放（replay）
掌握用 seekToBeginning/seekToEnd、offsetsForTimes 与 seek() 把消费者跳到任意偏移量，用于重放历史、跳过积压或按时间点恢复。
- `kafka-consumer-offsetsfortimes-seek-mechanism` Q: 如果想让消费者从「一小时前」这个时间点开始重新读取消息，而不是跳到某个具体的偏移量数字，应该怎么做？
  A: 先用 `consumer.offsetsForTimes(...)` 方法，给它一个「分区 → 目标时间戳」的映射（比如把每个已分配给该消费者的分区都映射到一小时前的时间戳），这个调用会向 broker 发请求，换回每个分区里对应这个时间点附近的偏移量（`OffsetAndTimestamp`）；然后对每个分区调用 `
- `kafka-consumer-seek-changes-poll-position-not-commit` Q: 调用 `consumer.seek(partition, offset)` 之后，下一次调用 `poll()` 会从哪里开始读取？这个操作本身会不会顺带把这个新位置提交到 Kafka？
  A: `seek()` 只是修改了消费者在内存里对这个分区「下一次要读取的位置」，之后紧接着的 `poll()` 就会从这个新设置的偏移量开始返回消息。但 `seek()` 本身并不会自动提交偏移量——是否要把这个新位置持久化为已提交偏移量，仍然需要应用程序自己显式调用提交方法，否则一旦发生再均衡或消费者重启，进度又会退回到
- `kafka-consumer-seek-use-cases` Q: 除了单纯「回放全部历史」，`seek()` 这类定位偏移量的 API 还能解决哪两类实际问题？
  A: 一是对处理延迟敏感的应用，如果发现自己已经落后太多、来不及追上最新数据，可以主动向前跳过一部分积压消息，放弃过时的数据以保证时效性；二是当消费者原本用来保存处理结果的下游系统（比如某个输出文件）意外丢失或损坏时，可以把消费者的偏移量重置回更早的位置，重新读取那段区间的消息来恢复丢失的数据。
- `kafka-consumer-seektobeginning-seektoend-purpose` Q: 如果想让消费者跳过所有历史积压消息、只读之后新产生的数据，或者反过来想重新处理某个分区从头到尾的全部历史消息，应该调用哪两个 API？
  A: 调用 `consumer.seekToEnd(partitions)` 可以把消费者在指定分区上的读取位置直接跳到分区末尾，之后 `poll()` 就只会返回跳转之后新写入的消息，用于跳过大量积压数据；调用 `consumer.seekToBeginning(partitions)` 则会把位置重置到分区起始处，让消费

## consumer.deserialization — 反序列化器与Avro反序列化
掌握自定义反序列化器的实现，以及在消费者中使用Avro反序列化记录的做法。
- `kafka-consumer-avro-deserializer-early-error-detection` Q: 使用 Avro 加模式注册表（schema registry）来做序列化和反序列化，相比自定义反序列化器，在「排查兼容性错误」这件事上有什么明显优势？
  A: AvroSerializer 在生产者写入时就会保证数据与主题的模式兼容，消费者这边任何因为模式不兼容而产生的错误，都会被 Avro 相关的序列化/反序列化组件直接捕获，并附带描述性的错误信息；这样开发者不需要像使用自定义反序列化器那样，在出问题时去逐字节比对、费力调试原始字节数组，问题能更早、更清楚地被发现。
- `kafka-consumer-avro-specific-reader-config` Q: 消费者用 `KafkaAvroDeserializer` 反序列化 Avro 消息时，配置 `specific.avro.reader=true` 起什么作用？
  A: 它告诉反序列化器把消息还原成代码生成工具预先生成的「专用」Avro 类实例（比如带有 getName()、getID() 这类方法的 Customer 类），而不是还原成通用的 GenericRecord（类似 map 的通用容器）。这样消费者代码就能用生成类的强类型访问方式来读取字段，而不用像操作 GenericRe
- `kafka-consumer-custom-deserializer-tight-coupling` Q: 为什么不建议使用自定义反序列化器（custom deserializer），即使它的写法并不复杂？
  A: 自定义反序列化器要求消费者端使用和生产者端完全对应的类定义和字节布局逻辑（比如同一个 Customer 类），一旦生产者那边修改了对象结构，所有使用自定义反序列化器的消费者代码都要跟着同步修改，这把生产者和消费者紧紧耦合在一起，在有多个团队共享同一份数据的大企业里很容易出错、难以协调。推荐改用 JSON、Thrift、
- `kafka-consumer-serializer-deserializer-must-match` Q: 生产者用 `IntSerializer` 把消息值序列化成字节数组，如果消费者用 `StringDeserializer` 去反序列化，会发生什么？为什么反序列化器必须和当初的序列化器相对应？
  A: 会出错甚至得到无意义的结果，因为字节数组本身没有自描述能力，反序列化器只是按照约定好的编码方式去解析这些字节；如果解析方式和写入时用的编码方式不一致（比如整型的字节布局被当成字符串来解析），得到的 Java 对象要么解析失败抛异常，要么是一堆没有意义的乱码。所以开发者必须清楚知道某个主题里的消息是用哪种序列化器写入的，

## consumer.standalone — 独立消费者：脱离消费者群组的场景
理解何时以及如何使用不属于任何消费者群组的独立消费者。
- `kafka-consumer-assign-vs-subscribe-exclusive` Q: 消费者可以调用 `subscribe()` 订阅主题（从而加入消费者群组），也可以调用 `assign()` 给自己直接指定要读取的分区。这两种方式能不能同时使用？
  A: 不能。一个消费者要么通过 `subscribe()` 订阅主题、加入消费者群组，让 Kafka 自动分配分区并在群组变化时触发再均衡；要么通过 `assign()` 自己明确指定要读取哪些分区，完全跳过订阅和群组机制。二者是互斥的，只能选其中一种方式来确定消费者要读取的分区。
- `kafka-consumer-standalone-new-partitions-blind-spot` Q: 使用 `assign()` 给独立消费者指定分区之后，如果这个主题后来被管理员增加了新分区，消费者会自动感知并开始读取新分区吗？需要怎么处理？
  A: 不会自动感知。独立消费者用 `assign()` 手动指定的分区列表是固定的，Kafka 不会像消费者群组那样在主题变化时主动通知它、触发重新分配。要跟上新增的分区，需要应用程序自己定期调用 `consumer.partitionsFor()` 检查是否有新分区出现，或者干脆约定每次给主题加分区之后就重启一次这个独立消
- `kafka-consumer-standalone-still-needs-group-id` Q: 使用独立消费者（不调用 `subscribe()`）时，还需不需要配置 `group.id`？为什么？
  A: 仍然需要配置 `group.id`。虽然不调用 `subscribe()` 就不会让这个消费者加入任何消费者群组、也不会经历再均衡，但提交偏移量（比如调用 `commitSync()`）时依然要归属到某个群组 ID 下保存进度，所以 `group.id` 这个配置项还是必须设置的，只是它不再用于分区分配和再均衡。
- `kafka-consumer-standalone-when-to-use` Q: 什么情况下适合让一个消费者不加入任何消费者群组、以「独立消费者」（standalone consumer）的方式直接读取某个主题的全部或部分分区，而不是走消费者群组和再均衡那一套机制？
  A: 当只需要用单独一个消费者读取某个主题的全部分区、或者读取某几个已经明确知道的固定分区时，就不需要消费者群组自动分配分区、自动再均衡这些机制带来的复杂性——只要把这些分区直接分配给这个消费者，让它开始读取消息并适时提交偏移量即可，做法更简单直接。
