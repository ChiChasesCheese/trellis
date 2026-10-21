# fit · Chi 的简历 vs Java Software Engineer JD（逐条）

> 评级：**强** = 简历上有直接证据且能讲 3 分钟 · **部分** = 有相邻经验，但缺关键一层 · **缺口** = 没有证据，不要硬说，补课 + 诚实表述。
> 诚实线：数字只说量级；不点同事和商户名；自己没做的不说自己做的。

## 0. 总览

| 类别 | 条数 | 强 | 部分 | 缺口 |
|---|---|---|---|---|
| Qualifications（9 条硬性 + 1 条 Plus） | 10 | 4 | 4 | 2 |
| Day to Day（10 条，含"面试别人"） | 10 | 3 | 4 | 3 |

**一句话画像**：Chi 的强项是**"正确性要求极高的数据管线 + 线上值守 + 事后定量复盘 + 测试纪律"**；弱项是**"机器和网络那一层"（Linux、网络、存储引擎、性能剖析、C++）**，而这恰好是 JD 后半的措辞。面试策略：把强项讲成 JD 前半的证据，把弱项讲成"我知道它在哪、读过什么、能推到哪一层"，不要装有。

---

## 1. Qualifications

| # | JD 原文 | 评级 | 证据 | 该怎么说 | 缺口：补什么 |
|---|---|---|---|---|---|
| Q1 | Preferred degree in any computing related area | **强** | NYU MS Computer Science（2023–2025） | "I have an MS in computer science from NYU." 不展开本科（建筑管理）；被问时说"I switched into CS for my master's and have been writing production code since." | — |
| Q2 | Well-versed in the fundamentals of software engineering | **部分** | PayPal 两年同一平台；Ruby/Kotlin→Java 迁移含"行为一致性测试"；Quant-Stroller 66K+ 行、470+ 测试文件、narrow seams | "My fundamentals are from owning one money pipeline end to end: idempotency, tests that span stages, migrations with parity checks." 薄的是**数据结构 / 算法 / OS 的口头深度**，不是工程习惯 | 数据结构与算法、复杂度、堆、有序结构、缓存、OS/IPC、网络六块基础 |
| Q3 | Genuine interest in solving technical problems, along with a strong ability to implement solutions | **强** | Quant-Stroller（没人要求，为了搞懂回测能否撑过成本与样本外检验而自建）；schema pool（没人分配）；on-call 的 RCA | 讲 Quant-Stroller 的故事，和 Terraform RCA 后扫全仓库的故事 | — |
| Q4 | Low ego, able to work both in a collaborative team setting and autonomously | **强** | 无简历句子，靠故事：公开撤回自己的数字；接受批评写 ADR；把 SLA 定论讲清让别人 defer，但不挤部署环节；修了就主动说"下一个雷" | "I'd rather retract my own number in public than have a remediation sized off a bad predicate." | — |
| Q5 | Committed to designing and implementing fully automated, scalable, and maintainable solutions with extensive testing | **强** | 简历：Ruby/Kotlin→Snowflake/Java 迁移"comprehensive testing … behavioral parity"；Quant-Stroller 470+ 测试文件、自托管 CI、append-only experiment ledger、dual-gate；事后补"跨 promote→fee"的 e2e；配置驱动门禁 | 讲 ACH NULL 事故：重点是**测试为什么没抓到**的四个原因，和"补上跨阶段 e2e" | — |
| Q6 | Comfortable operating at various levels of abstraction, from individual machines to large scale distributed systems | **部分** | 高层：Kafka、K8s（部署形态）、Snowflake、Spark。低层：讲得出零拷贝克隆为什么 2 秒（微分区元数据）、并行度 = replicas × tasks.max 受 partition 数限制；**简历没有单机层面（CPU、内存、磁盘、内核）的证据** | "Most of my work has been at the distributed-service and data-warehouse level. I've gone down a layer when it mattered — why a clone takes two seconds, why consumer parallelism is capped by partitions — and I'm deliberately learning the single-machine layer: caches, syscalls, the JVM." 不要说"all levels" | CPU 缓存局部性 → 进程/线程/IPC |
| Q7 | Strong knowledge of the details of computing all throughout the technical stack | **缺口**（诚实） | 同上；简历没有 Linux、JVM 调优、网络栈的任何句子 | 不要说"strong"。说："I know the details where I've been burned — SQL NULL semantics, at-least-once delivery, Snowflake's storage model. Below the JVM I'm earlier in the curve, and here is what I've read." 然后让对方选一层，你推到最深处并说"我就知道到这里" | 语言深度题库的速度、分配、JIT/GC、Linux 工具四节；JIT/ZGC |
| Q8 | Superior ability to write, refactor, and debug programs in Java | **部分** | 简历 skills 有 Java；PayPal 把 Ruby/Kotlin 迁到 **Java**（含 Claude Code 辅助重构 + 测试）；实习用 Kotlin / Spring Boot（跑在 JVM 上，但不等于 Java 语言功底）；HackerRank（Java）已通过 | "Day to day at PayPal I'm in Java and Snowflake; I've also written Kotlin/Spring. The Java OA passed. I've been drilling Java 21 for this loop." 说"superior"会被追问，靠编码题与语言深度题撑 | Java 21 特性（record、sealed、模式 switch、虚拟线程）；视频面编码题 |
| Q9 | Good knowledge of networking and storage systems | **部分** | 存储：Snowflake（微分区、零拷贝克隆、Streams）、PostgreSQL、Kafka log 的使用者视角。网络：Kafka proxy（SASL/TLS 代理）、gRPC 列在 skills；**没有 TCP / 延迟 / 吞吐的亲手经验** | 存储：用 Snowflake 的存储模型讲 immutable files + metadata pointers。网络：诚实说"as a user of Kafka and gRPC"，并讲你读过的 Nagle/`TCP_NODELAY`、批量 vs 延迟 | 存储引擎（B+ 树 / LSM）；TCP 基础 |
| Q10 | Plus: C++, Linux, trading industry | **缺口 / 部分** | C/C++、Rust 只出现在 skills 行，**没有任何 bullet**；Linux 没出现；交易行业：只有 Quant-Stroller 的 paper trading（没有真实交易所连接）和支付行业经验 | C++：不主动提；被问就说"listed from coursework, not production"——**前提是真的**；不确定就说"I haven't used C++ in production"。交易行业："Not in industry; I built a research and paper-trading platform to learn it, and found how little of a good backtest survives costs and out-of-sample tests." | C++ 与 Java 的差异（语言深度题库的版本、语言对比两节）；交易常识（spread、延迟、回测） |

> Q1–Q9 是 JD 的九条硬性要求，Q10 是 "Plus"（按"缺口"计）。§0 的计数由此得出。

---

## 2. Day to Day

| # | JD 原文 | 评级 | 证据 | 该怎么说 | 缺口：补什么 |
|---|---|---|---|---|---|
| D1 | Maintain and extend core research infrastructure | **部分**（个人项目很强，雇主侧无） | Quant-Stroller：narrow DataSource/Factor/Strategy/Broker seams，加一个市场 = 薄适配器；point-in-time 数据平面（raw→bars→panel，DuckDB/Parquet）；2,300+ 因子目录；experiment ledger。**这是个人项目，不是雇主工作**；雇主侧：PayPal 费用管线是内部"平台" | "The closest I have to a research platform is my own: it's why I know what a researcher needs from infra — reproducibility, point-in-time data, a ledger of every run." 明说是个人项目 | 量化研究基础设施的常见形态 |
| D2 | Design, implement, and maintain distributed storage systems with various performance and reliability requirements | **缺口** | 没有自建存储系统的经验。相邻：对 Snowflake / Kafka / PostgreSQL 的**使用与取舍**（幂等、四层 MERGE、ADR 的容量分析） | "I haven't built a storage engine. I've designed on top of three of them and had to know their failure modes: …" 然后讲一个具体失败模式（at-least-once 重投 → 幂等；stream offset 与业务写入不是同一事务）。**追问到副本、一致性协议、compaction 就说不到** | Kafka 日志模型、幂等；LSM / B+ 树取舍；公司背景里的分布式存储一节 |
| D3 | Address performance limitations within our own software, open-source libraries and applications, Linux, etc. | **部分（偏弱）** | 简历没有性能 bullet。最接近的故事：识别"逐行 numpy 推理在 7.6 亿行 / 天规模下会超时"，把上线拆成两阶段，先上纯 SQL pushdown 的确定性规则、模型推理放到 go/no-go 门后——**这是设计期的推理，不是剖析（profiling）出来的**。Quant-Stroller：简历只写了 DuckDB/Parquet 与 5,500 只股票面板，没写向量化也没有基准数字，**不要说成性能成果** | 讲这个故事时说清楚："this was capacity reasoning before anything shipped, not profiling a running system." 然后补一句你**怎么**做剖析 | **最大的单项缺口。** 缓存局部性；语言深度题库的速度、分配、JIT/GC、Linux 工具；固定内存池；找一个真实的性能排查案例填进故事 |
| D4 | Investigate new technologies to improve stability, scalability, and performance of a distributed computing farm | **部分** | 实习：Kafka Connect 在 K8s，一 topic 一 Deployment，并行度 = replicas × tasks.max，上限 = partition 数（边界：我是消费 / 落库 / 校验侧，没有运维过集群）；Airflow DAG 调度 Spark 作业；Quant-Stroller 在 8-GPU 服务器上跑 PyTorch + 自托管 CI | "I've worked on the consumer side of a horizontally scaled system and scheduled Spark jobs with Airflow; the one thing I'd say I learned is that parallelism is capped by the narrowest partitioned resource." 别说"运维过集群" | K8s 基础；计算集群调度 |
| D5 | Develop and improve monitoring and proactive detection capabilities | **强** | 简历：on-call，建 transaction-tracing 与可观测性栈（Sentry、Datadog）。自己建的每日健康检查"每笔 settled 交易都有费用"抓到静默 NULL 事故；异常检测器 + go/no-go | 讲 ACH NULL 事故。强调"检查是对的，不能压掉"。可补："a check that fires on missing data is better than a dashboard nobody opens." | — |
| D6 | Perform basic data analysis to support decision making and better plan for future growth | **强** | blast-radius 查询、修正谓词、规模 196K→22K 行；QA 6 商户 vs 生产 18k、峰值每天数亿行的容量推理；ADR 的容量分析 | 讲两个故事；强调"每条断言配一个可复跑的查询" | — |
| D7 | Improve networking communication between different components of the system to achieve optimal latency and throughput | **缺口** | 唯一相关：Kafka 批量消费（批量 vs 延迟的取舍）；没有 socket / TCP / 序列化 / 零拷贝的亲手经验 | "I haven't tuned network paths. What I understand: latency vs throughput trade through batching, Nagle's algorithm, serialization cost. I'd start by measuring where the time goes." 然后问对方当前的瓶颈 | TCP/UDP、Nagle、NIO、组播与内核旁路；虚拟线程 |
| D8 | Communicate with stakeholders across teams | **强** | 一条查询结束跨三个团队 50 条回复的争论；事故指挥里的 SLA 定论；跨定价 / 结算 / 出款 / 收单行的数据契约 | 讲事故指挥或那场争论（1 分钟版）：先把"边界在哪"讲清，冲突自然消解 | — |
| D9 | Conduct code reviews of other developers, researchers and operations team members | **部分（证据薄）** | 简历：用 Claude Code 做 code review（review AI 产出，不是评审同事）；带教只讲 domain-ownership / architectural collaboration，不编 code-review 记录；两年约 90 个 PR（自己的，不是评审数） | "I read every diff — including the AI's — in money code, and I review as if it were someone else's code." 但**不要编造**"我评审过 N 个 PR"。回忆一次真实的评审经历（如有） | 无需补课，需要**回忆真实经历** |
| D10 | Participate in the recruitment process by conducting interviews and providing candidate evaluations | **缺口** | 简历没有。你是被面试者，这条只说明"你的面试官会写评价，你的表现 = 给他的材料" | 不需要回答。用法：把每个回答讲成"面试官能原样写进评价的句子" | — |

---

## 3. 缺口优先级（按"被追问的概率 × 补得上的程度"）

| 优先 | 缺口 | 为什么 | 做什么 |
|---|---|---|---|
| 1 | **性能剖析 / 排查**（D3） | JD Day-to-day 第 3 条，面试评分点"性能直觉"（每个追问都是"能不能更快/更省"） | ① 编码题的 Part 2–4 练到口述；② 语言深度题库的速度、分配、JIT/GC 各答一遍；③ 填一个真实的性能排查案例 |
| 2 | **单机层：缓存 / OS / Linux**（Q6、Q7） | 视频面追问"为什么这样更快"的终点 | 顺序：缓存局部性 → OS/进程/IPC → 网络 |
| 3 | **网络**（Q9、D7） | JD 点名一条，视频面可能问并发 / non-blocking | 网络基础；多线程合并数据流题 |
| 4 | **Java 语言细节**（Q8） | "Superior ability" + 面经里的挂法是"语言细节答不深" | JIT/GC、内存模型；Java 21 特性 |
| 5 | **C++ / 交易**（Q10） | Plus 项，不是硬性；不主动提 | 只需能说出 spread、延迟、回测各是什么 |
| 6 | **分布式存储设计**（D2） | 简历没有，面试官若问设计会用 JD 原词 | 不补深，诚实表达"使用者视角"，推到 Kafka/Snowflake 的存储模型 |

## 4. 一句话版（放在回答的结尾，可复用）

> "My experience is strongest in correctness-critical pipelines, on-call, and quantitative post-mortems; I'm earlier in the curve on single-machine performance and networking, which is why I've spent the last weeks on exactly that — caches, the JVM, syscalls. I'd expect the first year here to be about closing that gap on real systems."

公司自己说新人要一两年才能完全上手，所以他们本来就预期你要学。
