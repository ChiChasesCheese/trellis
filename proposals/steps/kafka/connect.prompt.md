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
  "connect.pipeline-design": ["<id shown first>", "…"],
  "connect.connect-basics": ["<id shown first>", "…"],
  "connect.smt": ["<id shown first>", "…"],
  …
}

## connect.pipeline-design — 构建数据管道的设计考量
理解及时性、可靠性、吞吐量、数据格式与耦合性等因素如何影响数据管道的设计取舍。
- `kafka-connect-pipeline-delivery-guarantee-levels` Q: 数据管道对「传递保证」的要求通常分为哪两个级别？Kafka 本身天然支持哪一级，要做到更高一级的保证，还需要依赖什么条件？
  A: 两个级别：**至少一次传递**（at-least-once，源系统的每个事件都必须到达目的地，但重试可能导致同一事件被传递不止一次）和**精确一次传递**（exactly-once，每个事件必须到达且不能丢也不能重复）。Kafka 本身天然支持至少一次传递；要实现精确一次传递，需要 Kafka 的事务机制，再配合目标端
- `kafka-connect-pipeline-etl-vs-elt` Q: 构建数据管道时，「在数据流经管道时就做转换（ETL）」和「先原样搬到目标系统，转换交给目标系统去做（ELT）」，这两种做法各自的核心优势和代价是什么？
  A: ETL（提取–转换–加载，extract-transform-load）在数据经过管道时就完成清洗、过滤、改字段等加工，省去了「先落地原始数据、再改、再落地」这几步，节省时间和存储；但代价是下游应用程序只能拿到被转换过的数据，如果后续需要访问被过滤掉的字段或原始记录，往往必须重建管道并重新回放历史数据（如果历史数据还在
- `kafka-connect-pipeline-overprocessing-coupling` Q: 如果一条数据管道在搬运数据的过程中做了过多的聚合、字段裁剪等「末端处理」，会给整个系统的灵活性带来什么隐患？推荐的替代做法是什么？
  A: 管道里做的处理越多，就等于把「哪些字段该保留」「数据该怎么聚合」这类业务决策提前固化在了管道本身里，下游系统被迫接受这些既定选择；一旦下游系统的需求发生变化（比如需要一个被管道过滤掉的字段），就必须回过头去修改管道逻辑，这种改动既不灵活，也容易出错、效率低。推荐的做法是尽量在管道里保持原始数据的完整性，只做少量必要的预
- `kafka-connect-pipeline-schema-loss-coupling` Q: 一条从 Oracle 到 HDFS 的数据管道，如果不保留模式（schema）元数据、也不支持模式的变更传播，当 DBA 在 Oracle 表里新加了一个字段之后，会给下游带来什么麻烦？相比之下，支持模式演进的管道好在哪？
  A: 如果管道不保留模式信息，生产者（写入端）和消费者（读取端）就只能靠约定或硬编码去解析数据格式，形成了事实上的紧密耦合；一旦 Oracle 端加了新字段却没有把这个模式变化传递下去，所有从 HDFS 读取数据的下游应用都会因为格式对不上而出错，开发者不得不逐一修改每个下游应用才能修复。如果数据管道本身支持保留并传播模式（
- `kafka-connect-pipeline-throughput-decoupling` Q: 如果生产者写入 Kafka 的速度突然远超消费者处理数据的速度，为什么不需要在管道里实现复杂的回压（backpressure）机制来协调两端？
  A: 因为 Kafka 把生产者和消费者的吞吐量也解耦了：生产者写入的数据会先积压保存在 Kafka 里，而不是直接冲击消费者，等消费者的处理能力追上来之后再慢慢消化这些积压数据即可。生产者端和消费者端还可以各自独立地动态扩缩容（比如单独增加消费者实例）来应对吞吐量的变化，不需要精细协调两端的处理节奏。这也是为什么用 Kaf
- `kafka-connect-pipeline-timeliness-buffer` Q: 同一条数据管道里，上游生产者需要每毫秒实时写入数据，下游某个消费系统却只想每小时批量拉取一次数据处理。把 Kafka 放在中间，为什么能同时满足这两种截然不同的「及时性」需求，而不需要为它们分别搭建两条管道？
  A: Kafka 起到了一个巨大缓冲区的作用，把生产者和消费者对「时间」的敏感度**解耦**了：生产者可以按自己的节奏（实时或批量）往 Kafka 写，消费者也可以按自己的节奏（实时读取或每小时连一次读取积压数据）从 Kafka 读，两边互不干扰，因为数据先落到 Kafka 里持久保存，谁都不用等对方。这也让施加回压（bac

## connect.connect-basics — Kafka Connect：适用场景与架构
理解何时该用Connect API而不是原生客户端API，以及source/sink连接器与Connect worker的协作方式。
- `kafka-connect-connector-vs-task-division` Q: 在 Connect 里，「连接器（connector）」和它启动的「任务（task）」分别负责什么？以 JDBC 数据源连接器为例说明两者是怎么分工的。
  A: 连接器本身**不直接搬运数据**，它负责三件事：决定要运行多少个任务、决定如何把数据复制工作拆分给这些任务、把每个任务的具体配置信息传给 worker（Connect 的运行节点）去启动任务。「任务」才是真正把数据搬进或搬出 Kafka 的执行单元。以 JDBC 数据源连接器为例：它连接数据库后统计出要同步的表的数量，
- `kafka-connect-converter-decouples-format` Q: Connect 的「转换器（converter）」在整个数据流转过程中扮演什么角色？它是怎么让「连接器要接入什么系统」和「数据在 Kafka 里以什么格式存储」这两件事互不影响、可以自由组合的？
  A: 数据源连接器（比如 JDBC 连接器）读取外部系统的数据后，会用 Connect 自带的一套内存对象模型（Schema 描述字段类型，Struct 保存具体字段值）来表示这条记录，而不是直接生成 JSON、Avro 这类具体格式；真正把这个内存对象序列化成 Kafka 里存储的字节格式（比如 JSON、Avro、Pro
- `kafka-connect-prefer-over-custom-app` Q: 如果想对接的外部系统还没有现成的连接器（connector），推荐的做法是优先基于 Connect API 开发一个连接器，而不是直接写一个独立的小应用程序（用生产者/消费者客户端手写读写逻辑）。为什么明明后者「看起来更简单」，却不推荐？
  A: 手写一个从 Kafka 读数据插入数据库的小程序，核心逻辑确实一两天就能写完，但真正让集成可靠、好用的部分——配置管理、多种数据类型的处理、并行处理、错误处理、REST 管理接口、故障恢复、伸缩性——都需要投入大量额外精力才能做好，可能要花几个月而不是几天；而且团队里其他人还要学习和维护这个自制方案。Connect 作
- `kafka-connect-source-offset-atleastonce-mechanism` Q: 数据源连接器（source connector）任务在向 worker 汇报「已处理到哪里」时，用的是 Kafka 自己的分区和偏移量吗？worker 是在什么时机才把这个进度持久化下来，这个时机为什么和「至少一次传递」的保证有关？
  A: 不是。数据源连接器返回给 worker 的每条记录都带着一个**逻辑分区和逻辑偏移量**，这是「源系统」自己的概念，与 Kafka 的分区/偏移量无关——比如文件数据源里，分区可以是某个文件，偏移量是文件里的行号或字符位置；JDBC 数据源里，分区可以是一张数据库表，偏移量是某条记录的 ID 或时间戳。worker 只
- `kafka-connect-vs-client-api-decision` Q: 什么情况下应该用 Kafka 的生产者/消费者客户端 API 直接对接 Kafka，什么情况下应该改用 Kafka Connect（一个专门用于在 Kafka 和外部数据存储系统之间移动数据的框架）？
  A: 如果要连接 Kafka 的应用程序代码是你自己开发、可以随意修改的（比如一个业务服务想主动往 Kafka 写事件或读事件），就直接把生产者/消费者客户端嵌入到这个应用程序里。如果要对接的是一个你没有开发、无法或不想修改其代码的外部数据存储系统（比如 MySQL、ElasticSearch 这类现成系统），就应该用 Co
- `kafka-connect-worker-separation-of-concerns` Q: Connect 的 worker（承载连接器和任务运行的节点，多个 worker 组成一个 worker 集群）具体负责哪些事情？为什么说「连接器和任务负责搬数据、worker 负责搬数据之外的一切」是 Connect API 相对普通客户端 API 的最大优势？
  A: worker 负责处理创建/管理连接器的 REST 请求、把连接器配置持久化到内部 Kafka 主题、启动连接器和任务并给任务分发配置、自动把偏移量提交到内部主题，以及在任务抛异常时重试；如果某个 worker 崩溃，集群里其他 worker 会通过消费者协议的心跳机制感知到，并把它上面的连接器和任务重新分配出去，新 

## connect.smt — 单一消息转换（SMT）与Connect内部机制
掌握单一消息转换如何在不写代码的情况下对流经Connect的记录做轻量加工。
- `kafka-connect-smt-common-types` Q: Connect 内置的单一消息转换（SMT）覆盖了几类常见的轻量加工需求，包括：{{c1::Cast——改变某个字段的数据类型}}、{{c2::MaskField——把某个字段的内容替换成 null，常用于遮蔽个人识别信息等敏感数据}}、{{c3::Filter——按主题名、消息头或是否为墓碑消息（值为 null 的消息）等条件丢弃或保留记录}}、{{c4::RegexRouter——用正则表达式和替换字符串动态改变消息要写入的目标主题}}、{{c5::InsertHeader——给每条消息的消息头（header）里加入一个固定的字符串}}。这些转换都不需要写代码，只需在连接器配置里声明即可生效。
- `kafka-connect-smt-config-not-connector-specific` Q: 在给某个连接器加一个 SMT（比如给 MySQL 数据源连接器加 `InsertHeader`）时，这个 SMT 的配置和使用方式是不是要针对不同的连接器类型分别学习一套专属语法？
  A: 不是。SMT 的配置方式与具体使用哪个连接器无关，是 Connect 框架层面提供的统一能力：不管底层连接的是 MySQL、ElasticSearch 还是其他系统，都在连接器配置里用相同的 `transforms`、`transforms.<name>.type` 等参数声明要用哪个 SMT、传什么参数。这意味着一旦
- `kafka-connect-smt-error-tolerance-dlq` Q: 一个数据池连接器（sink connector）在处理来自 Kafka 的记录时，遇到了一条格式损坏、无法正常处理的消息。配置参数 `error.tolerance` 能提供哪两种应对方式，分别适合什么场景？
  A: `error.tolerance` 可以让连接器在遇到处理失败的消息时选择：一种是**静默丢弃**这条损坏的消息，直接继续处理后面的记录，适合那种「个别脏数据丢了也无所谓、更看重管道不中断」的场景；另一种是把这条消息路由到一个专门的「死信队列（dead letter queue）」主题里，管道继续正常运行，同时保留下这
- `kafka-connect-smt-insertheader-lineage-example` Q: 如果想给某个连接器同步过来的每一条记录都打上「这条数据来自哪个连接器」的标记，方便后续做数据溯源审计，同时又不想改动原始的业务字段，应该用哪个 SMT？它是往哪里加信息的？
  A: 应该用 `InsertHeader`：它会在每条消息的**消息头（header，独立于消息键值的一块元数据区域）**里插入一个固定的字符串，比如把消息头字段设为「MessageSource」、值设为连接器的名字。因为信息是加在消息头而不是消息本身的键或值里，原始的业务数据结构完全不受影响，下游想要按需读取这个溯源标记，
- `kafka-connect-smt-timestamprouter-usecase` Q: `TimestampRouter` 这个 SMT 是根据消息的什么信息来改变目标主题的？在什么场景下这种「按时间戳路由」的能力特别有用？
  A: `TimestampRouter` 会根据消息自带的时间戳来决定这条消息最终应该被路由到哪个主题。这在数据池连接器（sink connector）把数据写入下游存储时特别有用：如果下游系统按时间对数据做了分区（比如按天/按月建不同的数据集或分区表），就可以用消息的时间戳自动算出它该落到哪个目标主题（进而对应下游哪个数据
- `kafka-connect-smt-vs-streams-boundary` Q: Kafka Connect 里的单一消息转换（SMT，single message transformation）能不能用来实现「把两个主题的数据按某个字段连接（join）起来」或者「按时间窗口聚合统计」这类需求？为什么不行，应该改用什么？
  A: 不行。SMT 是**无状态**的：它只能基于当前这一条记录本身的内容做加工（改字段类型、遮蔽字段、过滤、改路由主题等），处理时看不到也不记得其他消息，所以天然做不了需要「记住之前见过的数据」才能完成的操作，比如把两个数据源的记录连接起来，或者把一段时间窗口内的多条消息聚合成一个统计值——这些都需要维护跨消息的状态。这类

## connect.alternatives — Connect之外的数据集成选择
理解除Kafka Connect外，其他数据摄入框架、图形化ETL工具与流式处理框架在数据集成中的定位。
- `kafka-connect-alt-flume-logstash-vs-connect` Q: 一个团队的数据架构以 Hadoop 或 ElasticSearch 为中心，Kafka 只是众多数据来源之一；另一个团队的架构以 Kafka 为中心，需要对接大量各种各样的源系统和目标系统。这两种情况分别更适合用 Flume/Logstash 这类系统自带的数据摄入工具，还是用 Kafka Connect？
  A: 以 Hadoop 或 ElasticSearch 为中心、Kafka 只是数据来源之一的架构，更适合继续用它们各自生态原生的摄入工具——Hadoop 用 Flume，ElasticSearch 用 Logstash 或 Fluentd，因为整个数据流的核心枢纽本来就不是 Kafka。反过来，如果架构以 Kafka 为核
- `kafka-connect-alt-gui-etl-tools-tradeoff` Q: Informatica、Talend、Pentaho、Apache NiFi、StreamSets 这类基于图形界面的 ETL 工具也能把 Kafka 当作数据源或数据池使用。如果团队已经在用这类工具搭建数据管道，是不是应该改用 Connect 来对接 Kafka？这类图形化 ETL 工具的主要缺点是什么？
  A: 如果团队已经在用某个图形化 ETL 工具（比如 Pentaho）搭建数据集成流程，通常没有必要仅仅为了接入 Kafka 就额外再引入一套集成工具，继续沿用熟悉的图形化方案即可。这类工具的主要缺点是它们的工作流普遍比较复杂厚重：如果需求只是单纯地把数据从 Kafka 读出来或写进 Kafka，用这种面向复杂可视化流程设计
- `kafka-connect-alt-kafka-as-integration-platform` Q: 可以把 Kafka 定位成一个同时覆盖三类集成需求的平台：{{c1::数据集成——通过 Connect 在 Kafka 与外部数据存储系统之间搬运数据}}、{{c2::应用集成——通过生产者/消费者客户端让自研应用直接读写 Kafka}}、{{c3::流式处理——对流经 Kafka 的数据做实时计算}}。在这个定位下，Kafka 本身可以被当作传统图形化 ETL 工具的一种可行替代方案，而不只是众多数据源之一。
- `kafka-connect-alt-stream-framework-shortcut-risk` Q: 如果本来就打算用某个流式处理框架（比如 Kafka Streams、Flink 等）去处理来自 Kafka 的数据，而这个框架本身也支持直接把处理结果写到外部目标系统，直接让这个框架完成「读取—处理—写出」全流程（不经过 Connect、也不把中间结果落回 Kafka）能省掉什么步骤？这样做会带来什么额外的风险？
  A: 这样做可以省掉「把处理好的结果先写回 Kafka 的某个主题，再单独用连接器把它导出到目标系统」这一步——流式处理框架直接读取 Kafka 数据、处理后一步写入外部系统即可，减少了一次落地和一道额外的组件。代价是一旦在写入目标系统的过程中出现数据丢失或数据损坏，诊断问题会变得更困难：因为处理结果没有像经过 Connec
