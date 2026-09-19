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
  "monitoring.metrics-and-slo": ["<id shown first>", "…"],
  "monitoring.broker-metrics": ["<id shown first>", "…"],
  "monitoring.client-metrics": ["<id shown first>", "…"],
  …
}

## monitoring.metrics-and-slo — 指标基础与服务级别目标（SLO）
理解Kafka指标的来源与应用健康检测方法，以及如何把关键指标转化为SLI/SLO并驱动告警。
- `kafka-monitoring-alert-vs-debug-metrics-retention` Q: Kafka 指标按用途可以分成「用于告警」和「用于调试问题」两类，这两类指标在保留时间和客观性要求上有什么不同？为什么要这样区分？
  A: 用于告警的指标只需要保留很短的时间（通常不超过响应问题所需的时长，以小时或天为单位），它们要发给能立刻处理已知问题的自动化工具或运维人员，所以要求尽量客观，且只关注真正影响客户的问题。用于调试的数据则需要保留几天到几周，因为经常要拿它排查一个已经存在一段时间、或比较复杂的问题，且不一定要接入监控系统长期采集——只要在需
- `kafka-monitoring-automation-vs-human-metrics` Q: 同样是采集 Kafka 指标，给自动化系统使用和给人（比如运维人员）看，在指标的「具体程度」和数量上应该有什么不同的设计原则？为什么给人看的指标太多反而是坏事？
  A: 给自动化系统用的指标可以尽量具体、细粒度：越具体的指标解释空间越小，越容易写成明确的自动化判断逻辑，而处理海量细节数据本来就是计算机的强项。但如果把同样海量、琐碎的指标直接暴露给人去做告警判断，人会难以承受，容易陷入「告警疲劳」——警报太多、经常误报，会让人逐渐怀疑告警本身是否还能反映系统真实状态，也很难持续维护每个指
- `kafka-monitoring-health-check-stale-metrics-tradeoff` Q: 检测 Kafka broker 是否健康有两种常见方式：一种是用外部进程主动探测 broker（比如尝试连接它对外的端口看是否有响应），另一种是「broker 一段时间没有上报任何指标就告警」（也叫过时指标检测）。为什么说第二种方式虽然可行，但存在一个明显的局限？
  A: 「过时指标」检测依赖监控系统本身持续、正常地收到 broker 上报的数据，一旦发现指标停止更新就报警；但这时候很难分清究竟是 broker 本身出了故障，还是采集或传输指标的监控链路（比如采集代理、网络、监控系统本身）出了问题——两种原因看起来是一样的现象。相比之下，直接用外部进程连接 broker 对客户端开放的那
- `kafka-monitoring-percentile-bad-sli` Q: 为什么「响应时间的第90百分位数（P90）」这类分位数指标不适合直接当作衡量服务可靠性的 SLI（服务级别指标），更好的做法是什么？
  A: 好的 SLI 最好能针对**每一个具体事件**单独判断它是否满足 SLO（服务级别目标）阈值——例如「这次请求是否在10毫秒内完成」，这样就能直接数出满足/不满足阈值的事件数量算比率。而 P90 这类分位数指标只会告诉你「90%的事件低于某个具体的值」，但这个具体的值本身是随数据分布浮动的，你并不能提前设定并检验它是否
- `kafka-monitoring-sli-slo-sla-ola-terms` Q: 工程师、经理、高管常常混用「服务级别」相关的术语。SLI（服务级别指标）、SLO（服务级别目标，也叫SLT）、SLA（服务级别协议）、OLA（运营级别协议）这四个术语分别描述的是什么，它们之间是什么关系？
  A: SLI（service level indicator）是描述服务可靠性的一个客观指标，通常表示为「正常事件数/总事件数」的比率，比如 Web 服务器返回 2xx/3xx/4xx 响应的请求占比。SLO（service level objective，也叫 SLT，service level threshold）是把一
- `kafka-monitoring-slo-burn-rate-alerting` Q: 一个 SLO 规定「每周 99.9% 的请求要在10毫秒内返回首字节」，为什么不能等到这个每周 SLO 快要被违反、甚至已经违反的那一刻才触发告警？建议用什么指标来提前发现问题？
  A: SLO 的统计窗口通常比较长（比如一周），如果直接拿「这周还剩多少违规配额」作为告警条件，往往要等到临近周末、大量违规请求已经发生之后才会触发，这时候造成的影响已经无法挽回，属于「发现得太晚」。更好的做法是监控 SLO 的**燃烧率**（burn rate，即当前不满足 SLO 阈值的事件发生速度）：例如正常情况下每小

## monitoring.broker-metrics — broker指标与集群问题诊断
掌握用broker指标（含非同步分区）诊断集群问题的方法，以及JVM与操作系统层面需要关注的监控项。
- `kafka-monitoring-find-culprit-broker-multi-urp` Q: 用 `kafka-topics.sh --describe --under-replicated` 发现有好几个不同主题、不同分区都处于非同步状态，涉及的首领分布在不同 broker 上，此时怎么快速判断问题的根源出在哪一个 broker，而不是整个集群？
  A: 把所有非同步分区的 ISR（同步副本集合）和完整副本清单列出来对比，找出哪个 broker 编号**没有出现在任何一条非同步分区的 ISR 里，却出现在所有这些分区的完整副本清单中**——这说明其他 broker 都能正常互相复制，唯独这个 broker 一直无法从别的副本那里把数据复制过来（或者一直不能被别的副本复制
- `kafka-monitoring-outbound-vs-inbound-bytes` Q: 很多 Kafka 集群里，主题的「流出字节速率」（broker 发给消费者和跟随者副本的数据速率）经常能达到「流入字节速率」（生产者写入 broker 的数据速率）的好几倍，甚至6倍。这是什么原因造成的？为什么设置流出流量的告警阈值时要特别留意这一点？
  A: 流出字节速率不仅包含消费者读取消息产生的流量，还包含 broker 之间为了维持副本同步而产生的复制流量：如果一个主题的复制系数是 N，那么即使完全没有消费者在读取，光是把消息从首领复制到其余 N-1 个跟随者副本，流出速率就已经相当于流入速率的 N-1 倍（连同首领自身写入，整体等价关系近似 N 倍上下）；如果再叠加
- `kafka-monitoring-request-handler-idle-and-msg-format` Q: 「请求处理线程空闲率」这个指标低于多少通常说明存在潜在问题，低于多少说明已经出现明显的性能问题？除了线程数配置不够（一般应等于 broker 的 CPU 核数），Kafka 0.10 引入的哪项改动显著减轻了这个线程池的负担？
  A: 经验上，请求处理线程空闲率低于 20% 说明存在潜在问题，低于 10% 说明已经出现了明显的性能问题。在 Kafka 0.10 之前，请求处理线程（负责真正处理来自客户端的请求，包括读写磁盘）在处理生产请求时还要负责解压缩消息批次、验证消息、重新分配偏移量，并在写盘前用带同步锁的方式重新压缩，非常消耗这个线程池的资源；
- `kafka-monitoring-two-active-controllers` Q: 「活跃控制器数量」这个指标在正常情况下应该在整个集群里加起来恒等于1（只有一个 broker 报告自己是控制器）。如果监控发现集群里同时有两个 broker 都把这个指标报告为1，说明出了什么问题？该如何解决？
  A: 这说明本该退出控制器角色的旧控制器线程被卡住了（阻塞），没能正常释放控制器身份，导致新选出的控制器和这个卡住的旧控制器同时都以为自己是集群唯一的控制器。这会导致创建主题、移动分区之类的管理操作无法正常执行，因为两个控制器可能给出互相冲突的决策。由于旧控制器线程已经被卡住，往往无法通过正常方式安全地重启它所在的 brok
- `kafka-monitoring-urp-not-a-good-alert` Q: 非同步分区（under-replicated partitions，URP，指首领 broker 上有多少分区的部分副本没有跟上首领进度）数量是 Kafka 最常被提及的监控指标，但现在不再建议把它直接用作主要的告警指标，为什么？应该用什么替代？
  A: URP 能反映从 broker 崩溃到资源过度消耗等各种各样的问题，但也正因为原因太多，在很多完全良性的操作场景下（比如正常的集群维护、部署、分区重分配）它也会短暂变成非零值。如果直接拿 URP 非零就告警，会频繁产生误报，久而久之运维人员会开始忽略这类告警，真正严重的问题反而被掩盖；而且要正确解读 URP 具体代表什
- `kafka-monitoring-urp-stable-vs-fluctuating` Q: 发现集群的非同步分区（URP）数量持续维持在一个稳定不变的数值，和这个数值一直在上下波动，这两种表现分别通常指向什么完全不同的根因？
  A: 如果 URP 数量长期稳定不变，很可能是集群中有某个 broker 已经彻底离线：整个集群的 URP 数量恰好等于这个离线 broker 上的分区数量，因为离线的 broker 不会再产生任何指标，它负责的这些分区就会一直停留在「非同步」状态，直到这个 broker 的硬件、操作系统或 Java 层面的问题被解决并重新

## monitoring.client-metrics — 客户端监控：生产者、消费者指标与配额
掌握生产者与消费者关键指标的含义，以及配额（quota）机制如何限制客户端对broker资源的占用。
- `kafka-monitoring-consumer-rate-min-alert-pitfall` Q: 有人给消费者的 bytes-consumed-rate 或 records-consumed-rate 设置了「低于某个最小值就告警」的规则，想以此检测消费者工作负载不足的问题，为什么这样做容易产生误报？
  A: 消费者读取消息的速率在很大程度上取决于生产者当前有没有在正常写入数据——如果某段时间恰好生产者流量低甚至没有新消息可读，消费者的消费速率自然也会跟着降低到接近零，这并不代表消费者本身出了问题。给消费速率设置最小值告警，实际上隐含了「生产者流量应该一直保持在某个水平」这个假设，一旦这个假设不成立（比如业务本身就有低峰期）
- `kafka-monitoring-quota-three-types` Q: Kafka 的配额（quota，限制客户端能占用多少 broker 资源）机制支持三种类型：{{c1::生产配额（producer quota），限制客户端每秒能向 broker 发送多少字节}}、{{c2::消费配额（consumer quota），限制客户端每秒能从 broker 读取多少字节}}、{{c3::请求配额（request quota），限制 broker 花在处理这个客户端请求上的时间占比}}。
- `kafka-monitoring-record-error-vs-retry-rate` Q: Kafka 生产者提供 record-error-rate 和 record-retry-rate 两个指标，为什么前者比后者更值得设置告警？
  A: record-retry-rate 反映的是消息重试的频率——生产者配置了重试次数和退避策略，遇到可重试的错误（比如短暂的网络抖动）会自动重发，这是一种正常、预期内的行为，本身不代表出了严重问题。而 record-error-rate 表示消息在重试次数用尽后仍然发送失败、最终被生产者**丢弃**的比率，正常情况下这个
- `kafka-monitoring-records-lag-max-not-recommended` Q: 消费者的获取请求管理器（fetch request manager）提供了一个 records-lag-max 指标，能直接反映消费滞后（消费者偏移量和 broker 日志结束偏移量之间的差值）。为什么不建议把它当作监控消费滞后的首选指标？
  A: 这个指标有两个局限：一是它只能反映**单个分区**的最大滞后，如果消费者读取多个分区，看不到每个分区各自的滞后情况，也拿不到跨消费者群组的全局视图；二是它依赖消费者客户端自身的内部实现细节，不同客户端或版本的行为可能不一致，不够可靠和通用。因此更好的做法是使用专门的外部消费滞后监控工具，从 broker 侧独立计算每个
- `kafka-monitoring-static-vs-dynamic-quota` Q: 配置 Kafka 客户端配额既可以写在 broker 静态配置文件里（如 `quota.producer.default`），也可以用 `kafka-configs.sh` 或 AdminClient 动态设置。为什么说「特定客户端的配额通常采用动态配置」而不是写进静态配置文件？
  A: 写在 broker 配置文件里的配额是静态的，任何修改都需要重启所有 broker 才能生效；但实际业务里客户端是不断有新的加入、旧的下线的，如果每次要给某个新客户端单独设定配额都必须重启整个集群，运维成本极高而且有风险。动态配置则可以通过命令行工具或 AdminClient 在线修改某个客户端 ID 或用户的配额，不
- `kafka-monitoring-throttle-silent-must-monitor` Q: 当一个生产者或消费者客户端的流量超出了配额被 broker 节流（throttle）时，broker 返回给客户端的响应里会不会带一个「你被限流了」的错误码？这对监控策略意味着什么？
  A: 不会。broker 节流的方式是延迟响应客户端的请求，而不是在响应里携带专门的节流错误码，所以从应用程序的角度看，被节流只表现为请求变慢，程序本身根本不知道这是配额限制造成的还是别的原因造成的。这意味着如果不主动监控 `produce-throttle-time-avg`、`fetch-throttle-time-av

## monitoring.lag-e2e — 消费滞后监控与端到端监控
理解消费滞后（consumer lag）的监控方法，以及端到端监控如何验证消息从生产到消费的完整链路健康。
- `kafka-monitoring-burrow-no-static-threshold` Q: 开源工具 Burrow 用于监控消费者滞后时，相比「给每个分区手动设一个滞后条数阈值再告警」的做法，它是怎么判断一个消费者群组是否健康、是否变慢或已经停止工作的？
  A: Burrow 不需要为每个分区预先配置一个静态的滞后数量阈值，而是持续跟踪消费者群组在每个分区上提交偏移量的变化趋势，通过分析这个变化过程本身（比如偏移量是否还在稳定推进、推进速度是否在变慢、是否完全停止推进）来判断这个群组当前处于正常、滞后、变慢还是已经停止工作的状态。这样即使不同分区吞吐量差异巨大，也不需要人工为每
- `kafka-monitoring-burrow-vs-xinfra-scope` Q: 同样是 LinkedIn 开源的外部监控工具，Burrow 和 Xinfra Monitor（原 Kafka Monitor）各自负责回答什么不同的问题？
  A: Burrow 关注的是「消费端」问题：它对比 broker 上分区的最新偏移量和各个消费者群组已提交的偏移量，判断某个消费者群组是不是正常、是不是滞后或已经停止工作，回答的是「这个消费者群组是不是把消息消费到位了」。Xinfra Monitor 关注的是「集群本身能不能正常读写」这个更基础的问题：它主动向一个跨越所有 
- `kafka-monitoring-e2e-two-questions` Q: 即使已经在监控生产者和消费者客户端的各项延迟指标，为什么还需要单独做一次「端到端监控」，去回答哪两个具体问题？
  A: 生产者/消费者客户端指标（比如请求延迟）虽然能反映出「可能」有问题，但延迟升高到底是客户端本身的问题、网络问题，还是 Kafka 集群本身的问题，单看这些指标只能猜测，无法确定。端到端监控从一个完全独立于具体业务客户端的外部视角，直接去验证两个最根本的问题：「现在还能不能向 Kafka 集群写入消息？」和「现在还能不能
- `kafka-monitoring-external-lag-tool-vs-client-metric` Q: 消费者客户端自己提供了 records-lag-max 这个滞后指标，但监控消费滞后（consumer lag，消费者当前读到的位置和分区最新消息之间的差值）最好用外部工具而不是这个客户端指标，具体有哪两个原因？
  A: 第一，records-lag-max 只反映消费者读取的**所有分区里滞后最大的那一个**分区的数值，看不到其他分区各自的滞后情况，无法拼出消费者的整体滞后视图。第二，这个指标是消费者在处理每次获取（fetch）请求时自己顺带计算出来的，一旦消费者本身崩溃、卡住或离线，它要么不再更新变得不准确，要么干脆拿不到——而消费
- `kafka-monitoring-lag-threshold-per-partition-problem` Q: 如果直接用命令行工具输出的滞后消息条数（绝对数量）来做告警，为什么给所有分区设置同一个固定阈值是不合理的？
  A: 「滞后了多少条消息」这个绝对数字的严重程度完全取决于这个分区本身的消息生成速率：一个每小时只收到100条消息的主题，滞后100条可能意味着消费者已经停摆了一小时；而一个每秒能收到10万条消息的主题，滞后100条只是几毫秒的正常波动。用同一个固定阈值套用到吞吐量差异巨大的所有分区上，要么对低速主题反应迟钝，要么对高速主题
- `kafka-monitoring-xinfra-per-broker-not-per-topic` Q: 理想情况下，端到端监控应该对集群里每一个主题都验证一遍读写是否正常，但 Xinfra Monitor（原名 Kafka Monitor）这类工具实际上把验证粒度下沉到了 broker 级别而不是主题级别，为什么？
  A: 如果要对集群里的每一个真实业务主题都专门注入一份人工合成流量来验证读写，主题数量一多（可能成百上千个），这种做法的开销和复杂度会变得不现实。折中的办法是构造一个横跨集群所有 broker 的专用主题，持续向这个主题的每个 broker 生成并读取消息，以此监控每个 broker 上生产请求和读取请求的可用性以及读写之间
