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
  "streams.concepts": ["<id shown first>", "…"],
  "streams.design-patterns": ["<id shown first>", "…"],
  "streams.streams-api": ["<id shown first>", "…"],
  …
}

## streams.concepts — 流式处理核心概念
掌握拓扑、时间语义、状态、流与表的对偶关系、时间窗口与处理保证等流式处理的核心概念。
- `kafka-streams-exactly-once-config` Q: Kafka Streams 应用要开启「精确一次」处理保证（一条记录不管是否发生故障，都恰好被处理一次，不多不少），需要把 `processing.guarantee` 配置成什么值？它依赖 Kafka 的哪些底层特性来实现？`exactly_once_beta` 这个更高效的实现选项对 broker 版本有什么要求？
  A: 把 `processing.guarantee` 设置为 `exactly_once` 就能启用精确一次保证；Streams 借助 Kafka 生产者原生支持的**事务**（transaction）和**幂等性**（idempotence，避免因重试导致同一条消息被重复写入）这两项特性来实现这个保证，而不是自己重新发明
- `kafka-streams-local-vs-external-state` Q: Kafka Streams 应用在做聚合、连接这类需要跨事件累积信息的操作时要维护「状态」，可以选择把状态存在应用实例内嵌的本地状态存储里，也可以存到 Cassandra 这类外部数据存储里。这两种方式各自的优缺点是什么？
  A: 本地状态（local state）只能被这一个应用实例访问，通常内嵌在应用进程里，优点是访问速度快，缺点是容量受限于这台机器的可用内存，所以很多流式处理设计会先把数据拆分成多个子流，让每一份本地状态只需要处理其中一小部分数据。外部状态（external state）保存在独立的外部存储系统里，几乎没有容量上限，还能被同
- `kafka-streams-stream-table-duality` Q: 流和表可以看作「同一枚硬币的两面」。把一张数据库表转成一条事件流、以及把一条事件流转成一张表，分别对应什么操作？
  A: 表（table）保存的是数据在某一时刻的当前状态（比如客户当前的联系方式），流（stream）保存的是导致状态变化的一系列历史事件（比如每一次联系方式的修改记录）。把表转成流，需要捕获这张表发生过的所有 insert、update、delete 变更事件并依次写入流，这通常靠数据库的 CDC（change data c
- `kafka-streams-time-semantics-choice` Q: Kafka Streams（Kafka 官方流式处理库）在处理事件时可以使用事件时间、日志追加时间、处理时间三种不同的时间语义。计算「某一天实际生产了多少台设备」这类统计时，应该优先用哪种时间？为什么说处理时间「最好避免使用」？
  A: 应该优先用**事件时间**（事件真正发生的时刻，比如设备实际下线的时间），因为它反映的是业务上事情真正发生的那一刻，即使消息因为网络问题延迟一天才写入 Kafka，事件时间也不会变。**日志追加时间**（消息到达并写入 broker 的时刻，也叫摄取时间）可以在事件时间缺失时作为近似替代，前提是数据管道延迟不大。**处
- `kafka-streams-tumbling-hopping-session-window` Q: Kafka Streams 支持滚动窗口（tumbling window）、跳跃窗口（hopping window）、会话窗口（session window）三种时间窗口，它们各自是按什么规则划定窗口边界的？什么场景适合用会话窗口？
  A: 滚动窗口是「移动间隔等于窗口大小」的固定窗口，比如每5分钟统计一次、窗口之间彼此不重叠也不留缝隙。跳跃窗口是「移动间隔比窗口大小更频繁」的固定窗口，比如窗口大小是5分钟但每1分钟就滑动一次，相邻窗口之间会有重叠，能提供更平滑、更新更频繁的结果，但计算量也更大。会话窗口不是固定长度的，而是按「不活跃时间段」来划定：只要连
- `kafka-streams-window-grace-period` Q: 一个基于事件时间的5分钟移动平均数窗口（比如00:00~00:05）已经计算完成一小时后，又收到了一条事件时间落在00:02的迟到消息，Kafka Streams 是否应该重新计算并更新这个窗口的结果？由什么机制决定？
  A: 由应用开发者配置的**宽限期**（也叫窗口可更新时间）决定：宽限期规定了一个时间段，在这个时间段内到达的迟到事件仍然可以被补算进它本应归属的那个时间窗口，触发结果更新；一旦超过这个宽限期还没到达，这条事件就会被直接忽略，不会再去更新已经「定型」的旧窗口结果。比如把宽限期设为4小时，就意味着只要事件到达时间与它的事件时间

## streams.design-patterns — 流式处理设计模式
掌握本地状态、多阶段处理与重分区、流表连接、处理乱序事件等常见流式处理设计模式。
- `kafka-streams-external-lookup-vs-table-join` Q: 要把用户信息填充到点击事件流里，一种做法是每次来一条点击事件就实时查询外部用户信息数据库，另一种做法是通过 CDC（change data capture，变更数据捕获）把这张用户表转成一条变更事件流、在流式处理应用里物化成本地缓存表再做「流与表的连接」。为什么更推荐后者？
  A: 实时查询外部数据库有两个致命问题：一是每次查询都会给这条记录的处理增加 5~15 毫秒的额外延迟；二是流式处理系统每秒能处理的事件量（10万到50万级别）远超普通数据库每秒能承受的查询量（约1万级别），把数据库当成实时查找服务用，很容易把它打垮，还引入了「数据库不可用时应用该怎么办」的额外复杂度。用 CDC 把用户表的
- `kafka-streams-local-state-recovery-changelog` Q: Kafka Streams 应用把聚合状态保存在本地（比如内嵌的 RocksDB）里，如果这个应用实例发生崩溃、之后在同一台或另一台机器上重启，本地状态是怎么恢复回来的，而不会丢失？
  A: Streams 除了把状态写进本地的 RocksDB，还会把这个本地状态的每一次变更同步发送到一个 Kafka 主题（changelog 主题）里，比如把「IBM 当前最低价 167.19」这类变更记录下来；这个主题使用压缩日志（compacted topic，只保留每个键最新值的日志清理策略），所以不会随时间无限膨胀
- `kafka-streams-multistage-repartition` Q: 要计算「今天全市场涨幅前10的股票」，为什么不能只靠每个应用实例各自维护的本地状态直接算出来？两阶段方案是怎么解决这个问题的？
  A: 本地状态只对**分组聚合**有效——每个实例只能看到被分配给自己的那些分区（比如某几只股票代码）的数据，天然算不出跨越所有股票、需要全局排名的结果，因为涨幅最高的10只股票可能分散在不同实例负责的分区里。两阶段方案是：第一阶段，每个实例仍用本地状态算出各自负责的每只股票当天的涨跌幅（这一步的输入数据量很大，需要多个实例
- `kafka-streams-out-of-order-late-result-overwrite` Q: 一个基于事件时间的聚合时间窗口已经算出了结果并写入了输出主题，之后又收到了属于这个窗口、但姗姗来迟的乱序事件，Kafka Streams 是重新算一条新记录追加进去，还是覆盖之前的结果？为什么要用压缩日志主题（compacted topic）来保存这类聚合结果？
  A: Streams 会针对这同一个聚合时间窗口重新计算出更新后的结果，并把它作为**新的一条记录**再次写入输出主题，这条新记录会用同样的键（代表这个时间窗口）覆盖掉旧的那条结果，而不是在流水账式地追加一条独立记录。因为聚合结果对应输出主题采用了压缩日志策略，即只保留每个键的最新值，这样即使同一个时间窗口的结果因为迟到事件
- `kafka-streams-reprocessing-two-versions-safer` Q: 给已有的流式处理应用修复了一个逻辑 bug，需要用修好的新版本重新计算历史结果，为什么建议优先「让新版本作为一个全新的消费者群组、从头重新处理并产出一份独立的新结果流」，而不是直接「重置」现有应用回到起点重新跑？
  A: 直接重置现有应用需要同时把输入流的读取位置、应用内部维护的本地状态都清空回到最初，还可能要手动清理掉旧的输出结果，操作复杂、任何一步出错都可能导致数据丢失或新旧结果混在一起，而且一旦跑错了没有回头路。而让新版本应用作为一个**新的消费者群组**独立从头读取输入主题、产出一份全新的结果流，旧版本应用和它的结果流完全不受影
- `kafka-streams-table-join-vs-stream-join-windowing` Q: 「表与表的连接」和「流与流的连接」都是 Kafka Streams 支持的连接操作，但前者不基于时间窗口、后者却必须基于时间窗口，为什么会有这个区别？
  A: 表代表的是数据当前的状态，连接两张表本质上是把两边当前各自最新的状态匹配起来，任意时刻查询得到的都是「当下」的结果，不涉及“哪些事件发生在同一段时间内”这个问题，所以表与表的连接不需要时间窗口。而流代表的是无边界的历史事件序列，连接两个真实的流意味着要把发生在**相近时间段**内、键相同的事件两两匹配起来（比如用户输入

## streams.streams-api — Kafka Streams API与拓扑构建
通过字数统计等示例掌握用Kafka Streams API构建处理拓扑的基本写法。
- `kafka-streams-application-id-role` Q: 创建 KafkaStreams 应用时必须配置 `StreamsConfig.APPLICATION_ID_CONFIG`（应用程序 ID），这个 ID 起什么作用？为什么它必须在同一个 Kafka 集群内保持唯一？
  A: 应用程序 ID 有两个作用：一是被同一个应用启动的多个实例用来互相协调、组成一个处理集群（类似消费者群组的机制）；二是被 Streams 用来给这个应用内部自动创建的本地状态存储和相关的内部主题（比如状态变更日志主题）命名。如果同一个 Kafka 集群里两个不同的 Streams 应用用了相同的应用程序 ID，它们各自
- `kafka-streams-cluster-no-external-scheduler` Q: 很多流式处理框架在本地开发时很简单，但要部署到生产集群，往往需要额外安装 YARN 或 Mesos 这类资源调度系统，并在所有机器上单独装框架、再学习如何提交作业。用 Kafka Streams 部署一个多实例集群，需要额外安装这些资源调度组件吗？为什么？
  A: 不需要。Kafka Streams 应用本质上就是一个普通的 Java 应用程序，把它的多个实例分别启动起来（在不同机器或不同终端里各跑一份），这些实例会通过 Kafka 自身的机制（类似消费者群组协调分区分配）互相发现、协调，自动分摊输入主题的分区，从而组成一个处理集群。这意味着开发机上运行的和生产环境里运行的完全是
- `kafka-streams-dsl-vs-processor-api` Q: Kafka 提供了两套构建流式处理逻辑的 API：底层的 Processor API 和高级的 Streams DSL（domain specific language，领域特定语言）。写字数统计、股票统计这类应用时，为什么通常优先选用 Streams DSL 而不是 Processor API？
  A: Streams DSL 让开发者通过给一个 KStream/KTable 声明式地串联一连串转换（比如 flatMapValues、filter、groupByKey、aggregate）来定义处理拓扑，绝大多数常见的过滤、聚合、连接需求都能用几行链式调用表达清楚，简单直观、上手成本低。Processor API 是更
- `kafka-streams-groupbykey-noop-when-key-unchanged` Q: 在字数统计示例里，调用 `.map(...)` 把单词放进事件的键之后，紧接着又调用了一次 `.groupByKey()`，但这个方法实际上并没有真正执行任何重新分组或重分区的工作。既然什么都没做，为什么还要调用它？
  A: `groupByKey()` 本身并不会重新洗牌或触发网络传输，它只是向 Streams 声明「接下来的聚合操作要按当前的键进行分区处理」，并确认当前事件流确实已经是按这个键分区的。因为在这条处理链里，从写入主题时使用的键，到调用 `groupByKey()` 之前都没有再修改过键，所以数据本来就已经是按这个键正确分区
- `kafka-streams-joinwindows-asymmetric-before` Q: 示例里用 `JoinWindows.of(Duration.ofSeconds(1)).before(Duration.ofSeconds(0))` 来连接搜索事件流和点击事件流，为什么不直接用一个对称的「搜索前后各1秒」的窗口，而要额外调用 `before(0秒)` 来收窄它？
  A: `JoinWindows.of(Duration.ofSeconds(1))` 默认构造的是一个对称窗口，即搜索事件前1秒到后1秒之间的点击事件都会被匹配进来；但业务逻辑上，只有发生在搜索**之后**的点击才可能是「用户看到搜索结果后点击」，发生在搜索之前的点击和这次搜索毫无关系，只是巧合地落在了时间窗口内。调用 `.
- `kafka-streams-leftjoin-stream-table-vs-stream-stream` Q: 填充点击事件流的示例里，先用 leftJoin 把点击事件流和用户信息表（KTable）连接，再用 leftJoin 把结果和搜索事件流连接，但后一个 leftJoin 多传了一个 JoinWindows 参数，前一个却没有。为什么流与表的连接不需要时间窗口，而流与流的连接必须指定时间窗口？
  A: KTable（用户信息表）在任意时刻都代表这份数据当前最新的状态，流与表做 leftJoin 时，每一条流事件到达的那一刻，直接去查这张表缓存里当前的值就行，不涉及“表里的哪个历史版本对应流里的哪个时间点”这个问题，所以不需要时间窗口。而点击事件流和搜索事件流都是无边界的历史事件序列，如果不加时间窗口限制，理论上要把每

## streams.streams-architecture — Kafka Streams架构
理解Streams如何优化、测试、扩展拓扑，以及在故障发生时如何存活并恢复状态。
- `kafka-streams-join-requires-copartition` Q: Kafka Streams 中「任务」（task，Streams 里最基本的并行执行单元，负责处理输入主题里的一部分分区）是独立执行的，但要连接两个流（比如把点击事件流和搜索事件流连接起来）时，为什么要求参与连接的所有主题必须有相同的分区数，并且都按连接用的键进行分区？
  A: 连接操作需要同时看到两条流里键相同的事件才能配对，如果两个输入主题的分区数不同，或者分区依据的键不一致，那么同一个用户（或同一个连接键）产生的事件就可能被分散到不同数量、不对应的分区里，没有哪一个任务能同时拿到这个键在两个主题里的全部相关事件。只有当两个主题分区数相同且按同一个键分区时，Streams 才能把「相同分区
- `kafka-streams-repartition-splits-subtopology` Q: 一个 Streams 应用原本所有事件都按用户 ID 分区，现在要基于邮政编码重新做聚合统计，这就需要对数据重新分区（repartition）。这次重新分区会把原来的一个拓扑拆成什么结构？两组任务之间是紧密耦合、需要互相等待的吗？
  A: 重新分区会把原来单一的拓扑拆分成两个独立的子拓扑，各自拥有一组任务：第一组任务按原来的键（用户 ID）读取和处理数据，处理完之后把结果连同新的键（邮政编码）写入一个新主题；第二组任务再从这个新主题读取数据、按新的分区方式执行后续聚合。两组任务之间不需要互相通信、不共享任何运行资源，也不需要跑在同一个线程或同一台服务器上
- `kafka-streams-standby-replica-and-compaction-speedup` Q: 一个 Streams 任务所在的实例发生故障后，另一个实例接手这个任务时需要先重建本地状态（比如当前的聚合窗口），这个恢复期间应用会暂停处理、造成短暂不可用。除了缩小内部状态主题的 `min.compaction.lag.ms`、把日志片段大小从默认的1 GB调小到100 MB以加快压实、缩短需要重放的数据量之外，还有什么机制能进一步大幅缩短这段恢复时间？
  A: 可以为任务配置备用副本（standby replica）：这是运行在其他服务器上的「影子任务」，它们平时就在持续同步、保持着与活跃任务几乎相同的最新本地状态，而不是等到故障发生才开始从头重建。一旦活跃任务所在实例发生故障，原本就已持有最新状态的备用副本可以近乎零停机地立刻接管处理，不需要再经历「从头读取内部状态主题、重
- `kafka-streams-testcontainers-vs-embedded-cluster` Q: 对 Kafka Streams 应用做集成测试，EmbeddedKafkaCluster（broker 和测试代码跑在同一个 JVM 里）和 Testcontainers（broker 跑在 Docker 容器里）是两个常见选择，为什么优先推荐 Testcontainers？
  A: EmbeddedKafkaCluster 把 broker 和被测代码放进同一个 JVM 进程运行，测试环境和真实生产环境的隔离程度较低，测试代码的类加载、依赖冲突等问题可能干扰到内嵌 broker，也更难完全模拟真实网络行为。Testcontainers 借助 Docker，把 Kafka、它依赖的组件以及测试所需的
- `kafka-streams-topology-optimization-flag` Q: 用 Streams DSL（领域特定语言）写的每一步转换默认会被独立映射成对应的底层操作，错失了对整体执行计划做优化的机会。要让 Streams 在生成物理拓扑时对整体执行计划进行优化，需要做哪两件事，缺一会怎样？
  A: 需要两步同时做到：一是把配置 `StreamsConfig.TOPOLOGY_OPTIMIZATION` 设置为 `StreamsConfig.OPTIMIZE`；二是调用 `StreamsBuilder.build(props)` 时把这份包含该配置的 Properties 对象传进去。如果只调用不带参数的 `bui
- `kafka-streams-topologytestdriver-limitation` Q: TopologyTestDriver 是测试 Kafka Streams 应用拓扑的推荐工具，它让测试代码可以像普通单元测试一样：把数据写入模拟输入主题、运行拓扑、再从模拟输出主题读取结果做断言。但用它测试有一类问题检测不出来，是什么？
  A: TopologyTestDriver 没有模拟 Streams 内部的缓存行为（一种用于减少不必要中间结果写入下游的优化机制），所以任何只有在真实缓存生效时才会暴露出来的问题，用这个工具是测不出来的。因此它适合作为快速、轻量、易调试的单元测试手段，但不能完全替代需要跑真实 broker 的集成测试或端到端测试。

## streams.choosing-framework — 流式处理的应用场景与框架选型
掌握判断一个问题是否适合流式处理，以及在多种流式处理框架之间做选型的考量维度。
- `kafka-streams-async-microservice-requirements` Q: 要用流式处理框架给异步微服务（负责执行大型业务流程里某个简单操作，比如更新库存信息）搭建本地状态缓存，这个框架至少需要具备哪两项能力，分别解决什么问题？
  A: 第一，需要能与消息总线（最好就是 Kafka 本身）集成，并具备变更捕获（CDC，change data capture）能力，这样上游数据源的变更才能被实时同步进来，用来持续更新微服务自己维护的本地缓存，避免缓存数据过时。第二，需要支持本地存储，把它当作这个微服务数据的缓存和物化视图使用，这样微服务在处理请求时可以直
- `kafka-streams-complex-analytics-requires-local-storage` Q: 要构建一个执行复杂聚合和连接操作的几近实时数据分析引擎，为什么这类应用必须选择支持本地存储的流式处理框架，而且这里的「本地存储」用途和异步微服务场景里的本地存储用途并不一样？
  A: 高级聚合（比如按时间窗口计算平均值）、时间窗口操作和多种类型的连接，都需要在处理过程中持续维护一份「到目前为止累积的中间结果」（比如某个时间窗口内已经看到的最小值、总和、计数），如果框架没有支持本地存储中间状态的能力，这些操作根本无法实现。这里本地存储的用途是保存计算过程中的**聚合中间状态**，而不是像异步微服务场景
- `kafka-streams-ingestion-connect-vs-streamproc` Q: 需求是「把数据从一个系统搬到另一个系统，传输过程中顺带做一些格式转换」，这属于数据摄取场景。在这种场景下，应该优先考虑专门做数据摄取的系统（如 Kafka Connect），还是上一整套流式处理框架？
  A: 应该先判断这个搬运和转换需求是否简单到用专门的数据摄取系统就能搞定——数据摄取系统通常更轻量、专注于把数据从源系统搬到目标系统并做一些通用转换，不需要额外引入流式处理框架的学习和运维成本。只有当转换逻辑复杂到数据摄取系统无法胜任、确实需要用流式处理框架时才引入它，而且这时还要确认这个流式处理框架和数据的源系统、目标系统
- `kafka-streams-low-latency-event-vs-microbatch` Q: 要构建一个要求「立即得到响应」的低延迟应用（比如某些欺诈检测系统），为什么首先要考虑这个需求是否真的适合用流式处理框架来做？如果确实需要流式处理，应该选逐事件处理模型还是微批次（micro-batch）模型的框架？
  A: 「立即响应」往往意味着对单次请求的延迟要求达到亚毫秒到毫秒级，这正是请求与响应范式（比如直接同步调用一个服务）最擅长的场景；流式处理框架处理的是持续到达的事件流，即使延迟很低，通常也达不到请求响应模式那种确定性的极低延迟，所以要先确认这个问题是不是用一次同步的请求/响应调用就能解决，而不是默认套上流式处理。如果业务确实
- `kafka-streams-samza-spark-flink-beam` Q: Samza、Spark、Flink、Beam 都可以用于流式处理，但设计定位差别很大：如果需要极低延迟的逐事件处理，如果更看重容错和广泛的社区生态、可以接受微批次带来的延迟，如果想用一套代码同时兼顾流处理和批处理，分别应该倾向选哪一个？
  A: 需要极低延迟的逐事件处理，应该倾向 **Flink**——它专门面向流式处理设计，延迟非常低，除了 Yarn 还能运行在 Mesos、Kubernetes 或独立集群上，并且高级 API 支持 Python 和 R。更看重容错能力和广泛社区支持、能接受微批次延迟的，倾向 **Spark**——它本质是面向批处理的项目，
- `kafka-streams-selection-criteria-beyond-usecase` Q: 除了针对具体应用场景挑选合适的流式处理框架，选型时还应该从全局评估四个维度：{{c1::系统的可操作性（是否容易部署、监控、调试、扩展，能否与现有基础设施集成，出错后如何重新处理数据）}}、{{c2::API 的可用性和可调试性（用同一个框架的不同实现开发同等质量的应用所耗费的时间可能相差很大）}}、{{c3::抽象是否真正化繁为简（框架是替开发者处理好了伸缩和故障恢复，还是只给了一层脆弱的抽象、把剩下的脏活丢给开发者自己解决）}}、{{c4::社区是否活跃（活跃社区意味着新特性、较高的软件质量、更快的 bug 修复，以及能在网上搜到别人遇到过的同类问题）}}。
