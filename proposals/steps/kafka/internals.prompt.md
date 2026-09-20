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
  "internals.controller": ["<id shown first>", "…"],
  "internals.replication-protocol": ["<id shown first>", "…"],
  "internals.request-handling": ["<id shown first>", "…"],
  …
}

## internals.controller — 控制器（controller）的角色与选举
理解控制器在集群中承担的元数据管理与首领选举职责，以及控制器自身如何被选出。
- `kafka-internals-controller-election` Q: 一个 Kafka 集群刚启动，或者当前控制器（controller，负责首领选举的那个 broker）突然下线了。集群是如何选出（新）控制器的？为什么这种方式能保证同一时刻只有一个控制器？
  A: Kafka 依赖 ZooKeeper 里一个固定路径 `/controller` 的**临时节点（ephemeral node）**：临时节点会随创建它的客户端连接断开而自动消失。集群中第一个成功在 `/controller` 创建该节点的 broker 就成为控制器；其余 broker 尝试创建时都会收到「节点已存在
- `kafka-internals-controller-epoch-zombie` Q: 某个控制器（controller）因为一次很长的 JVM 垃圾回收（GC）停顿而与 ZooKeeper 失联，集群趁机选出了新控制器；停顿结束后，旧控制器恢复运行，但它并不知道新控制器已经存在，仍继续向其它 broker 发送指令。Kafka 用什么机制防止这种「僵尸控制器」造成的脑裂（split brain，两个节点同时认为自己是唯一控制器）？
  A: 每当一个新控制器当选，都会通过 ZooKeeper 的条件递增操作获得一个严格更大的**epoch（选举代数，一个单调递增的整数）**，并把这个 epoch 带在自己发出的每条控制消息里。其它 broker 会记住当前已知的最大 epoch：一旦收到的消息里 epoch 比自己记录的小，就直接丢弃。这样，恢复过来的旧控
- `kafka-internals-controller-leader-election-flow` Q: 控制器（controller）通过 ZooKeeper watch 或收到 `ControlledShutdownRequest`（有序关闭请求）发现某个 broker 离开了集群。它接下来要做哪几件事，才能让该 broker 上原来的分区首领恢复对外服务？
  A: 控制器要依次做：1）找出这个下线 broker 上原本是**首领副本（leader replica）**的所有分区；2）为每个这样的分区从其副本集（replica set）里挑一个新首领（简单实现就是取副本列表中的下一个副本）；3）把这些新的首领/ISR（in-sync replicas，同步副本集合）状态以流水线（p
- `kafka-internals-controller-role` Q: 在传统的基于 ZooKeeper（一个协调分布式系统元数据与选主的外部服务）的 Kafka 集群里，「控制器（controller）」和普通 broker（Kafka 服务器节点）是什么关系？它比普通 broker 多承担了什么职责？
  A: 控制器本身也是集群里的一个普通 broker，同样接收生产者/消费者的读写请求；不同之处在于它额外承担了集群范围的元数据管理与**首领选举**：当某个分区的首领副本（leader replica）所在的 broker 下线时，由控制器决定这个分区的新首领是谁，并把这个决定告知集群里其它相关 broker。也就是说，一个
- `kafka-internals-controller-startup-load-latency` Q: 为什么一个分区数很多的 Kafka 集群里，新控制器（controller）当选后往往需要几秒钟才能真正开始工作，而不是瞬间完成？
  A: 新控制器上任后必须先从 ZooKeeper 加载全部主题、分区、副本集的最新状态，之后才能开始管理元数据和执行首领选举。这个加载调用的是异步 API，请求会以「流水线（pipeline）」方式连续发出而不是一条条等待应答，以尽量压低总耗时；但分区数越多，需要拉取和处理的状态越多，所以在分区规模很大的集群里，即便有流水线

## internals.replication-protocol — 复制协议：首领/追随者同步与副本滞后
掌握追随者如何拉取并追赶首领的复制协议，以及副本滞后如何被检测并移出ISR。
- `kafka-internals-follower-fetch-protocol` Q: 在 Kafka 里，跟随者副本（follower replica，不直接处理客户端请求的副本）是通过什么方式跟首领副本（leader replica）保持数据同步的？首领又是怎么据此判断某个跟随者「落后」了多少？
  A: 跟随者会像消费者一样，主动向首领发送 `Fetch` 请求，请求里带着自己想要拉取的下一条消息的偏移量（offset）；这些偏移量是严格递增有序的。首领通过记录每个跟随者最近一次请求的偏移量，就能推算出该副本已经获取到哪里、与最新消息相差多少，从而判断它的复制进度和滞后程度。也就是说，同步进度完全靠跟随者「主动来拉」并
- `kafka-internals-follower-read-highwatermark` Q: Kafka 支持消费者直接从跟随者副本（follower replica）而不是首领副本（leader replica）读取消息（KIP-392），目的是就近读取以降低网络成本。但为什么这种读法仍然只能读到「已提交」的消息，且往往比从首领读要慢一点？
  A: 首领在把消息发给跟随者做复制的同时，会把自己当前的**高水位标记（high watermark，即最近一次被判定为「已提交」的消息偏移量）**一并带过去，跟随者据此知道自己保存的消息里哪些已经被正式提交、可以对外提供。这保证了不论从首领还是跟随者读，读到的都只是已提交消息，可靠性一致。但高水位标记本身需要经过一次网络传
- `kafka-internals-isr-matters-leader-election` Q: 为什么「一个副本是否在 ISR（in-sync replicas，同步副本集合）里」这件事，会直接决定首领（leader）故障时谁能接任新首领？
  A: 只有持续、及时地向首领发送 `Fetch` 请求并追上最新消息的「同步副本」才会被算进 ISR；不同步的副本意味着它没有拿到首领已经确认写入的全部消息。如果首领崩溃，Kafka 只允许从 ISR 中选出新首领，因为只有 ISR 里的副本才能保证不丢失任何已经写入首领的数据；如果允许一个滞后的副本当选，新首领会缺失部分消
- `kafka-internals-isr-out-condition` Q: 一个跟随者副本（follower replica）在什么条件下会被首领判定为「不同步」，从而被移出 ISR（in-sync replicas，同步副本集合）？这个判定标准由哪个参数控制？
  A: 首领会看两件事：一是这个跟随者有没有在最近 `replica.lag.time.max.ms`（默认场景下的滞后时间阈值）配置的时间窗口内发来过 `Fetch` 请求；二是即使发来了请求，它请求的偏移量与首领最新消息的偏移量之间的差距，是否已经超过了这个时间窗口所允许的追赶时间。只要满足其一，这个副本就被认为跟不上首领
- `kafka-internals-preferred-leader-rebalance` Q: Kafka 中的「首选首领（preferred leader）」是什么，为什么 Kafka 会在集群运行一段时间后自动把首领「换回」首选首领，而不是让当前首领一直当下去？
  A: 首选首领是主题创建时，为每个分区在副本列表中排在第一位的那个副本；因为创建分区时 Kafka 会把各分区的首领尽量均匀地分散到不同 broker 上，首选首领天然对应着这种均衡分布。但集群运行中会发生 broker 下线导致首领切换到其它副本，切换久了负载就会往少数 broker 集中。当配置 `auto.leader

## internals.request-handling — broker如何处理生产请求与获取请求
理解broker处理生产请求和获取请求的内部路径，以及请求处理与网络/IO线程的关系。
- `kafka-internals-client-routes-to-leader-via-metadata` Q: Kafka 的生产请求和获取请求必须发给分区的首领副本（leader replica）所在的 broker，但客户端一开始并不知道哪个 broker 是首领，它是怎么找到正确目标的？如果目标选错了会怎样？
  A: 客户端会先发送一种叫**元数据请求（metadata request）**的请求，可以发给集群里任意一个 broker（因为所有 broker 都缓存了完整的集群元数据），得到的响应里列出了每个主题各分区的副本分布和当前首领是谁。客户端把这些信息缓存下来，之后直接把生产/获取请求发给目标分区首领所在的 broker，并
- `kafka-internals-fetch-min-max-bytes-tradeoff` Q: 消费者可以给一次获取请求（fetch request）同时设置「最多返回多少数据」和「至少凑够多少数据才返回」两个参数。为什么需要同时设置这两个看似相反的限制？
  A: 上限（最多返回多少数据）是为了防止 broker 一次性塞进大量数据把消费者的内存撑爆——客户端要为返回的数据预留内存，没有上限就存在被撑爆的风险。下限（比如设成 10 KB）则是为了在主题流量不大时减少来回请求的次数：如果不设下限，消费者可能每隔几毫秒就发一次请求却常常拿到很少甚至没有数据，浪费 CPU 和网络开销；
- `kafka-internals-fetch-only-sees-committed` Q: 分区首领（leader replica）本地磁盘上已经写入了一条新消息，但这条消息还没有被所有同步副本（ISR，in-sync replicas）复制完。这时候一个普通消费者发起获取请求想读这条消息，会发生什么？为什么 Kafka 要这样设计？
  A: 首领不会把这条消息返回给消费者，客户端会收到一个「空」响应而不是错误，要等到消息被所有同步副本复制完之后才能读到。这是因为如果首领在这条消息复制完之前崩溃，另一个副本被选为新首领时并不包含这条消息，它就相当于从未真正写入成功；如果之前已经允许某个消费者读到它，就会出现「有的消费者读到了后来却消失的消息」这种不一致行为。
- `kafka-internals-fetch-zero-copy` Q: Kafka 的 broker 在处理获取请求（fetch request，消费者/跟随者副本用来拉取消息的请求）时，为什么用「零复制（zero-copy）」技术发送消息，它省掉了什么？
  A: 零复制指 broker 把消息直接从磁盘文件（实际常常是 Linux 文件系统缓存）发送到网络通道，中间不经过应用层的任何缓冲区，也就不需要先把数据拷贝进 broker 进程的内存再拷贝出去。相比很多数据库那种「先读进本地缓存、处理后再发送」的做法，零复制省掉了字节复制的开销和内存缓冲区的管理成本，因此获取请求的吞吐和
- `kafka-internals-network-io-thread-pipeline` Q: 客户端一条生产请求（producer request）到达 Kafka 的 broker 后，要经过哪几类线程和队列才能被真正处理？为什么要把「接收连接/收发字节」和「真正处理请求」分成不同的线程？
  A: broker 在每个监听端口上先由一个**接收器线程（acceptor thread）**接受新连接，并把连接交给若干个**处理器线程**（也叫**网络线程**，数量可配置）；网络线程只负责把请求从连接里读出来放进**请求队列**，以及把已经算好的响应从**响应队列**发回客户端。真正解析并执行请求的是另一组 **IO
- `kafka-internals-purgatory-delayed-response` Q: Kafka 里的「炼狱（purgatory，一块临时保存未完成响应的内存区域）」是用来解决什么问题的？举一个会用到它的场景。
  A: 有些请求不能立刻给出响应，因为响应依赖将来才会发生的事件——例如生产者设置 `acks=all`（要求所有同步副本确认才算写入成功）时，broker 收到消息并写入首领后还不能马上应答，必须等所有同步副本（in-sync replicas，ISR）复制完这条消息才能返回成功；再比如消费者的获取请求要求「有足够数据才返回

## internals.storage-segments — 物理存储：分区分配与日志片段（log segment）
掌握分区在磁盘上的分配策略、文件管理方式，以及日志如何被切分为多个片段文件。
- `kafka-internals-active-segment-retention` Q: 某主题的保留时间配置为 1 天，但因为消息量小，某个片段（segment）实际跨越了 5 天才写满被关闭。这 5 天的数据会在第 1 天后就被删除吗？为什么？
  A: 不会，这 5 天的数据要等到整整 5 天后（片段被关闭之时）才可能进入删除流程。原因是 Kafka 的保留策略是以**片段**为单位执行的：当前正在被写入的片段叫**活动片段（active segment）**，活动片段永远不会被删除，哪怕里面已经有消息早就超过了配置的保留期限，也必须等它被写满关闭、成为非活动片段后，
- `kafka-internals-log-segment-basics` Q: Kafka 为什么要把一个分区的数据切分成多个「片段（segment）」文件，而不是一直写在一个大文件里？默认情况下什么时候会切出一个新片段？
  A: 如果一个分区始终只有一个文件，无论是按时间/大小删除旧数据，还是定位某个偏移量，都要在一个不断增长的大文件里操作，既慢又容易出错。所以 Kafka 把分区拆成多个片段文件：broker 写入数据时，一旦当前片段达到大小上限（默认 1 GB）或时间上限（默认一周），以先到者为准，就关闭这个片段，开一个新片段继续写。这样删
- `kafka-internals-open-file-handles` Q: 一个 Kafka broker 往往要为分区维护许多个日志片段（log segment）文件，这会给操作系统层面带来什么运维上的注意点？
  A: broker 会为分区的每一个已打开的日志片段分配一个文件句柄（file handle），哪怕这个片段已经不是当前正在写入的活动片段、只是保留期内的历史数据。当一个 broker 上分区和片段数量都很多时，同时打开的文件句柄数会相当可观，因此需要针对操作系统的文件句柄上限等参数做相应调优，否则可能因句柄耗尽而出问题。
- `kafka-internals-partition-allocation-goals` Q: Kafka 在创建一个新主题时，要把它的所有分区副本分配到集群里的各个 broker 上。这个分配过程要同时满足哪几个目标？
  A: 三个目标：1）**broker 间副本数量均衡**——比如 6 个 broker、10 个分区、复制系数（replication factor）3，一共 30 个副本，理想情况下每个 broker 分到 5 个；2）**同一分区的多个副本不能落在同一个 broker 上**——否则那个 broker 一旦下线，这个分区
- `kafka-internals-partition-allocation-roundrobin` Q: Kafka 具体是怎样把一个分区的首领副本和跟随者副本分配到不同 broker 上的？在没有配置机架信息，和配置了机架信息两种情况下有什么区别？
  A: 没有机架信息时：先随机挑一个起始 broker，然后用轮询（round robin）方式依次把各分区的首领副本分配给 broker 列表中的下一个 broker；对每个分区，再从它的首领所在 broker 开始，按 broker 编号顺序依次分配跟随者副本。配置了机架信息（Kafka 0.10.0 起支持）时，brok
- `kafka-internals-partition-disk-assignment` Q: 一个 broker 上通常配置了多个存放分区数据的目录（`log.dirs`，对应多块磁盘或挂载点）。给一个新分区选目录时，Kafka 用的是什么规则？这个规则有什么局限？
  A: 规则很简单：统计每个目录当前已有的分区**数量**，新分区总是被放进分区数量最少的那个目录；因此如果给 broker 新加一块磁盘，后续新建的分区会持续优先落到这块新盘，直到数量重新拉平。局限在于这个规则只看分区**个数**，不看每个目录的可用空间或者各分区的实际大小——如果集群里新旧服务器混用、磁盘大小不一，或者有些

## internals.indexes — 索引：偏移量索引与时间索引
理解偏移量索引和时间索引如何让broker在不扫描整个日志的情况下快速定位消息。
- `kafka-internals-index-corruption-recovery` Q: 偏移量索引或时间索引文件如果损坏了，或者管理员手动把它删除了，Kafka 会丢失定位消息的能力吗？为什么说手动删除索引「绝对安全」？
  A: 不会永久丢失。Kafka 并不为索引文件维护校验和（checksum），一旦发现索引损坏，它会重新扫描一遍对应的日志片段，边读消息边记录每条消息的偏移量和文件位置，从而重新生成索引；管理员即便主动删除索引文件也是安全的，因为 Kafka 会自动检测到索引缺失并重建，唯一的代价是重建过程需要重新扫描日志，如果数据量很大，
- `kafka-internals-index-segmented-with-log` Q: Kafka 的日志片段（log segment）会随着数据被删除而整体清理掉；那配套的偏移量索引和时间索引要怎么处理，才不会留下指向已删除数据的悬空条目？
  A: 索引本身也和日志一样被切分成对应的片段：每个日志片段都有自己配套的一段索引文件。当某个日志片段因为超出保留期限被删除时，与它对应的那部分索引也一起被删除，两者是绑定在一起管理的，因此不会出现索引残留、指向已经不存在的日志片段的情况。
- `kafka-internals-offset-index-purpose` Q: 消费者要求从偏移量（offset，消息在分区里的位置编号）100 开始读 1 MB 消息，而这个偏移量可能落在分区众多日志片段（log segment）文件中的任意一个里。如果没有额外的索引结构，broker 要怎么找到它，为什么这样做不可取？
  A: 没有索引的话，broker 只能从某个片段的文件开头开始顺序扫描，逐条读取消息、累加它们占的字节数，直到找到目标偏移量对应的那条消息——分区数据量越大，这种线性扫描越慢。为此 Kafka 为每个分区维护一个**偏移量索引**，直接记录「某个偏移量」到「它在哪个片段文件、文件内哪个字节位置」的映射，使 broker 能一
- `kafka-internals-time-index-purpose` Q: 除了按偏移量（offset）查找消息，Kafka 还支持「给我某个时间戳之后的消息」这样的按时间查找需求，例如 Kafka Streams（Kafka 提供的流处理库）和某些故障转移场景就要用到。Kafka 靠什么机制支持这种查找，而不用整分区扫描时间戳？
  A: Kafka 为每个分区额外维护了一个**时间索引**，它建立的是「时间戳 → 消息偏移量」的映射。要按时间戳查找消息时，broker 先用时间索引把时间戳换算成对应的偏移量，再用偏移量索引（把偏移量映射到片段文件及文件内位置）定位到具体数据，两级索引配合，避免了对整个分区做逐条扫描来比对时间戳。

## internals.compaction — 日志压实（log compaction）
掌握日志压实保留每个键最新值的原理、执行时机，以及它与基于时间/大小保留策略的适用场景差异。
- `kafka-internals-compact-vs-delete-policy` Q: 一个应用把每个用户的「当前状态」不断写入 Kafka 主题（同一个用户对应同一个消息键），应用故障恢复时只想读到每个用户**最新**的状态，不关心历史上所有的中间变化。这种场景应该给主题配置什么保留策略，为什么普通的按时间删除策略不合适，以及这个策略有什么前提条件？
  A: 应该把主题的保留策略设为 `compact`（压实），它只为每个消息键保留最新的一条值，旧值会在后续压实中被丢弃，天然契合「只关心最新状态」的场景；而按时间删除的 `delete` 策略只会删掉超过保留期限的旧消息，无法做到「同一个键只留最新一条」——它删的是「老」而不是「同键的重复」。使用 `compact` 有一个
- `kafka-internals-compaction-clean-dirty-map` Q: Kafka 执行压实（compaction）时，把日志片段分成「干净部分」和「浑浊部分」，压实线程具体是怎么利用内存里的一张 map 来完成去重的？为什么说这个过程对内存很省？
  A: 「浑浊部分」是上一次压实之后新写入、还没有去重的消息，「干净部分」是已经压实过、每个键只剩一条最新值的部分。压实线程先扫描浑浊部分，为每个键在内存里的 map 中记下「键的哈希值（16 字节）→ 该键最新一条消息的偏移量（8 字节）」，每条记录只占 24 字节，即使有大量消息，只要键的种类不太多，map 也很小（例如 
- `kafka-internals-compaction-map-memory-limit` Q: Kafka 管理员给压实线程分配的 map 内存，如果连一个日志片段（log segment）浑浊部分的全部键都放不下，会发生什么？管理员有哪两种解决办法？
  A: Kafka 并不要求这张去重用的 map 能装下整个分区浑浊部分的所有键，但至少要能装下**一个片段**的浑浊部分，否则会报错，压实无法正常进行。管理员的解决办法有两种：一是调大分配给压实线程的 map 内存总量（这个内存是所有压实线程共享分配的，比如 1 GB 内存配 5 个线程，每个线程平均可用 200 MB）；二
- `kafka-internals-compaction-tombstone` Q: 要把某个键在压实主题（启用 `compact` 保留策略的主题）里彻底删除（例如用户注销后按法律要求清除其数据），应用应该怎么做？Kafka 内部是怎么处理这类「删除」消息，让消费者不会错过删除通知的？
  A: 应用需要发送一条键为该用户、**值为 null** 的消息，这条消息被称为**墓碑消息（tombstone）**。压实线程遇到墓碑消息时，照常执行常规压实（丢弃这个键的所有旧值），但会保留这条值为 null 的墓碑消息本身一段配置好的时间，而不是立刻删除。这段保留期让所有消费者都有机会读到这条消息、发现该键的值已经被置
- `kafka-internals-compaction-trigger-and-lag-config` Q: Kafka 默认不是消息一写入就立刻压实，而是攒到「浑浊率」（浑浊消息占分区总消息的比例）达到一定程度才触发一轮压实。这个默认阈值是多少，为什么不设得更低或更高？另外，`min.compaction.lag.ms` 和 `max.compaction.lag.ms` 各自约束什么？
  A: 默认阈值是 50%：阈值太低会让压实过于频繁，压实本身要占用 CPU/IO 并影响主题的读写性能；阈值太高则会让浑浊（未去重）的数据长期占用磁盘空间。50% 是一个折中值，管理员也可以调整。两个滞后参数控制的是时间边界而非比例：`min.compaction.lag.ms` 保证一条消息写入后至少要经过这么久才**可以
- `kafka-internals-delete-and-compact-combo` Q: 如果既想「只保留每个键的最新值」，又想「超过一定时间的数据无论新旧都必须被删除」（比如出于合规要求），单独用 `compact` 策略够吗？Kafka 提供了什么组合方案？
  A: 单独用 `compact` 不够：它只保证同一个键只留一条最新记录，但不会因为时间到了就把这条最新记录删掉，所以压实主题理论上可以无限增长（只要键不断变化）。Kafka 提供了 `delete.and.compact` 组合策略：一方面像 `compact` 一样为每个键只保留最新值，另一方面像 `delete` 一样

## internals.kraft-mode — KRaft模式与ZooKeeper的移除
理解Kafka 3.3+/4.0用基于Raft的KRaft控制器取代ZooKeeper后，元数据管理与控制器选举方式发生的根本变化。
- `kafka-internals-kraft-active-standby-controller` Q: 在 KRaft 架构下，多个控制器节点组成一个 Raft 仲裁（quorum）。这些控制器节点里谁负责真正处理请求？为什么控制器发生故障转移（failover，故障后切换到另一节点）时能很快恢复，而不像传统架构那样需要重新从头加载？
  A: Raft 选出的首领节点被称为**主控制器（active controller）**，只有它负责处理所有来自 broker 的 RPC（远程调用）请求；其余控制器节点是**跟随者控制器**，持续从主控制器复制元数据日志，充当热备。因为跟随者控制器本来就在实时同步、掌握最新状态，一旦主控制器故障需要切换，新的主控制器几乎
- `kafka-internals-kraft-broker-fencing` Q: 在 KRaft 架构中，一个 broker 注册到控制器仲裁（controller quorum）之后即使被关闭下线，注册状态也不会自动消失，要靠管理员显式注销。如果一个 broker 还在线，但没能及时跟上最新元数据，会发生什么？这样设计是为了防止什么问题？
  A: 这种在线但元数据落后的 broker 会被**隔离（fenced）**，不允许再处理来自客户端的请求。这是为了防止客户端把请求发给一个「已经不是分区首领、但自己还不知道」的过时节点——如果不隔离，客户端可能凭旧元数据继续往一个早已失去首领身份的 broker 写消息或读消息，从而读写失败或造成数据不一致。
- `kafka-internals-kraft-metadata-as-log` Q: KRaft（基于 Raft 的新控制器架构）用什么方式取代了 ZooKeeper 原来保存集群元数据（主题、分区、ISR、配置等）的角色？为什么选这种方式？
  A: KRaft 把集群元数据的每一次变更都表示成一个事件，写进一份由控制器节点共同维护的**元数据事件日志**——这正是 Kafka 本身最擅长的「基于日志的架构」：状态变化被表示成一串有序事件流，任何一方都可以通过重放（replay）这份日志追上最新状态。原来保存在 ZooKeeper 里的一切都被搬进了这份日志，好处是
- `kafka-internals-kraft-motivation` Q: Kafka 社区从 2019 年开始用基于 Raft（一种分布式一致性算法）的 KRaft 控制器取代基于 ZooKeeper（外部协调服务）的传统控制器。抛开「少依赖一个外部系统」，主要的技术性动因有哪些？
  A: 主要有三条：1）传统架构下，元数据虽然同步写入 ZooKeeper，但同步给各 broker 以及 broker 从 ZooKeeper 接收更新都是**异步**的，多环节异步容易导致 broker、控制器、ZooKeeper 三者的元数据出现难以检测的不一致；2）控制器重启时要从 ZooKeeper 完整读出所有 b
- `kafka-internals-kraft-pull-metadata-fetch` Q: 传统架构里，控制器用 `UpdateMetadata` 请求主动把元数据变更**推送**给各个 broker。KRaft 架构把这个方向反过来了，用的是什么新接口，为什么这样对大规模集群更友好？
  A: KRaft 下 broker 改用新的 **MetadataFetchAPI** 主动向主控制器**拉取（pull）**元数据更新，机制类似消费者的获取请求：broker 记录自己已经拉到的元数据偏移量，每次只请求比这个偏移量更新的部分，而不是被动等待推送全部内容。broker 还会把拉到的元数据持久化到本地磁盘上，这

## internals.tiered-storage — 分层存储（tiered storage, KIP-405）
理解分层存储如何把冷数据下沉到低成本对象存储，从而把日志保留期与broker本地磁盘容量解耦。
- `kafka-internals-tiered-storage-decouple-storage-compute` Q: 分层存储让 Kafka 集群「延长数据保留时间」这件事不再需要「扩大集群」，具体是通过什么方式实现存储与计算（CPU/内存）的解耦，还带来了哪些附加好处？
  A: 远程存储层用的是 HDFS、S3 这类可以独立于 broker 计算资源扩展的专用存储系统，所以要延长整体数据保留期只需要在远程层多存数据，不需要给 broker 加磁盘或加节点，实现了存储容量扩展与 CPU/内存扩展的解耦。附加好处还有：留在 broker 本地的数据量变小，故障恢复和再均衡（rebalance）时需
- `kafka-internals-tiered-storage-isolation-benchmark` Q: KIP-405 的性能测试里，对比「有无分层存储」两种场景下消费者读取旧数据对延迟的影响：无分层存储时，正常读取和读旧数据的延迟分别是 21 毫秒和 60 毫秒；启用分层存储后，正常读取变为约 25 毫秒，读旧数据变为约 42 毫秒。为什么分层存储能显著缓解「读旧数据拖慢整体延迟」这个问题？
  A: 没有分层存储时，读旧数据和读最新数据都要争用同一份本地磁盘 I/O 和同一块操作系统页面缓存（page cache），大量读旧数据会把本该留给最新数据的页面缓存挤出去，拖慢正常读取，也拖慢自己（因为要去磁盘读冷数据）。启用分层存储后，旧数据的读请求走网络从远程存储系统读取，不再和本地磁盘 I/O、页面缓存竞争，页面缓存
- `kafka-internals-tiered-storage-motivation` Q: 在传统 Kafka 架构里，所有日志片段都保存在 broker 的本地磁盘上。这种「只有本地磁盘一层存储」的设计，在需要长期保留海量数据时会带来哪几个具体问题？
  A: 三个问题：1）一个分区能存多少数据受限于单个挂载点的物理磁盘容量，分区数量因此不仅由业务需求决定，也被磁盘大小卡住；2）如果为了满足存储需求而配大磁盘/大集群，集群规模往往会超过延迟和吞吐量本身所需要的规模，造成成本浪费；3）在 broker 间迁移分区（比如扩缩容）所需要的时间由分区大小决定，分区越大，集群在扩缩容时
- `kafka-internals-tiered-storage-read-path-choice` Q: 开启了分层存储的 Kafka 集群里，一个对延迟敏感的实时消费应用，和一个需要回填/故障恢复读取历史数据的应用，分别应该期望自己的读请求落在本地存储层还是远程存储层？为什么？
  A: 对延迟敏感、只关心最新消息的应用通常读的是分区**尾部**（最近写入的数据），这部分数据还留在本地存储层，可以受益于 Kafka 现有的存储机制（尤其是操作系统页面缓存 page cache），延迟低；而做数据回填或故障恢复的应用往往需要读很久以前的**旧数据**，这些数据已经从本地层过期、只存在于远程存储层，只能通过
- `kafka-internals-tiered-storage-two-layers` Q: 分层存储（tiered storage，KIP-405）给 Kafka 集群引入了「本地存储层」和「远程存储层」两层。这两层分别用什么介质，各自的保留时间设置通常有什么差异？
  A: 本地存储层和以前一样，用 broker 自己的本地磁盘保存日志片段（log segment）；远程存储层则把日志片段存到 HDFS、S3 这类专用的低成本对象存储系统里，两层可以分别配置各自的保留策略。因为本地磁盘的单位存储成本明显高于远程对象存储，本地层的保留时间通常只设几小时甚至更短，远程层则可以设成几天甚至几个月
