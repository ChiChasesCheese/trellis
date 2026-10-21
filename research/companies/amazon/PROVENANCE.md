# Amazon 学习材料的出处留档（开发用，不在 Obsidian 里）

清理前的完整版本见 commit `513b6233`（2026-10-17）。下面按文件抽出原来的来源 / 出处小节。

---

## `vault/interviews/core/system-design/amazon/hld_sketches.md`
> 来源：`../catalog/raw/forums.md` §3.3 / §4.4（2025-01..2026-10 的候选人报告）。**这是骨架（sketch），不是完整题解**：每个只给需求关键点、数据模型、4–5 个关键决策、

---

## `vault/interviews/core/system-design/amazon/problems/serverless_query_over_s3.md`
> 来源说明：Athena 官方文档称 "serverless … you pay only for the queries you run"（https://docs.aws.amazon.com/athena/latest/ug/what-is.html ，2026-10-15 抓取）；SQL 查询按扫描数据量计费（定价页另有 Provisioned Capacity 按计算计费的选项）；定价页示例按 $5/TB 计算（3 TB 未压缩文本 = $15；GZIP 后 1 TB = $5；Parquet+压缩只读一列 0.25 TB = $1.25，说明计费的是实际读取的压缩/列裁剪后字节），实际单价按区域而异，面试里不要报具体单价（来源：https://aws.amazon.com/athena/pricing/ ，经 r.jina.ai 镜像读取，2026-10-15 核对）。

---

## `vault/interviews/core/system-design/amazon/sd-index.md`
## 来源

- 题目来自 2026-09-16..10-16 一亩三分地与 Hello Interview 上 Amazon 候选人的报告（不含 OA）；逐条记录见
  `interviews/companies/amazon/catalog/raw/1p3a_2026-10-16.md` 与 `hellointerview_2026-10-16.md`。每篇题解的最后一节写明该题
  的具体出处、日期、级别、置信度，以及题面里哪些是根据有限信息补全的。
- 学习顺序依据：Hello Interview 上 Amazon Lockers 累计 14 条报告、URL Shortener 累计 12 条，是 Amazon 系统设计题里最常见的两道；
  SD01 另有一亩三分地 2026-10-02 现场轮的报告。
- 30 天窗口外但长期高频的 Amazon 系统设计题（本批未写，可先读通用题解）：实时协作文档 14 条（[[solution-google-docs]]）、
  停车场管理 11 条、网约车 9 条（[[solution-ride-hailing]]）、大规模通知系统 7 条（[[solution-notification-system]]）。
- 另有两条系统设计轮的报告内容被隐藏、看不到题目；一亩三分地的一篇整理帖提到 SDE-2 的 OA 里有 15–20 分钟的系统设计，属于 OA，不在这份题单里。
- 与 Hello Interview 题解重合的题，沿用了它的分析骨架和关键取舍并在每篇末尾注明；它是付费内容，仓库公开，所以只链接、不摘录。

---

## `vault/interviews/core/system-design/amazon/sd01-url-shortener.md`
## 来源与延伸阅读

**这个问题在哪里被问到**

- 一亩三分地（1point3acres）帖 1193105，2026-10-14 发布，SDE II，2026-10-02 现场四轮，摘要为「task and course scheduling, URL shortener design, and Amazon Locker LLD」。楼主 2026-10-15 回复「都是 dry run，不用跑。System Design 连图都没画」。帖子正文被隐藏，所以只有题名可信，置信度高（仅题名）。「连图都没画」说明这一轮很可能被压成了口头讨论，所以上面的 45 分钟版要能不用白板讲完。https://www.1point3acres.com/bbs/thread-1193105-1-1.html
- Hello Interview 社区题库的 Amazon 条目共 12 条（2022-09 至 2026-09，最近一条 2026-09-01，senior，美国）。2025-09-20 一条（mid，EMEA）写道：「Asked at Amazon. Exact same question. But I didn't had much time, since some portion of the interview was LP.」置信度中。https://www.hellointerview.com/community/questions?company=Amazon

**哪些部分是补全的**：具体追问（是否要求自定义别名、是否要求点击分析、流量数字）没有任何一条报告给出。前面的需求与数字是按 Amazon 的常见出法重建的，面试时以面试官当场给的为准。

**延伸阅读**

- Hello Interview《Bitly》（Evan King，2026-02 更新，难度标「easy」，面向偏初级的读者）：https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly 。它的骨架是需求（创建、可选别名、可选过期、跳转）→ 非功能（唯一性、延迟小于 100 ms、99.99% 可用、10 亿条与 1 亿日活）→ 实体与 API → 单体到拆分的高层设计 → 深挖「短码如何生成并保证唯一」「如何扩展读」。编号上它比较长 URL 前缀、哈希截断、计数器加 base62 三种，推荐 Redis 计数器批量领号；读扩展上依次给出索引、内存缓存、CDN 与边缘。
- 与它一致之处：骨架、读写 100:1 的判断、302 优先、批量领号加不相交号段、缓存与 CDN 分层。
- 与它不同之处：（1）计数器放 DynamoDB 而不是 Redis，理由是异步复制下回退计数的风险，Amazon 面试官更爱听托管服务的保证；（2）补上它没展开的可逆置换防枚举；（3）补上多区域下别名的静默冲突，这是它单区域叙述里碰不到的问题；（4）把分析放回 CDN 实时日志而不是源站，因为 CDN 命中的请求源站看不到；（5）把下架延迟明确写成 `max-age` 的函数。它的页面把 staff 期待写在评语里（要求看穿教科书方案并讨论真实的生产问题），上文的「Staff 视角」一节就是在回答那一条。
- 本库通用题解 [[solution-url-shortener]] 覆盖了短码生成三选一、NoSQL 分区键、读路径缓存与热键、分析管道、301/302 与别名并发；这里只写 Amazon 的追问方式与 AWS 组件的落点。限流细节见 [[solution-rate-limiter]]。题单总览见 [[sd-index]]。

---

## `vault/interviews/core/system-design/amazon/sd02-amazon-lockers.md`
## 来源与延伸阅读

**这个问题在哪里被问到**

- Hello Interview 社区题库的 Amazon 条目 `amazon-lockers-delivery`，共 14 条（2024-01 至 2026-09，最近一条 2026-09-10，senior）。题面摘要：「a package delivery system that integrates with e-commerce platforms, allowing customers to select locker locations during checkout and securely retrieve their packages using authentication codes.」置信度中。https://www.hellointerview.com/community/questions?company=Amazon
- 2025-12-20 一条（senior，EMEA）：「design for drop and pickup for delivery and return of the item」；2025-01-10 一条：「Design from Point of Sale to Locker Delivery」。两条都强调从下单到取件的完整链条，并且包含退货，所以上文把退货放进了需求。
- 一亩三分地（1point3acres）帖 1193105（2026-10-02 现场，SDE II）问的是同一主题的 LLD 版，不是分布式系统版。https://www.1point3acres.com/bbs/thread-1193105-1-1.html

**哪些部分是补全的**：Hello Interview 没有保存名为 Amazon Lockers 的题解页面，上面只有社区条目公开的摘要。具体追问、流量数字、是否要求离线取件，都是按 Amazon 的常见出法重建的，以面试官当场给的为准。

**延伸阅读**（Hello Interview 没有该系统的专题题解，下面是相邻的题解与模式，以及它们与上文的差异）

- 《Ticketmaster》https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster ：预留带时限、读多写少的可见性缓存、热门场次的排队。上文沿用「带时限的预留」；差异是名额可互换，所以用计数器而不是对个体加锁；它的等候室（virtual waiting queue）这里基本用不上，因为单站预留速率只有个位数每秒。
- 《Notification System》https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system ：先持久化再发送、优先级隔离、幂等。取件码通知适用，但量级小得多。通用做法见 [[solution-notification-system]]。
- 模式《Multi-step Processes》https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes ：编排与工作流引擎的取舍。这里选 Step Functions，因为有以天计的等待、超时和补偿；差异是它的叙述偏通用，上文强调设备事件才是工作流推进的信号。
- 模式《Dealing with Contention》https://www.hellointerview.com/learn/system-design/patterns/dealing-with-contention ：对稀缺资源的原子更新、乐观并发与悲观锁的取舍。预留的桶更新就是它的「原子条件更新」，没有用锁。
- 与它们都不同的部分：（1）设备是**有权威的边缘客户端**，需要离线能力与事件对账，这在以上几个页面里都不是主题；（2）取件码的熵与尝试限制是量化推导的；（3）预留是时间分桶的容量，而不是个体座位。
- 本库的 LLD 题解 [[solution-amazon-locker]]（题库叶子 `amazon.amz-locker-onsite`）讲单机的类设计：格口分配、易混字符的处理、到期回收、逆向投件，以及「新尺寸不许动分配」的判分点。与之相邻的预订类题解见 [[solution-ticket-booking]]，限时抢购的最后一件库存争用见 [[solution-flash-sale]]。题单总览见 [[sd-index]]，同批的另一篇见 [[sd01-url-shortener]]。

---

## `vault/interviews/core/system-design/amazon/sd03-dc-stock-state.md`
> 来源：一亩三分地（1point3acres）题库条目 `distribution-center-stock-state-service`，onsite system design，2026-09-18，1 个来源，正文被锁；题库标签为 distributed-systems、data-modeling、ingestion、sharding、idempotency。相关旧条目：Hello Interview 社区 `warehouse-inventory-architecture`（2025-03）、1p3a 题库 `perishable-goods-tracking-system`（电面，2026-06-24）、`fulfillment-center-inventory-transfer`（onsite 编程，2026-07-22）。对照页面：https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff 、https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale 、https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture 、https://www.hellointerview.com/community/questions?company=Amazon 。
## 来源与延伸阅读

> 来源：一亩三分地（1point3acres）题库条目 `distribution-center-stock-state-service`，onsite system design，2026-09-18，1 个来源，正文被锁；题库标签为 distributed-systems、data-modeling、ingestion、sharding、idempotency。相关旧条目：Hello Interview 社区 `warehouse-inventory-architecture`（2025-03）、1p3a 题库 `perishable-goods-tracking-system`（电面，2026-06-24）、`fulfillment-center-inventory-transfer`（onsite 编程，2026-07-22）。对照页面：https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff 、https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale 、https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture 、https://www.hellointerview.com/community/questions?company=Amazon 。

- 被报告的题面（题库行名，2026-09-18，级别未公开，置信度：题名与标签为中，其余为低）：「distribution center stock state service」。
- **（重建）**：题干正文看不到。上文的题面由标签推断：「很多配送中心持续产生库存事件，要有一个服务接收这些事件，并能回答某个 SKU 在某个 DC 现在有多少、能卖多少、哪里能发货」。事件类型（收货、上架、拣货、调拨、盘点调整）、规模数字、一致性要求都是为了练习而设定的，面试时第一件事就是和面试官确认。

**Hello Interview 怎么做。** 它的《Gopuff》题（本地配送服务）是同一类问题的入门版：需求是按地点汇总附近多个 DC 的库存并让下单不重复占用，骨架是需求、实体（区分商品与库存实例）、接口、高层、深挖。它的强项是：把下单放进单个 Postgres 事务里原子地检查库存、写订单和更新库存；读侧用只读副本、分区和缓存扩展；还讨论了按行驶时间而非直线距离选 DC。《Flash Sale》覆盖单热点库存的预留与排队。《Change Data Capture》讲的是日志式捕获与 outbox。

**一致的地方。** 强一致只放在「占用库存」这一步；读侧用缓存或副本换速度；用 outbox 或日志而不是双写；热点要先量化再拆。

**不同的地方。**

1. 它面对的是「下单」，正文面对的是「摄入」：DC 的物理事件才是库存的来源，事件的幂等、有序和重放是主要问题，它没有展开。
2. 它把库存当成单库里的状态，正文把状态当成账本的投影，所以多出重新计算、对账和盘点这一层。
3. 它把读副本延迟当作不需要精确的小事；正文明确区分「物理在手」与「可承诺」，并用方向不对称解释哪种陈旧可以接受。
4. 在选择上更强调成本：把账本放进事务的代价用数字写了出来。

**本库的通用部分。** 电商核心流程里的库存预占、saga 与 outbox 见 [[solution-e-commerce]]；单热点的原子递减、令牌池和超卖/漏卖见 [[solution-flash-sale]]。正文只写 DC 摄入与库存状态的增量，不重复这两篇。

---

## `vault/interviews/core/system-design/amazon/sd04-fs-replication.md`
> 来源：Hello Interview 社区题目页 https://www.hellointerview.com/community/questions?company=Amazon （条目 `file-system-replication`，2026-10-01，mid-level）。对照页面：https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox 、https://www.hellointerview.com/learn/system-design/patterns/large-blobs 、https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture 。
## 来源与延伸阅读

> 来源：Hello Interview 社区题目页 https://www.hellointerview.com/community/questions?company=Amazon （条目 `file-system-replication`，2026-10-01，mid-level）。对照页面：https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox 、https://www.hellointerview.com/learn/system-design/patterns/large-blobs 、https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture 。

- 被报告的题面（2026-10-01，mid，置信度中）：「1. Interviewer didn't care about how the data is uploaded. 2. Design only the replication part. How does data transfer from region 1 to region 2 efficiently?」
- **（重建）**：除这两句，题目背景看不到。「文件系统」是什么（面向用户的网盘、内部分布式文件系统、还是对象存储）、规模、一致性要求，都是为了练习而做的假设。

**Hello Interview 怎么做。** 这个题目没有同名的专题拆解页，但相邻的三页覆盖了大部分底层内容。《Dropbox》先讲客户端分块、指纹（fingerprint）、可续传上传和同步，其强项是把大文件拆成块、用块指纹判断「是否已存在」、用预签名链接让数据绕开应用服务器。《Handling Large Blobs》总结了大文件传输的通用模式：直传、分块、断点续传、完成通知。《Change Data Capture》讲怎样从数据库日志得到下游可消费的变更流，以及用事务性 outbox 把业务意图变成显式事件。

**一致的地方。** 内容哈希识别块、块级去重、续传靠记录已完成的块、用 outbox 而不是用副作用推导事件。

**不同的地方。**

1. 它们的重点在客户端到服务端的上传路径；面试官明确说不关心上传，所以正文把重点放在服务端到服务端的传输：差量规划、探测、限速、检查点。
2. 它们没有讨论「数据先于指针」与按文件并行、按前缀提交这类跨区域副本的可见性问题。
3. 它们假设一个区域；正文把链路带宽当作约束，用数字（13.9 Gbps 峰值对 10 Gbps 专线；首次全量 92.6 天）推导出「只传差异」和「离线铺底」的必要性。
4. 反熵与 GC 的复制水位是它们没有展开的部分，也是副本可信度的关键。

**本库的通用部分。** 客户端同步、分块策略、冲突检测和游标式变更日志见 [[solution-file-sync]]；块存储的数据放置、副本与纠删码、垃圾回收见 [[solution-object-storage]]。正文只写跨区域复制的增量，不重复它们。

---

## `vault/interviews/core/system-design/amazon/sd05-vaccine-booking.md`
> 来源：Hello Interview 社区题库 Amazon 条目，2026-09-10，senior：https://www.hellointerview.com/community/questions?company=Amazon ；对照的 Hello Interview 题解《Ticketmaster》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster ；《Dealing with Contention》：https://www.hellointerview.com/learn/system-design/patterns/dealing-with-contention
## 来源与延伸阅读

> 来源：Hello Interview 社区题库 Amazon 条目，2026-09-10，senior：https://www.hellointerview.com/community/questions?company=Amazon ；对照的 Hello Interview 题解《Ticketmaster》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster ；《Dealing with Contention》：https://www.hellointerview.com/learn/system-design/patterns/dealing-with-contention

- 被报告的题面（一句）：「a vaccine distribution system that manages dynamic inventory replenishment and configurable eligibility rules, allowing eligible users to book vaccine appointments by location and date」，2026-09-10，senior，置信度 **中**；没有候选人笔记，只有这一句。
- **（重建）**：每日预约量、站点数、规则复杂度、是否有二针、是否对接真实身份核验，报告里都没有。正文的数字和范围按「州级疫苗项目开放新一批人群」重建。

**Hello Interview《Ticketmaster》的做法（转述）**：骨架是需求、实体、API、高层设计，再在深挖里处理订票过程中保留座位、极热门活动的虚拟排队和搜索。保留座位的主方案是带 TTL 的分布式锁，虚拟等候队列是热门活动的扩展；评论区有不少读者主张用数据库的乐观并发控制代替锁。《Dealing with Contention》一页系统比较了悲观锁、乐观并发、分布式锁和队列几种争用处理方式。

**一致的地方**：先保证不双订，再谈体验；热门事件需要排队整形；读写分离。

**不同的地方**：

1. 正文不把分布式锁当作正确性的来源。库存在持久账本里，锁只会增加一个不可信的故障面；正确性来自数据库事务里的条件写入，占位的过期由工作流和对账保证，不由锁的 TTL 保证。
2. 订票的座位是唯一对象，一个座位一个人；疫苗是两层库存（时段加剂量），稀缺的是剂量，所以「读路径先拒绝」和剂量子计数成为主要设计，而不是座位图。
3. 资格规则引擎在订票里不存在，它是疫苗场景新增的主线：版本化、两次求值、可回放；Hello Interview 的这两页没有覆盖。
4. 公平性在这里是硬需求（公共品），所以用随机化窗口代替先到先得；订票的虚拟队列默认先到先得。

**本库**：通用的座位状态机、虚拟队列和 saga 在 [[solution-ticket-booking]]；按房型-夜的计数行与多晚预订的原子性在 [[solution-hotel-reservation]]，两层库存的写法与它的「区间行 vs 计数行」选择同构，可以对照阅读。

---

## `vault/interviews/core/system-design/amazon/sd06-agent-security.md`
> 来源：一亩三分地（1point3acres）帖 1192714，2026-10-11 发布，L5，三轮各一小时的电话面，组是 AWS 下面做 Agentic AI 安全产品的团队（Austin）：https://www.1point3acres.com/bbs/thread-1192714-1-1.html ；对照的 Hello Interview 题解《Ad Click Aggregator》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator ；《Metrics Monitoring》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring ；模式页《Scaling Writes》：https://www.hellointerview.com/learn/system-design/patterns/scaling-writes
## 来源与延伸阅读

> 来源：一亩三分地（1point3acres）帖 1192714，2026-10-11 发布，L5，三轮各一小时的电话面，组是 AWS 下面做 Agentic AI 安全产品的团队（Austin）：https://www.1point3acres.com/bbs/thread-1192714-1-1.html ；对照的 Hello Interview 题解《Ad Click Aggregator》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator ；《Metrics Monitoring》：https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring ；模式页《Scaling Writes》：https://www.hellointerview.com/learn/system-design/patterns/scaling-writes

- 帖子摘要写「graph and topological-sort problems, AI agent security system design for 1 TB/day, and behavioral questions」，可见正文里有一句「我面的是这个是 Agentic AI 的 security product 组在 AWS 下面」。置信度 **中**：题名和 1 TB/天这个数字是明确的，题面的其余部分看不到。
- 这个组本身就是做「给 AI 代理（agent）装上安全观测与策略」的产品，所以这道系统设计很可能就是他们的核心系统：采集代理的行为遥测（telemetry），检测违规，告警，支持事后调查。
- **（重建）**：具体让你设计什么没有任何公开记录。下面的题面是重建的：「客户的 AI 代理会产生动作事件（提示词、工具调用、模型响应、访问的资源、身份），平台每天接收约 1 TB，要在分钟级检测策略违规（提示注入、越权调用工具、数据外泄），去重后告警，并允许安全分析师回溯调查。」事件大小、租户数、是否要求同步阻断都按下文的假设来，面试时以对方说的为准。


**Hello Interview《Ad Click Aggregator》**把问题定性为「扩展写入」的典型：用 Kafka 或 Kinesis 缓冲，用 Flink 预聚合，按广告 ID 分区，热点广告通过给键加随机后缀分散，再加周期性的批处理对账，形成流加批的组合（它称为 Lambda 架构）。**《Metrics Monitoring》**则讲从采集代理、消息队列到时序库的写入路径，把告警做成「定期对存储发查询」而不是流计算，并把基数爆炸作为主要的扩展天花板。**《Scaling Writes》**一页给出缓冲、批处理、分片和选写优化存储这套工具箱。

**一致的地方**：流是缓冲，不是存储；分区键决定热点；原始数据落湖，批层负责对账；告警评估可以建立在已有的存储上。

**不同的地方**：

1. 广告点击的聚合是**可交换的求和**，热点键加随机后缀即可，最后合并；安全检测要**按代理保序的序列状态**，随机后缀会破坏序列语义，所以我们的热点缓解是「在键里追加会话」并接受降级，而不是随机打散。
2. Metrics Monitoring 倾向于「告警 = 定期查询」，因为 1 分钟延迟可以容忍；这里同样的思路适用于基线类检测（批），但序列规则必须在流里评估，否则要等一个查询周期才能发现，窗口内的突发已经完成了外泄。
3. 广告点击的钱问题要求精确；安全告警更看重**召回**，宁可重复也不能漏，所以去重策略是弱的（指纹加时间桶），并且迟到数据的修正只升级不撤回。
4. 多租户隔离与数据脱敏是这道系统设计特有的维度，两个 Hello Interview 页面基本没有涉及。

**本库**：[[solution-ad-click-aggregation]] 覆盖事件时间与水位线、迟到数据和精确一次写入的通用知识，迟到处理直接建立在它之上，只写安全场景的差异；[[solution-metrics-monitoring]] 覆盖时序存储、基数与告警评估如何经受住它所报告的故障，对应「告警评估要在它所报告的故障中存活」这一点（金丝雀与管道静默故障）。读完这两篇再读正文，只需要补三件事：按代理保序的分区键、规则的双引擎编译、租户隔离与脱敏。

---

## `vault/interviews/core/system-design/amazon/sd07-external-sort.md`
> 来源：Hello Interview 社区题库 Amazon 条目，2026-09-10，mid：https://www.hellointerview.com/community/questions?company=Amazon ；正文用到的相关模式页（没有针对该问题的专页）：《Handling Large Blobs》https://www.hellointerview.com/learn/system-design/patterns/large-blobs 与《Scaling Writes》https://www.hellointerview.com/learn/system-design/patterns/scaling-writes
## 来源与延伸阅读

> 来源：Hello Interview 社区题库 Amazon 条目，2026-09-10，mid：https://www.hellointerview.com/community/questions?company=Amazon ；正文用到的相关模式页（没有针对该问题的专页）：《Handling Large Blobs》https://www.hellointerview.com/learn/system-design/patterns/large-blobs 与《Scaling Writes》https://www.hellointerview.com/learn/system-design/patterns/scaling-writes

- 报告原文（节选）：「you have files over 200gb which just contain numbers. these files can be present on multiple computers. Your server has a total disc memory = 500gb, and you have 8gb ram. How will you sort all the numbers? (you cant do any .sort() function …)」，2026-09-10，mid，置信度 **中**。候选人自己形容这轮是「LLD ish」：它名义上是系统设计，实际更像算法加存储层的设计，要求写得出可运行的核心逻辑。
- Hello Interview 没有针对该问题的专页，所以没有现成骨架可以对照；正文按需求、容量、实体与接口、架构、深挖的顺序自己搭，并借用《Handling Large Blobs》里的分块与可恢复传输的思路。
- **（重建）**：数字的类型（整数还是浮点、二进制还是文本）、值域、是否有重复、输出放在哪里、多台机器之间的网络带宽，原帖都没有说。下面按「64 位有符号整数、小端二进制、可有重复、输出一个有序文件」重建；面试时第一件事就是问清楚这几项。


**Hello Interview 没有针对该问题的专页**，所以不存在需要对照的骨架。可以借用的模式有两个：

- 《Handling Large Blobs》讲的是不要让应用服务器当数据的搬运工，用预签名链接让客户端直接和对象存储交互，大文件分块上传、带校验和、断点续传。正文借用的是**分块加校验和加断点续传**这套思路：运行文件的块、输出的分块上传、Manifest 的恢复，机制是同构的；不同之处在于外部排序里数据是我们自己的计算流水线中的产物，而不是用户上传的内容，因此不涉及预签名链接。
- 《Scaling Writes》讲的是用批处理、缓冲、分片来承接高写入量。外部排序的第一阶段（大块顺序写运行）和第二阶段（异步写输出缓冲）就是缓冲加批处理；分布式版的范围划分就是按键分片。

**本库**：没有对应的通用题解，最接近的是 [[solution-object-storage]] 里关于分块与完整性校验的部分和 [[solution-file-sync]] 里的分块传输，但它们讲的是对象的存取而不是计算。这篇的内容在本库里是独立的，主要的参考是 DDIA 第 3 章（LSM 树里的归并与压实）和第 10 章（批处理里的排序归并 shuffle）；它与 LSM 树的压实（compaction）、与 MapReduce 的 shuffle 阶段是同一个算法的不同场景，面试里点出这两个联系很加分。

排序偏算法，不需要 AWS 服务也能答好；但在数据服务岗位的面试里，最后常会问「如果这个任务要每天跑，在 AWS 上怎么做」，所以要备好 EMR/Spark 的回答，见上面的成本一节。

---

## `vault/interviews/core/coding/amazon/recent/amz_bus_routes.md`
## 来源
- Hello Interview 社区题目 `bus-routes-815`，约 2026-09-20，中级 APAC：https://www.hellointerview.com/community/questions/bus-routes-815 ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。报告只记录了题目名「Leetcode 815. Bus Routes」，摘要为 find the minimum number of bus rides from source to target。
- LC 官方 https://leetcode.com/problems/bus-routes/ （约束取自该页）。
- 代码：`../../coding/solutions/815_bus_routes.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_chess_king_min_moves.md`
## 来源
- 1point3acres 帖子 1192241（L5 店面，2026-10-07）：https://www.1point3acres.com/bbs/thread-1192241-1-1.html 。唯一可见的题面是「下棋游戏：棋子从起始点出发到打倒对面的king，求最短几步」，正文被积分墙挡住；回帖猜测是 BFS 加状态压缩。
- 棋盘大小、走法集合、障碍、是否有多个己方棋子、对方 king 是否移动，帖子都没有写。整道题的规则是补全出来的 **(reconstructed)**。
- 代码：`code/amz_chess_king.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_concatenated_words_trie.md`
## 来源
- 1point3acres 帖子 1192241（L5 店面，2026-10-07）的站内摘要「a LeetCode 472 variant using Trie and DFS」：https://www.1point3acres.com/bbs/thread-1192241-1-1.html 。「变体」具体怎么变，帖子没写 **(reconstructed)**。
- LC 官方 https://leetcode.com/problems/concatenated-words/ （约束取自该页）。
- 代码：`../../coding/solutions/472_concatenated_words_trie.py`。已有 `../../coding/solutions/472_concatenated_words.py`（词集合 DP / 最短优先 Trie）。

---

## `vault/interviews/core/coding/amazon/recent/amz_evaluate_division_cache.md`
## 来源
- 1point3acres 帖子 1191084（L6 店面，2026-09-28）摘要「BQ + BFS coding + caching follow-up」：https://www.1point3acres.com/bbs/thread-1191084-1-1.html 。
- 1p3a 题库条目 `evaluate-division-lc-399`（电话，2026-09-28）。
- 缓存追问的具体内容被积分墙挡住，上文按「重复查询怎么加速、新增等式后缓存怎么办」来写 **(reconstructed)**。
- LC 官方 https://leetcode.com/problems/evaluate-division/ （约束取自该页）。
- 代码：`../../coding/solutions/399_evaluate_division_cached.py`（BFS 版 + 缓存）；已有 `../../coding/solutions/399_evaluate_division.py`（带权并查集）。

---

## `vault/interviews/core/coding/amazon/recent/amz_jump_game_ii_path.md`
## 来源
- Hello Interview 社区题目 `leetcode-jump-game`，约 2026-09-10，Senior EMEA：https://www.hellointerview.com/community/questions/leetcode-jump-game ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 原话：「Jump game II but to return array of choices」。「choices」的含义没有展开，上文取「所经过的下标序列」**(reconstructed)**。
- LC 官方 https://leetcode.com/problems/jump-game-ii/ （约束取自该页）。
- 代码：`../../coding/solutions/45_jump_game_ii.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_lowest_common_manager.md`
## 来源
- 1p3a 题库条目 `lowest-common-manager-org-chart`（电话/现场，3 个来源，2026-07-31 至 2026-10-01），条目名即「组织架构树 + 两名员工，找最低的共同上级」；题库正文被挡。
- 1point3acres 帖子 1191548（L6 店面，2026-10-01）正文「coding 经典lc」：https://www.1point3acres.com/bbs/thread-1191548-1-1.html ，指 LC 235/236 一类的最近公共祖先。
- 题面按「公司组织架构」版本写，树的形式（是否有父指针、是否二叉）未知 **(reconstructed)**。
- 代码：`code/amz_lowest_common_manager.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_number_of_islands_ii.md`
## 来源
- 1point3acres 帖子 1191823（NG onsite，2026-10-03）：https://www.1point3acres.com/bbs/thread-1191823-1-1.html 。主问题是 LC 200 一类的数岛屿，追问原文为「如果矩阵是流式一行一行进来的怎么办 union find嘛？」。正文被积分墙挡住。
- 1p3a 题库条目 `number-of-islands-max-area-streaming`（3 个来源，最近 2026-10-03）。
- LC 305 题面镜像 https://leetcode.ca/all/305.html （官方页为付费题，镜像给出 follow-up「O(k log mn)」）。数据范围没有取到，按「m·n 大到不能每次重扫」处理 **(reconstructed)**。
- 已有 Anki 卡 `streaming-island-count`（只讲逐行流式）；这一讲把它和 305 连起来。代码：`../../coding/solutions/305_number_of_islands_ii.py`、`code/amz_streaming_islands.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_reconstruct_itinerary.md`
## 来源
- Hello Interview 社区题目 `reconstruct-itinerary`，约 2026-09-20，中级：https://www.hellointerview.com/community/questions/reconstruct-itinerary ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 报告原文：「You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.」
- LC 官方 https://leetcode.com/problems/reconstruct-itinerary/ （约束取自该页）。
- 代码：`../../coding/solutions/332_reconstruct_itinerary.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_safe_walk_grid.md`
## 来源
- Hello Interview 社区题目 `safe-walk-grid`，约 2026-10-01，中级 APAC：https://www.hellointerview.com/community/questions/safe-walk-grid ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 摘要：「Determine whether there's a 4-directional path from the top-left to bottom-right of an m×n binary grid ... so your health stays positive」。报告只有题目名，没有面试官的追问。
- LC 官方 https://leetcode.com/problems/find-a-safe-walk-through-a-grid/ （约束取自该页）。官方样例 1 和样例 2 即上文两个示例。
- 代码：`../../coding/solutions/3286_find_a_safe_walk_through_a_grid.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_sliding_window_rate_limiter.md`
## 来源
- Hello Interview 社区题目 `sliding-window-rate-limiter`，电话面，约 2026-10-01，中级 USA：https://www.hellointerview.com/community/questions/sliding-window-rate-limiter ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。该题另有两条 Amazon 报告（2026-08、2026-06，Senior）。
- 题目描述：「Implement a rate limiter using a sliding window algorithm ... Extend the solution to support rate limiting at multiple granularities, including per IP address, per user, and per experience.」
- 这是 coding 轮的题，不是 OOD。代码：`code/amz_rate_limiter.py`。

---

## `vault/interviews/core/coding/amazon/recent/amz_task_scheduler_ii.md`
## 来源
- Hello Interview 社区题目 `task-scheduler-ii`，约 2026-09-10，Staff：https://www.hellointerview.com/community/questions/task-scheduler-ii ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 摘要：「find the minimum total days (including required breaks) to finish all tasks while ensuring any two tasks of the same type are separated by at least space days」。报告只有题目名和级别，没有追问。
- LC 官方 https://leetcode.com/problems/task-scheduler-ii/ （约束取自该页）。
- 代码：`../../coding/solutions/2365_task_scheduler_ii.py`。与已有的 LC 621 Task Scheduler 不同：这里任务必须按给定顺序执行。

---

## `vault/interviews/core/coding/amazon/recent/amz_the_maze_directional.md`
## 来源
- 1point3acres 帖子 1190455（SDE II 店面，2026-09-16；发帖 2026-09-22）：https://www.1point3acres.com/bbs/thread-1190455-1-1.html 。摘要为 40 分钟的带移动约束 BFS，现场写了三维向量存储但写错、没留时间走查；回帖称接近 490 但带方向，另有回帖提到「不能回头不能左不能右转」。
- LC 490 题面镜像 https://leetcode.ca/all/490.html （官方页为付费题）。
- 方向约束变体的精确规则帖子没有写全，上文是按这些碎片重建的 **(reconstructed)**，不是原文。已有 Anki 卡 `forbidden-turn-grid`。
- 代码：`../../coding/solutions/490_the_maze.py`、`code/amz_directional_grid.py`。

---

## `vault/interviews/core/coding/amazon/top_list.md`
> 来源：`vault/interviews/core/leetcode/companies/amazon.md`（生成文件，2026-10-15 由 GitHub 两个仓库汇总：

---

## `vault/interviews/companies/amazon/RECENT_amazon_2026-10.md`
## 来源

- 一亩三分地：2026-09-16..10-16 Amazon 标签下 39 帖与题库 29 条，逐条记录（帖子编号、日期、级别、轮次、可见内容、置信度）在
  [[1p3a_2026-10-16]]。几乎每帖的核心段落要积分高于 188 才能看到（抓取时账号 99 分），题目来自可见文字、楼下回复、站方摘要和
  题库条目名；看不到的部分在各题题解的末尾注明是补全的。积分够了可以回去补全。
- Hello Interview：同一窗口 27 条 Amazon 报告，记录在 [[hellointerview_2026-10-16]]。
- 第 1 节的三条结论分别来自：一位 SDE II 在 onsite 后写的「基本不会有非常规题目」；同一位的「都是 dry run，不用跑」；
  Hello Interview 停车场题面「syntactically correct, although it will not be executed」；以及多帖里「每轮先问行为题」的描述。
- 第 5 节的问题来自一亩三分地的 4 帖与 Hello Interview 的 3 条报告；故事映射是依据 [[story_matrix]] 做的推断。
- 第 6 节来自一亩三分地 2026-10-02 的一篇 6–9 月面经整理帖（61 篇）和一篇 SDE II 全套面经。
- 抓取方法：用登录后的浏览器调用两站的公开接口，2026-10-16。

---

## `vault/interviews/companies/amazon/lp/00_how_lp_works.md`
> 来源标注：`[官]` = Amazon 官方页面（抓取日 2026-10-15）；`[三方]` = 第三方转述，官方页面没有，需要保留怀疑；`推断` = 我的推论。

---

## `vault/interviews/companies/amazon/lp/genai/question_bank.md`
> 来源：`../../catalog/raw/forums.md`（F）§4.2 的汇总行与 §3 的各 loop 记录，抓取日 2026-10-15。引号里是面经原文；**非引号**的是我归纳的报告主题（不是逐字）。

---

## `vault/interviews/companies/amazon/lp/stories/M1_onboarding-and-mentoring.md`
> 来源：`core/Answers.md` Q6、Q13、Q16、Q23；S6（接手实习生项目）。**没有 `core/stories/` 独立笔记。**

---

## `vault/interviews/companies/amazon/lp/stories/R1_quant-stroller.md`
> 来源：**仅简历**（`core/resume/resume.tex`，Projects，Jun 2026–Present）。没有 `core/stories/` 笔记 → 下面只用简历里的事实，其余全部 `【待 Chi 补】`。

---

## `vault/interviews/companies/amazon/lp/stories/R2_ai-native-migration.md`
> 来源：**仅简历一句**（PayPal, Feb 2025–Present）+ S7 笔记里的 AI 使用原则。没有独立的 `core/stories/` 笔记 → 细节大多 `【待 Chi 补】`。

---

## `vault/interviews/companies/amazon/lp/stories/R3_aiki-consumer-apps.md`
> 来源：**仅简历** Projects：Aiki（iOS，Mar 2024）、AikiCard（Web，Jun 2025）。没有故事笔记。

---

## `vault/interviews/companies/amazon/lp/stories/S10_refund-fee-retraction.md`
> 来源：`core/stories/S10 退款费 billing-terms 复盘.md`（status: verified）。

---

## `vault/interviews/companies/amazon/lp/stories/S11_intern-event-streaming.md`
> 来源：`core/stories/S11 实习期事件流.md`（status: **partial**）。**证据偏薄：这是技术广度故事，不是 LP 主力。** 作为 Learn and Be Curious / Dive Deep 的侧证，或当 LP 追问技术背景时使用。

---

## `vault/interviews/companies/amazon/lp/stories/S1_amex-settlement-pipeline.md`
> 来源：`core/stories/S1 Amex 结算管线.md`（status: verified）。只用其中有证据的事实；缺的写 `【待 Chi 补：…】`。

---

## `vault/interviews/companies/amazon/lp/stories/S2_quality-check-framework.md`
> 来源：`core/stories/S2 Quality-check 框架.md`（status: **partial**）。ADR 状态是 **Proposed**。

---

## `vault/interviews/companies/amazon/lp/stories/S3_ach-null-incident.md`
> 来源：`core/stories/S3 ACH 费用 NULL 传播事故.md`（status: verified）。

---

## `vault/interviews/companies/amazon/lp/stories/S4_au-amex-refund-fee.md`
> 来源：`core/stories/S4 AU Amex 退款费.md`（status: verified）。

---

## `vault/interviews/companies/amazon/lp/stories/S5_net-settlement-interchange.md`
> 来源：`core/stories/S5 Interchange 数据源切换.md`（status: **partial**）。

---

## `vault/interviews/companies/amazon/lp/stories/S6_anomaly-detector-go-no-go.md`
> 来源：`core/stories/S6 Anomaly detector go-no-go.md`（status: verified）。

---

## `vault/interviews/companies/amazon/lp/stories/S7_schema-pool.md`
> 来源：`core/stories/S7 Schema pool.md`（status: verified）。**个人仓库 `snowglobe-tools`，不是团队官方工具链。**

---

## `vault/interviews/companies/amazon/lp/stories/S8_terraform-rca.md`
> 来源：`core/stories/S8 Terraform 7 分钟 RCA.md`（status: verified）。

---

## `vault/interviews/companies/amazon/lp/stories/S9_amex-payout-delay-incident.md`
> 来源：`core/stories/S9 Amex 出款延迟事故.md`（status: verified）。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-closest-store.md`
## 来源与延伸

- 题目出处：Amazon 2026-09 的电话面试，一亩三分地上的回帖片段（[thread-1189934](https://www.1point3acres.com/bbs/thread-1189934-1-1.html)，回帖日期 2026-10-04）。原帖正文需要积分才能看，只能读到片段，置信度低。片段只确定四件事：有 add、remove、找最近值三个操作，找最近值是「离 target 最近的数」，起初的做法是排序一次再找，后来给了值域约束（range constraint）。
- 本页自己补充（推断，非报告原文）：具体 API、`Tie` 平局枚举、多重集合语义、值域大小，以及第 4 关的并发与 `k_closest`。若你能看到原帖全文，以原文的 API 为准，替换这些约定。
- [Python 标准库 bisect](https://docs.python.org/3/library/bisect.html)：`bisect_left` 与 `bisect_right` 的差别、`insort` 的复杂度说明（比较 O(log n)，插入 O(n)）。`SortedListIndex` 就是它的直接应用，文档里还有「用 bisect 做按键查找」的食谱，可以补读。
- [LeetCode 658 Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)：它是静态数组上的 k 个最近值，平局取较小的——默认平局规则沿用它。不同的是它的数组不会变，没有增删，也没有重复值的归并。
- [Fenwick tree（Wikipedia）](https://en.wikipedia.org/wiki/Fenwick_tree)：树状数组的原始论文来源与下标运算 `i & -i` 的解释。树状数组在这里额外用来做「第 k 小」，Wikipedia 页面里没有展开这一点，可看 [cp-algorithms 的 Fenwick 条目](https://cp-algorithms.com/data_structures/fenwick.html) 里「在树上二分」一节。
- [sortedcontainers](https://github.com/grantjenks/python-sortedcontainers)：Apache 2.0 的纯 Python 有序容器库，用「分块有序列表」做到实际很快的 `SortedList`。它不是标准库，面试里不能 import，但它的文档解释了为什么在 Python 里分块列表常常比平衡树快，可以支撑上文对方案 D 的判断。

概念背景：[[python.data-model|数据模型与特殊方法（Data Model）]]（`__len__`、`__contains__` 为什么该是特殊方法）、[[oop.interfaces|接口与抽象基类]]（`Protocol` 与 `ABC` 的取舍）。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-configurable-cache.md`
## 来源与延伸

- 题目来源：Hello Interview 社区题库的 Amazon 题目页：https://www.hellointerview.com/community/questions?company=Amazon ——题目原话（2026-09-20 中级与 2026-10-01 资深各一份报告）：设计一个可配置的缓存系统，支持可插拔的淘汰策略（如 LRU、LFU）和可互换的存储后端（如内存、文件系统、heap、stack）。页面只给出这一句话，没有解法；商业站点，只链接不引用。
- 一亩三分地 2026-09-18 SDE II 电面报告：https://www.1point3acres.com/bbs/thread-1189999-1-1.html ——第一道题是 LRU 缓存，说明起点是 LRU，可配置是追问。正文需要积分，只依赖这一个事实。
- 哪些是报告的、哪些是补的：报告里只有「淘汰策略可插拔」「存储后端可互换」两句话；过期时间（TTL）、统计、线程安全、配置对象、后端失败时怎么办，以及四关分级，是重建（reconstructed）的追问，读者若有原文，以原文为准。「heap、stack」两个词报告没有解释，按「存储介质」理解。
- Python 官方文档 `collections.OrderedDict`：https://docs.python.org/3/library/collections.html#collections.OrderedDict ——`move_to_end` 与 `popitem(last=False)` 都是 O(1)，文档里有一个 LRU 范例；与它不同的是，这里把「顺序」和「值」拆开了，因为值可能在文件里。
- Python 官方文档 `typing.Protocol`：https://docs.python.org/3/library/typing.html#typing.Protocol ——解释了为什么策略与后端的接口用结构化子类型而不是抽象基类。
- 题库里的相关题解：[[solution-lru-cache]]（LRU/LFU 的链表与频率桶、装饰器式 TTL）、[[solution-ttl-cache]]（惰性与主动过期、单飞回源）。主要分歧：前者的 TTL 与线程安全是装饰器，这里把 TTL 放进 `Cache`（见决策四）；前者的策略自带值，这里只记 key。
- 概念：[[patterns.strategy|策略模式与可替换算法（Strategy）]]、[[patterns.structural|结构型模式（Structural）]]。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-dag-runner.md`
## 来源与延伸

- [Hello Interview 社区题库：Amazon 条目（package-installation-order、dag-execution-order）](https://www.hellointerview.com/community/questions?company=Amazon)：第 1 关来自 `package-installation-order`（「Given a dependency adjacency list to install packages, return the installation order or throw an exception if a cycle is found」，2026-10-01，中级岗位，3 份报告）；第 2 关的形态来自 `dag-execution-order`（代码评审，2026-09-20，要求找出并修好执行顺序代码里的 bug）。报告里没有出现那份有 bug 的代码，`buggy_runner.py` 的三个 bug 是推断出的典型形态；第 3 关的「结果传给下游」和第 4 关的线程池并行与失败传播同样是推断。它只有题面和摘要，没有标准答案；与它不同之处是把「报出环本身」当作第 1 关的要求，而不是可选项。
- [Python 文档：graphlib.TopologicalSorter](https://docs.python.org/3/library/graphlib.html)：标准库自带拓扑排序，`prepare()` 会在有环时抛 `graphlib.CycleError`，`get_ready()` / `done()` 就是并行调度的接口。这里不直接用它，因为面试要你展示算法；但第 4 关的调度循环与它的用法同构，工作中应当优先用它。
- [一亩三分地 thread-1192714](https://www.1point3acres.com/bbs/thread-1192714-1-1.html)：2026-10-11 的 L5 电话面报告，第一轮是 LC 210（课程表 II）的拓扑排序，说明这类题在电话面就会出现，不必等到 onsite。
- 题库里有课程表（LC 207）的参考解，可对照：LC 207 只问「能不能排完」，这里要产出顺序并报出环。
- 相关：[[solution-task-scheduler]]（调度与优先级）、[[solution-thread-pool]]（自己实现线程池）、[[concurrency.patterns|并发模式]]。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-discount-engine.md`
## 来源与延伸

- 题目出处：Amazon VO 一轮 OOD，一亩三分地 [thread-1191754](https://www.1point3acres.com/bbs/thread-1191754-1-1.html)（2026-10-02）：`isEligible` / `apply` 的基类要求、遍历每行的主流程、BUY_X_GET_Y 折成减免的描述来自这里。与它的差别：它的遍历是「每行 × 每个折扣」，这里把整车折扣拆成第二层，并让 `apply` 接收剩余价格，避免叠加时多减。
- 旁证：一亩三分地 [thread-1190571](https://www.1point3acres.com/bbs/thread-1190571-1-1.html)（2026-09-23）只有「店面 OOD：模拟购物车」一句话，说明这类题在 Amazon 店面轮也会出现；另有一条欧洲区报告（2026-09）提到购物车价格计算器 API，追问全场折扣、满额翻倍、买三送一、热销商品折扣。
- 推断（页面自己补充，非报告原文）：百分比折扣、满减两种折扣，叠加顺序与「只取最大」，门槛按折后小计判断，第 4 关的账单与并发，优惠券写法。置信度：来源只有片段，整体为中低。
- Python 官方文档 `decimal`：https://docs.python.org/3/library/decimal.html ——精确的十进制算术与舍入模式；这里用它做“字符串 → 分”的单次转换，其余全部用整数。
- 题库里相邻的 [[solution-online-shopping]]：它讲完整的下单流程（库存、支付、订单状态）；这里把定价抽出来单独做深。
- 概念：[[patterns.strategy|策略模式与可替换算法（Strategy）]]、[[oop.values|值对象与不可变性（Value Objects）]]。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-emergency-pubsub.md`
## 来源与延伸

- 题目来源：Hello Interview 社区题库的 Amazon 题目页：https://www.hellointerview.com/community/questions?company=Amazon ——题目原话（publish-subscribe-system，2026-10-01 中级报告）：应急响应系统里一些组件订阅应急事件、另一些发布，实现处理发布与订阅逻辑的类。页面只给出这一句话，没有解答；商业站点，只链接不引用。另一条更早的线索来自面试论坛一份 SDE II 的报告（事件转发框架）：要支持批量、考虑慢事件、失败的订阅者不能阻塞其他订阅者。
- 哪些是报告的、哪些是补的：第 1 关与「失败隔离」「慢事件」来自报告；事件类型与严重度、按类型过滤、重试与死信、异步信箱与优先级是重建（reconstructed）的追问，没有可对照的完整解答。
- Python 官方文档 `heapq`：https://docs.python.org/3/library/heapq.html ——优先队列的 `(优先级, 序号, 任务)` 写法和同级先进先出、避免比较任务对象的理由；文档没讲有界队列满了挤掉最不重要元素，这里用一次扫描加 `heapify` 实现并说明了代价。
- Python 官方文档 `threading.Condition`：https://docs.python.org/3/library/threading.html#condition-objects ——`wait_for` 与 `notify_all` 的语义，信箱的"等事件"和 `flush` 的"等送完"都建立在它上面。
- 题库里的相关题解：[[solution-pub-sub]]（通用的有界主题日志、游标、通配订阅、死信主题）。主要分歧：它选"拉"模型，订阅者各有游标，可以重放；这里选"推"加每人一个信箱，因为应急通知是"当下立刻要送到"，不需要重放，代价是不能回头读已经送过的事件。
- 概念：[[patterns.observer|观察者与事件（Observer）]]。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-file-watcher.md`
## 来源与延伸

- [一亩三分地 thread-1189999](https://www.1point3acres.com/bbs/thread-1189999-1-1.html)：2026-09-18 的 Amazon SDE II 电面报告，跟帖里只提到「设计 file watcher system」，正文被隐藏。除题名外，全部题面都是为练习补出的（reconstructed）：第 1 关由题名直接逼出，第 2、3、4 关（订阅与过滤、去抖与回调隔离、后台线程与停止）是推断。
- [Python os.scandir](https://docs.python.org/3/library/os.html#os.scandir)：`DirEntry` 的 `is_dir(follow_symlinks=False)` 与缓存的 `stat()`；`DiskFileSystem` 据此遍历，并解释了为什么不跟随符号链接。
- [Python threading.Event](https://docs.python.org/3/library/threading.html#event-objects)：`Event.wait(timeout)` 既是可中断的睡眠，也是停止信号；后台循环和测试里的同步都用它。
- [Linux inotify(7)](https://man7.org/linux/man-pages/man7/inotify.7.html)：系统通知那条路的官方说明，包括队列溢出、改名事件（`IN_MOVED_FROM` / `IN_MOVED_TO`）等；与这里的轮询不同，它不需要扫描，但平台相关，所以这里只在扩展里提到。

概念背景：[[patterns.observer|观察者与事件（Observer）]]（订阅者是函数、事件是只读的小数据）、[[concurrency.primitives|同步原语（threading）]]（`Lock` 与 `Event` 各管什么）。题库里相邻的两篇：[[solution-in-memory-file-system]]（把文件系统本身做成内存里的树；这里的假文件系统在测试里扮演类似角色，但只需要「列出文件和指纹」一个方法）；Amazon kit 里的 `vault/interviews/companies/amazon/lld/file_search.md` 讲了树遍历与可组合的过滤器，`include` 参数可以直接接它的过滤对象。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-linux-find.md`
## 来源与延伸
- 题目来源：Hello Interview 社区题库 Amazon 条目「Design a Linux Find Command API」（共 11 份报告，最近一份 2026-10-01，中级岗位，美国）：https://www.hellointerview.com/community/questions?company=Amazon ——原文只有“按大小、格式、名字等条件跨目录搜索，如大于 5MB 的文件、所有 XML 文件；接口干净、可扩展”。一亩三分地题库里相邻的一行是「按大小和后缀搜索文件」（现场编码，4 份来源，2026-07-25 至 09-18，标签含 filesystem、oop-design、testing、cycle-detection）：https://www.1point3acres.com/
- 哪些是报告的、哪些是补的：第 1 关（单个条件）来自报告；第 2 关 AND / OR / NOT 的追问顺序、第 4 关的符号链接环（依据是题库标签 cycle-detection）是推断（reconstructed）；面试官原话没有留下。
- Hello Interview 的文件系统题解讲的是内存文件系统本身的创建、移动、重命名；这里是它的补集：树已经存在，重点放在“条件如何组合与扩展”。
- POSIX `find` 规范：https://pubs.opengroup.org/onlinepubs/9699919799/utilities/find.html ——AND 隐含、`-o` 为 OR、`!` 为 NOT，以及短路求值的要求；这里的 `&`、`|`、`~` 与之对应。
- Python 官方文档 `fnmatch`：https://docs.python.org/3/library/fnmatch.html ——`fnmatchcase` 区分大小写，我们用它实现 `NameGlob`。
- 规约模式（Specification）原始论文：https://martinfowler.com/apsupp/spec.pdf ——Evans 与 Fowler 对可组合业务规则的描述；这里在 Python 里用运算符重载实现。
- 题库里的 [[solution-in-memory-file-system]]：同一棵树的另一面。概念：[[patterns.structural|结构型模式（Structural）]]、[[oop.interfaces|接口与抽象基类]]。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-parking-fees.md`
## 来源与延伸

- 题目来源：[Hello Interview 社区题库](https://www.hellointerview.com/community/questions?company=Amazon)（题目 `parking-lot-system`，Amazon 资深岗，亚太地区，2026-09-20 的报告）：原文只说重点在停车费计算、不同场景有不同逻辑，代码「syntactically correct, although it will not be executed」。需要登录，只链接不摘录。仓库的 Amazon kit 还记着三份相关的论坛报告（停车场加车型并追加五六条新需求、按车型找最佳车位、停车票据与收据），编号见 `vault/interviews/companies/amazon/lld/route.md`，共同的信号是停车场在 Amazon 考的是出场计费。
- 哪些是报告的、哪些是补的：报告没有给出任何具体费率；四关分级、全部费率与时段、免费宽限期、每日封顶、会员折扣、丢票罚款、并发那一关都是推断，在这里是重建（reconstructed）的规则。
- [Python 标准库 datetime](https://docs.python.org/3/library/datetime.html)：`weekday()` 周一为 0、周日为 6，所以工作日是 `< 5`；`datetime.combine` 把日期与时间拼成当天的某个边界。这里处理的是不带时区的本地时间。
- [Hello Interview：停车场题解](https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/parking-lot)：题库停车场的主要参考。它的计费是「所有车型同一个小时费率、按小时向上取整」，并明确说不要过度设计。这里不同意的只是前提：题目说重点在计费，面试官一旦说「不同场景不同逻辑」，价目表加切段就是正确的形状；而在没有这句话的版本里，一个函数就够。商业站点，只链接不摘录。
- 题库已有的停车场题解 [[solution-parking-lot]]：车位分配、楼层、占用状态和阶梯计价（`TieredRate`）。它的阶梯计价是按总时长的边际分档，与这里按时间轴切段是两个正交的问题：一个按「停了多久」分档，一个按「什么时候停的」分段。
- Amazon kit 的 `vault/interviews/companies/amazon/lld/pricing_billing.md`：同一个骨架的其他变体（地铁封顶、购物车折扣、AWS 账单），共同点是用整数分和一个按顺序应用的规则列表。

概念背景：[[patterns.strategy|策略模式与可替换算法（Strategy）]]（什么时候需要策略接缝，什么时候是数据；决策二与决策四正是两个方向的例子）、[[problems.machines.parking-lot|停车场（Parking Lot）]]（这里站在它之上）。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-robot-restaurant.md`
## 来源与延伸

- [一亩三分地 thread-1189999](https://www.1point3acres.com/bbs/thread-1189999-1-1.html)：2026-09-18 的 Amazon SDE II 电面报告，跟帖里只提到「设计机器人餐厅以及追问」，正文被隐藏。除题名外，全部题面（订单来源、状态、分配、电量）都是为练习补出的（reconstructed）：第 1 关由题名直接逼出，第 2 关的多机器人与分配策略、第 4 关的并发与取消是推断。
- [一亩三分地 thread-1191952](https://www.1point3acres.com/bbs/thread-1191952-1-1.html)：2026-10-04 的帖子，Amazon Robotics 实习（面试在 2026-03），读者问「低于 50% 但没空 charger 怎么处理」。那是另一个团队的另一道题，这里只借它的问法做第 3 关的充电追问，阈值与规则是自己定的。
- [Python 标准库 enum](https://docs.python.org/3/library/enum.html)：`Enum` 的成员比较用 `is`；两个状态枚举和事件枚举都据此写。
- [Python 标准库 threading](https://docs.python.org/3/library/threading.html#lock-objects)：`Lock` 的语义；用它保护「读队首—选机器人—改状态」这个整体。

概念背景：[[patterns.state|状态模式（State）]]（决策一：何时用枚举加转移表、何时升级成状态类）、[[patterns.strategy|策略模式与可替换算法（Strategy）]]（决策二：一等函数当策略）。题库里相邻的是 [[solution-restaurant]]（桌位、点单、后厨流水线的餐厅系统），那道题讲餐厅的业务流程和订单生命周期；这里把重点放在机器人这一个会被调度、会没电的资源上，两道题可以对照读：同样是「订单」，一个重点在流程，一个重点在资源调度。

---

## `vault/domains/low-level-design/readings/problems/solution-amz-train-fare.md`
## 来源与延伸

- 题目出处：Amazon SDE 现场面，2026-10-12，一亩三分地 [thread-1192827](https://www.1point3acres.com/bbs/thread-1192827-1-1.html)。可见部分给出线路 G→U→H→K→I、统一票价、`calculateFare(start, stop)`、动态加站、周末封顶；后半被隐藏。
- 另一份独立报告：LeetCode Discuss [8500377](https://leetcode.com/discuss/post/8500377/)，2026-09，题面相同，称它「最后变成了 OOP／LLD 题」。只作旁证，不摘录。
- 推断（页面自己补充，非报告原文）：封顶是单程还是每日累计、封顶数额、第 4 关的每日累计封顶、高峰加价、并发。置信度：前三关中，题面本身为中，其余为低。
- [Python 标准库 datetime](https://docs.python.org/3/library/datetime.html#datetime.date.weekday)：`weekday()` 周一为 0、周日为 6，所以周末是 `>= 5`；也说明了无时区的「朴素时间」的含义——这里的 `when` 是线路所在地的本地时间。
- [Prefix sum（Wikipedia）](https://en.wikipedia.org/wiki/Prefix_sum)：前缀和的定义，以及用它在 O(1) 内回答区间求和；这里把它用在「两站之间价格之和」上，并讨论插入的代价。

概念背景：[[oop.values|值对象与不可变性（Value Objects）]]（`Money`、`Trip` 为什么是 frozen dataclass）、[[patterns.strategy|策略模式与可替换算法（Strategy）]]（`FareRule` 什么时候该是协议、什么时候一个函数就够）。本仓库的 Amazon kit 里也有一份地铁票价的变体写法，见 `vault/interviews/companies/amazon/lld/pricing_billing.md` 的第 4 节第 9 步，它把「按站数计费＋每日封顶」做成一个类；这里把线路、规则和记账拆成三块，好让每块的变化原因只有一个。
