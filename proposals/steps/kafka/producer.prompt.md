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
  "producer.client-basics": ["<id shown first>", "…"],
  "producer.acks-durability": ["<id shown first>", "…"],
  "producer.batching-throughput": ["<id shown first>", "…"],
  …
}

## producer.client-basics — 创建生产者与同步/异步发送
掌握生产者的创建方式，以及同步发送与异步发送（含回调）在延迟和吞吐上的取舍。
- `kafka-producer-bootstrap-servers-multiple-hosts` Q: 配置 `bootstrap.servers` 时，为什么建议至少填两个 broker 地址，而不是只填一个？
  A: `bootstrap.servers` 只是生产者用来建立到 Kafka 集群的初始连接的入口，一旦连上，生产者就能从这个 broker 那里获取到集群中其他 broker 的信息，并不需要在这里列出全部 broker。但如果只配置了一个地址而这台 broker 恰好停机，生产者就完全无法建立初始连接；配置至少两个地址
- `kafka-producer-callback-ordering-and-blocking` Q: 使用异步发送并传入回调（callback）时，如果连续向同一个分区发送了两条消息，它们的回调会按什么顺序执行？回调函数里能不能做耗时的阻塞操作？
  A: 回调在生产者的主线程里执行，如果两条消息被发往同一个分区，它们的回调会按照发送的先后顺序被依次调用。正因为回调运行在这条关键线程上，回调本身必须执行得快，不应该包含阻塞操作（比如同步 I/O）——否则会拖慢生产者处理后续消息的速度，阻塞操作应该被放到其他线程去做。
- `kafka-producer-required-config-three-props` Q: 创建一个 Kafka 生产者（producer，向 Kafka 写入消息的客户端）对象时，有哪三个属性是必须设置的？各自的作用是什么？
  A: 必须设置：`bootstrap.servers`（一组 broker 的 host:port 地址，用于建立到集群的初始连接）、`key.serializer`（把消息的键序列化成字节数组的类）、`value.serializer`（把消息的值序列化成字节数组的类）。之所以键和值的序列化器都要配置，是因为 broker
- `kafka-producer-sync-send-throughput-problem` Q: 为什么说同步发送方式「通常不会被用在生产环境中」？
  A: 因为同步发送要求发送线程在每次调用 send().get() 后一直阻塞，直到 broker 返回响应为止；根据集群繁忙程度，一次响应可能要等 2 毫秒甚至更久。在这段等待时间里，线程什么也做不了，甚至不能去发送下一条消息，这会严重拖累整体发送吞吐量，所以同步发送常见于示例代码，而不是生产环境。
- `kafka-producer-three-send-modes` Q: Kafka 生产者发送一条消息有三种方式：发送并忘记、同步发送、异步发送。它们在「是否知道发送结果」和「性能」上分别是什么权衡？
  A: 「发送并忘记」调用 send() 后不处理返回值，性能最好，但如果发生不可重试的错误或超时，消息会悄悄丢失且应用毫无感知；「同步发送」对 send() 返回的 Future 调用 get() 阻塞等待结果，能确定每条消息是否成功，但发送线程在等待期间什么也做不了，吞吐量差；「异步发送」调用 send() 时传入回调（c

## producer.acks-durability — acks与生产端持久性保证
理解acks=0/1/all如何决定消息在被确认前需要写入多少副本，以及由此带来的持久性保证差异。
- `kafka-producer-acks-0-fire-and-forget-risk` Q: 生产者把 `acks` 设置为 0 会带来什么效果？为什么这个设置吞吐量最高，但风险也最大？
  A: `acks=0` 表示生产者发送消息后完全不等待 broker（Kafka 服务器节点）的任何响应就认为发送完成。因为不需要等待网络往返，生产者可以以网络能支持的最快速度连续发送消息，吞吐量最高；但代价是如果 broker 没收到消息（比如网络问题、broker 故障），生产者完全不会知道，消息就这样悄悄丢失了，没有任
- `kafka-producer-acks-1-leader-crash-risk` Q: 生产者把 `acks` 设置为 1 时，消息在什么条件下算「写入成功」？这个设置下消息还有可能丢失吗？
  A: `acks=1` 时，只要分区的首领副本（leader replica）收到消息，broker 就会告诉生产者写入成功，不需要等待跟随者副本（follower replica）完成复制。这比 acks=0 更安全，因为首领没收到消息时生产者会收到错误并重试；但如果首领刚确认收到消息就立刻崩溃，而消息还没来得及被复制到任
- `kafka-producer-acks-all-isr-safety` Q: 生产者把 `acks` 设置为 all，一条消息在什么条件下才会被判定为「写入成功」？为什么这比 acks=1 更能防止丢消息？
  A: acks=all 要求分区的所有同步副本（ISR，in-sync replicas，与首领保持同步的副本集合）都确认收到消息之后，生产者才会收到写入成功的响应。这样即使首领随后崩溃，新选出的首领也一定是 ISR 里已经拥有这条消息的某个副本，不会丢失数据；而 acks=1 只要求首领收到，一旦首领确认后立刻崩溃且消息还
- `kafka-producer-acks-end-to-end-latency-same` Q: 既然 acks 的值越小生产者延迟越低，那么把 acks 调低是不是也能降低消息「从生成到消费者可以读到」的端到端延迟？
  A: 不会。不管 acks 设置成 0、1 还是 all，端到端延迟（从消息产生到消费者可以读取它）是一样的，因为 Kafka 为了保证一致性，只允许消费者读取已经被写入所有同步副本的消息，这个限制与生产者的 acks 设置无关。所以如果关心的是端到端延迟而不是生产者自己发送时的等待时间，就没有必要为了追求低延迟而牺牲可靠性
- `kafka-producer-acks-speed-vs-durability-tradeoff` Q: 从 acks=0 到 acks=1 再到 acks=all，生产者发送消息的「速度」和「可靠性」之间存在什么规律？
  A: acks 的值设得越小，生产者不用等待越多的确认，发送速度（生产者视角的延迟）就越快，但可靠性越低：acks=0 完全不等待、可能悄悄丢消息，acks=1 只等首领、首领崩溃时仍可能丢消息，acks=all 等所有同步副本确认、最安全但因为要等更多网络往返而生产者延迟最高。也就是说这三档配置是用可靠性换取生产者延迟的权

## producer.batching-throughput — 批处理、linger.ms与压缩（compression）对吞吐量的影响
掌握batch.size、linger.ms、buffer.memory与compression.type如何联合影响生产者吞吐量与延迟。
- `kafka-producer-batch-size-bytes-not-full-required` Q: `batch.size` 参数是按消息条数计算的吗？把它设置得很大，是不是意味着生产者会等到批次被填满才发送，从而增加延迟？
  A: 不是。`batch.size` 是按字节数（而不是消息条数）限制一个批次能使用的内存大小。批次填满时会被整体发送，但生产者并不要求批次必须填满才发送——未填满、甚至只有一条消息的批次也可能被发出去。因此把 `batch.size` 设置得很大本身不会增加延迟，只是会多占用一些内存；但如果设置得太小，生产者需要更频繁地发
- `kafka-producer-batching-config-interaction` Q: `batch.size`、`linger.ms`、`buffer.memory`、`compression.type` 这四个参数是如何共同影响生产者吞吐量的？
  A: `batch.size` 和 `linger.ms` 共同决定一个批次何时被发送——批次达到 `batch.size` 字节数或等待时间达到 `linger.ms`，哪个先满足就触发发送；批次越大、等待时间越长，单条消息的网络开销越低，吞吐量越高，但延迟也随之增加。`buffer.memory` 决定生产者在消息发出之
- `kafka-producer-buffer-memory-backpressure` Q: 如果应用程序调用 `send()` 的速度超过了生产者把消息发给 broker 的速度，生产者内部的发送缓冲区（由 `buffer.memory` 控制大小）会发生什么？
  A: 生产者的内存缓冲区可能会被耗尽，此时后续的 `send()` 调用会被阻塞，等待有内存被释放出来；如果等待时间超过了 `max.block.ms`，就会抛出异常。需要注意，这个异常是从 `send()` 方法本身直接抛出的，而不是像发送失败那样通过返回的 Future 对象抛出。
- `kafka-producer-compression-snappy-vs-gzip` Q: `compression.type` 可选 snappy、gzip、lz4、zstd 等压缩算法。在「CPU 开销」和「压缩率」上，snappy 和 gzip 分别适合什么场景？
  A: snappy 占用较少的 CPU 时间，同时能提供不错的性能和压缩比，适合同时关心性能和网络带宽的场景；gzip 通常占用更多 CPU 时间，但压缩比更高，适合网络带宽比较紧张、更需要省流量的场景。压缩能降低网络传输和存储的开销，而这往往是发送消息时的瓶颈所在，默认情况下 Kafka 不压缩消息。
- `kafka-producer-linger-ms-latency-throughput` Q: 默认情况下（linger.ms=0），生产者只要有可用的发送线程，即使批次里只有一条消息也会立刻发送出去。把 `linger.ms` 调大会带来什么效果？
  A: `linger.ms` 指定生产者在发送一个消息批次之前，愿意再多等待多长时间以便让更多消息加入这个批次。把它设置成大于 0 的值，会让批次里能装进更多消息，从而降低单位消息的网络和处理开销（如果启用了压缩，压缩效果也更好），显著提升吞吐量；代价是每条消息都要多等这么一段时间才被发出去，牺牲了一点延迟。

## producer.timeouts-retries — 消息传递超时与重试（max.in.flight.requests.per.connection）
理解生产者的传递超时体系与重试机制，以及并发在途请求数对消息顺序的影响。
- `kafka-producer-delivery-timeout-strategy` Q: 应该如何配置 `delivery.timeout.ms`，才能既保证「broker 崩溃、首领重新选举期间还能继续重试」，又不用手动精确纠结 `retries` 该设多大？
  A: 建议把 `delivery.timeout.ms` 直接设置成你愿意让生产者持续重试的最长时间（例如已知首领选举通常需要约30秒，出于保险设置为120秒），同时保留默认的、几乎无限制的 `retries` 次数。这样生产者只要还在 `delivery.timeout.ms` 规定的时间窗口内，就会一直重试，不需要再单独
- `kafka-producer-delivery-timeout-vs-request-timeout` Q: `delivery.timeout.ms` 和 `request.timeout.ms` 都是「超时」参数，二者控制的时间范围有什么不同？
  A: `request.timeout.ms` 只控制生产者在放弃单次请求之前，等待 broker 对这一次请求作出响应的时间，不包含重试和发送前排队的时间。`delivery.timeout.ms` 覆盖的范围更大：从消息准备好被发送（放入批次）开始，一直到 broker 最终响应或生产者放弃全部重试为止的总时间，所以它的
- `kafka-producer-max-block-ms` Q: `max.block.ms` 控制的是生产者哪个阶段的阻塞？和 `delivery.timeout.ms` 有什么区别？
  A: `max.block.ms` 控制的是调用 `send()`（或调用 `partitionsFor()` 查询元数据）时，生产者因为发送缓冲区已满或元数据不可用而发生阻塞的最长时间，超时会抛出超时异常，这发生在消息还没被真正放入批次、开始走发送流程之前。而 `delivery.timeout.ms` 是消息已经进入批次
- `kafka-producer-max-in-flight-ordering-risk` Q: 如果 `retries` 设置为非零、`max.in.flight.requests.per.connection`（生产者在收到响应前可以连续发送的消息批次数）大于1，为什么消息顺序可能被打乱？
  A: 因为多个批次可以同时在途（in flight，已发送但还没收到 broker 响应），如果第一个批次写入失败而排在它后面的第二个批次先写入成功，broker 随后重试写入第一个批次并成功后，这两个批次在分区里的实际落地顺序就和发送顺序颠倒了。也就是说，只要允许多个未确认请求同时在途并且开启了重试，顺序就有被打乱的风险，
- `kafka-producer-retries-retryable-vs-nonretryable` Q: 生产者收到 broker 返回的错误后，是不是所有错误都会触发自动重试？
  A: 不是。Kafka 会区分可重试错误和不可重试错误：像「非分区首领」这类暂时性错误（例如首领正在重新选举），只要重试通常就能解决，生产者会按 `retries` 参数自动重试，重试间隔由 `retry.backoff.ms` 控制；而「消息太大」这类本质性错误不会因为重试而改变结果，生产者不会重试，会立即把异常抛给应用。

## producer.idempotence-ordering — 幂等生产者开关（enable.idempotence）与顺序保证
理解开启幂等性如何消除重试导致的重复写入，并保障单分区内的消息顺序。
- `kafka-producer-idempotence-config-cloze` Q: 开启幂等生产者（`enable.idempotence=true`）要求同时满足三个条件：{{c1::max.in.flight.requests.per.connection ≤ 5}}、{{c2::retries > 0}}、{{c3::acks = all}}，否则 Kafka 会抛出 ConfigException（配置不合法异常）拒绝启动。
- `kafka-producer-idempotence-duplicate-scenario` Q: 即使把 `acks` 设为 all 并加大重试次数以追求可靠性，为什么消息仍有可能被写入 Kafka 不止一次？
  A: 设想一个 broker 收到消息，写入本地磁盘并成功复制给了其他副本，但还没来得及把成功响应发回给生产者就崩溃了。生产者等不到响应，达到 `request.timeout.ms` 后判断这次请求失败，于是重试，把同一条消息发给了新首领；但新首领其实已经通过复制拿到了这条消息，于是这条消息就在分区里出现了两次。也就是说，
- `kafka-producer-idempotence-exactly-once-relation` Q: 「幂等生产者」（idempotent producer）和 Kafka 的「精确一次性」（exactly-once semantics，每条消息只被处理一次的语义）是什么关系？
  A: 从 0.11 版本开始，Kafka 支持精确一次性语义，这是一个更大的话题，涉及生产、消费和跨系统处理等更广泛的保证。幂等生产者只是精确一次性语义里一个简单但重要的组成部分：它专门解决「生产者重试导致同一条消息被写入多次」这一类重复问题，但它本身并不等同于完整的精确一次性语义。
- `kafka-producer-idempotence-sequence-number-mechanism` Q: 开启 `enable.idempotence`（幂等生产者）之后，Kafka 靠什么机制识别并丢弃因重试产生的重复消息？生产者会不会因此报错？
  A: 幂等生产者会给发送的每一条消息都打上一个序列号。broker 如果收到了序列号与之前已经成功写入的消息相同的消息，就会判定这是一次重试导致的重复，直接拒绝写入第二份。生产者这边会收到一个 DuplicateSequenceException，但这个异常对生产者来说是无害的——它只是说明这条消息其实已经写入成功过了，不需
- `kafka-producer-idempotence-solves-ordering` Q: 如果既想让 `max.in.flight.requests.per.connection`（生产者在收到响应前能连续发送的批次数）大于1以提升吞吐量，又想开启重试以提升可靠性，但又担心重试打乱消息顺序，解决方案是什么？
  A: 把 `enable.idempotence` 设置为 true。开启幂等生产者后，Kafka 在最多允许 5 个请求同时在途的情况下仍然能保证消息顺序不被打乱，同时借助序列号机制保证重试不会引入重复消息，这样就同时兼顾了并发在途请求带来的吞吐量、以及顺序和不重复这两个可靠性要求，不需要再在它们之间做取舍。

## producer.serialization — 序列化器与使用Avro序列化数据
掌握自定义序列化器的实现方式，以及使用Avro对消息进行结构化序列化的做法。
- `kafka-producer-avro-generic-vs-specific-record` Q: 用 Avro 发送数据时，「基于模式生成的专用对象（如 Customer 类）」和「通用的 GenericRecord」这两种方式有什么区别？
  A: 专用对象是通过 Avro 代码生成工具，根据模式预先生成带有 getter/setter 方法的 Java 类（如 Customer），发送前需要先生成好这些类；GenericRecord 则像一个通用的键值容器（类似 map），可以在运行时直接用一个 Schema 对象和字段名/值来构造记录，不需要事先生成任何专用类
- `kafka-producer-avro-schema-evolution-example` Q: 一个 Avro 模式（schema，描述消息结构的规范）原本有 `faxNumber` 这个可选字段，后来被替换成 `email` 字段。还在用旧代码的消费者程序，读到用新模式写的消息时会发生什么？为什么不会报错中断？
  A: 消费者程序调用 `getFaxNumber()` 读取传真号字段时会得到 null，因为新消息里根本没有这个字段，但整个反序列化过程不会抛异常、也不会中断。这是 Avro 模式演化（schema evolution）的效果：只要新旧模式相互兼容，读取方即使还没升级到能识别新字段（如 `getEmail()`）的版本，依
- `kafka-producer-avro-writer-reader-schema-compatibility` Q: 使用 Avro 时，「写入数据时用的模式」和「读取数据时用的模式」一定要完全相同吗？反序列化器（deserializer）具体需要用到哪个模式？
  A: 不需要完全相同，但两者必须相互兼容（Avro 文档定义了具体的兼容性规则）。反序列化时真正需要用到的是写入数据时所用的那份模式，即使它与读取方当前期望的模式版本不一样，也要能拿到当初写入时的模式，才能正确解析出字段，即便某些字段在读取方版本里已经改名或废弃。
- `kafka-producer-custom-serializer-fragility` Q: 为什么不建议给业务对象手写自定义序列化器（custom serializer），而是推荐使用 Avro、Thrift、Protobuf 这类通用序列化框架？
  A: 手写序列化器把字段的编码方式硬编码在代码里，一旦对象结构发生变化（比如把某个字段类型从 int 改成 long，或新增一个字段），新旧序列化器产生的字节数组就不兼容，排查这种兼容性问题需要直接比较原始字节，非常困难。而且如果公司里多个团队都要写入同一种对象，大家必须使用完全相同的序列化器代码并同步修改，协调成本很高。通
- `kafka-producer-schema-registry-purpose` Q: 如果每条 Avro 消息都完整携带自己的模式定义，会有什么问题？Kafka 生态里常用什么方案来避免这个问题？
  A: Avro 的完整模式定义体积不小，如果每条消息都内嵌一份完整模式，会成倍增加每条消息的大小，造成很大的存储和网络开销。常见做法是引入一个独立的模式注册表（schema registry，例如 Confluent Schema Registry），把所有用到的模式集中保存在注册表里，消息本身只携带一个模式标识符；生产者写

## producer.extensibility — 分区策略、消息标头（headers）与拦截器
掌握如何自定义分区策略、通过消息标头携带元数据，以及用拦截器介入发送生命周期。
- `kafka-producer-custom-partitioner-hotkey-isolation` Q: 一个 B2B 供应商的某个大客户贡献了超过10%的交易量。如果继续用默认的哈希分区策略，会带来什么问题？自定义分区器（custom partitioner）如何解决它？
  A: 默认哈希分区器会把这个大客户的消息和其他客户的消息混在同一个（由哈希值决定的）分区里，导致这个分区的数据量远大于其他分区，可能造成该分区所在服务器存储紧张、请求处理变慢。解决办法是实现 Kafka 的 Partitioner 接口，在 partition() 方法里对这个大客户的键做特殊判断（比如固定分配到某个专用分区
- `kafka-producer-headers-purpose` Q: Kafka 消息除了键和值，还可以携带「标头」（headers）。标头解决了什么问题？为什么有时候必须靠标头而不是解析消息体来做路由？
  A: 标头是一组有序的键值对（键是字符串，值可以是任意序列化后的对象），可以在不改变消息键值内容的情况下附加元数据，比如标明消息的来源。它的一个重要用途是：某些中间处理系统（如路由器）需要根据消息的元数据来做路由或链路追踪，但消息体本身可能是加密的、这些系统根本没有权限解密查看内容，这时候读取标头就成了在不接触消息体的情况下
- `kafka-producer-interceptor-hooks` Q: Kafka 生产者拦截器（ProducerInterceptor）提供的 `onSend` 和 `onAcknowledgement` 两个方法分别在什么时机被调用？为什么用拦截器而不是直接改业务代码更适合做监控埋点这类需求？
  A: `onSend` 在记录被发送、甚至在被序列化之前调用，可以读取甚至修改这条记录，但必须返回一个合法的 ProducerRecord；`onAcknowledgement` 在收到 Kafka 的确认响应时调用，可以读取响应信息（如是否出错）但不能修改它。拦截器的好处是可以在完全不修改业务代码的前提下，给公司里所有使用
- `kafka-producer-key-hash-partition-consistency` Q: 生产者用键的哈希值把消息映射到固定分区，能保证「同一个键总是被写到同一个分区」，这个保证在什么情况下会被打破？
  A: 只要主题的分区数量不发生变化，键到分区的哈希映射就是稳定的，比如某个用户的记录总是被写到某个固定分区，从而能针对这种局部性做各种读取优化。但一旦给主题增加了新分区，旧数据依然留在原来的分区里，而新写入的相同键的记录却可能被哈希到新分区，映射关系就被打破了。所以如果要依赖键到分区的稳定映射，最好在建主题时就规划好分区数，
- `kafka-producer-key-null-sticky-partitioning` Q: 如果 ProducerRecord 没有指定键（key 为 null），Kafka 默认分区器会怎么选择分区？Kafka 2.4 之后这个策略有什么改进？
  A: 键为 null 时，默认分区器采用轮询调度（round-robin）算法把消息尽量均衡地分布到各个分区。从 Kafka 2.4 开始，这个轮询变成了「粘性」的（sticky）：在切换到下一个分区之前，会把同一个批次里的消息都写入当前分区，而不是每条消息都轮换一次分区。这样可以用更少的请求发送相同数量的消息，既降低延迟，
