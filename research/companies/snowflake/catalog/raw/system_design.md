# Snowflake 系统设计轮（电面 SD + onsite SD）原始资料汇编

> 采集日期：2026-09-13。方法：WebSearch + WebFetch，约 40 次抓取/检索。来源覆盖 1point3acres（正文
> 403，经其 Telegram 镜像 `t.me/s/usinterview?q=snowflake` 与 1p3a 自带的搜索摘要/问题库页面读到）、
> Blind（teamblind.com，浏览器 UA 可直连）、PracHub / StaffEngPrep / FastPrep / TechInterview.org /
> Aced(Exponent) 等聚合/培训站（**不采信** lodely、vervecopilot，按仓库规矩）、careers.snowflake.com。
> 与本仓库已有材料 `../../raw/process_research.md`（下称"P"）、`../../raw/company_research.md`（下称
> "C"）互补：P 里已有的题目（KV store、Quota System、SQL notebook、SQL engine as cron job、Queue
> service、Audit Log、Dynamic Blacklist Filter、Password Storage、DAG cache、Web Crawler）本文件**复
> 用并补充新证据**，标注"复用 P + 原采集日期 2026-09-13"（P 与本文件同日完成，故日期未变）。
> 置信度：**[高]** = 一手候选人叙述（Blind/1p3a 正文或搜索摘要包含具体转述）；**[中]** = 聚合站转述但
> 多源一致或与一手细节吻合；**[低]** = 单一聚合/培训站、疑似 AI 生成题库，仅供参考轮廓。

---

## 0. 结论速览

| 问题 | 结论 | 置信度 |
|---|---|---|
| SD 轮出现在哪些阶段 | 电面阶段（"两轮 back-to-back" 里的第二轮，常与 1 轮 coding 搭配）与 onsite 阶段都会出现；早期职业（IC1/IC2）也会遇到，不是只有 senior 才有 | 高（P §1.3 一手证据 + 本文件新证据） |
| 时长 | 45–60 min，多数报告落在 60 min 一轮的电面/onsite 结构里；45 min 更常见于强调"介绍+设计+提问"三段式的报告 | 高 |
| 工具 | 未见候选人明确点名 Snowflake 用什么白板（不同于 Stripe 明确用 Whimsical）；聚合站泛泛提到 Excalidraw/Miro/CoderPad 白板是行业通用工具，**未证实 Snowflake 专用哪一个**；coding 轮明确用 **CoderPad**（P 引用 Blind ICT2 帖 "coderpad"） | 中（工具未证实）／高（CoderPad 用于 coding） |
| 面试官风格 | 两极：多数一手报告"人很好、会给 hint"，但至少一条 IC1/IC2 SD 报告明确"interviewer remained largely silent" | 高（矛盾并存，如实记录） |
| 题目风格 | **infra/data 味道浓**：KV store、quota、调度器、队列、审计日志、DAG 缓存、SQL 执行引擎——不是"设计 Twitter"这类泛消费品题；候选人反馈"不像标准的'设计一个通用 web 服务'面试，更接近 data-platform 问题" | 高（多源一致） |
| "Hire" 门槛 | Blind 一手（ex-Google, IC2, 2025-10-04）："The first two are just screens, doesn't signal anything"；"you need to get Hire in all the remaining ones."——即电面不计入通过线，onsite 每一轮都要拿到 Hire | 高（复用 P §1.3） |

---

## 1. 逐题证据（按任务要求的题目清单排列）

### 1.1 KV Store（键值存储）系统设计

Snowflake 面试库里 KV store 是**出现频率最高的 infra 题族**，但版本很多，不是单一题目：

- **基础版**：`PUT/GET/DELETE`，需要持久化 + `getRange(minKey, maxKey)` + point-in-time snapshot。—— 1point3acres 问题库（无法核实具体面经贴 ID，仅题库页摘要）https://www.1point3acres.com/interview/problems/company/snowflake（访问 2026-09-13）**[中]**
- **分布式版**（"signature" 变体，多个聚合站复述细节高度一致）：Design a distributed KV store，`PUT/GET/DELETE` 接口，要求 **global versioning**、**time travel 式 point-in-time snapshot**、**strong consistency on a single key within a partition**、**Raft-based replication**、service discovery；follow-up 延伸到"跨分区更新多个 key 的分布式事务协议，需 serializability，涉及两阶段提交"。—— staffengprep.com/companies/snowflake（访问 2026-09-13）**[中，聚合站转述，但与 Snowflake 自身"FDB 存元数据+分区版本"的架构高度吻合，可信度上调]**；1point3acres 独立帖 "Design a Distributed KV Store" https://www.1point3acres.com/interview/post/7100158（正文未读，仅标题）**[中]**
- **磁盘版/并发版**："Design a Disk-Backed KV Store Under Contention"，Easy 难度，考"durable on-disk storage, indexing"与并发；PracHub 标注 529 人做过、2026-03-01。—— https://prachub.com/companies/snowflake/positions/software-engineer/categories/system-design（访问 2026-09-13）**[低，AI 题库聚合站，仅作题型参考]**
- **序列化版**："Durable Key-Value Store Serialization" —— 1point3acres 问题库 https://www.1point3acres.com/interview/problems/post/7100062（仅标题）**[中]**
- **面经索引确认**：Blind 帖 "Snowflake System Design and Leetcode Questions" 提到 KV store 相关设计题存在于其面试库中。—— https://www.teamblind.com/post/snowflake-system-design-and-leetcode-questions-a83swi3f（访问 2026-09-13，仅标题/摘要）**[中]**
- **复用 P**：P §3.2 #7 记录 2025-12 两轮 back-to-back 电面中的 "KV store 系统设计" —— 1p3a thread-1158595（搜索摘要）**[medium，复用 P，原采集 2026-09-13]**

**追问汇总**（跨版本合并）：单分区强一致 vs 跨分区事务如何做（2PC/Raft）；快照/time travel 如何不无限增长（compaction）；副本一致性协议选型；分布式版本号 vs 向量时钟；range scan 如何在 LSM/B-tree 结构上实现。

### 1.2 Quota System（多个上游服务共用的配额系统）

- **一手**：P §3.2 #8 "Design a Quota System used by multiple upstream services" —— 1p3a thread-1137616（搜索摘要，标注"可用 AI"的帖子语境）**[medium，复用 P]**
- **聚合站细节版**（与 P 的题目同源，细节更完整）：Quota Service 要求 **strong consistency** 防止 client 超过资源上限，应用场景举例为"文件上传"；APIs 需支持 SET quota。—— staffengprep.com（访问 2026-09-13）**[中]**
- **另一变体**："Design a Multi-Tenant Quota System" / "Global Multi-Tenant Quota Service (Single Global Quota per User)"，Hard 难度，PracHub 标注 621 人做过、2025-09-06。—— https://prachub.com/companies/snowflake/positions/software-engineer/categories/system-design（访问 2026-09-13）**[低]**
- 归类页面显示该题族标签为 "Quotas/Distributed-Systems/Rate-Limiting/Caching"（60 min 归类下的独立报告）。—— staffengprep.com **[中]**

**追问汇总**：强一致 vs 最终一致的取舍（配额超发的业务后果 vs 延迟）；本地缓存配额+定期同步 vs 每次请求打中心服务；多区域部署下的全局配额如何不产生单点瓶颈；client 侧限流与服务端配额的分层。

### 1.3 SQL Notebook / 查询结果分发（"类 LeetCode 运行 SQL"）

- **一手（电面 SD，两轮 back-to-back 之一）**：题面为 "a notebook similar to SQL that supports users running queries"，讨论重点是 **client 如何拿到查询结果**（长查询的轮询/推送、结果分页、大结果集的流式返回）。—— 1p3a thread-1187965，经 Telegram 镜像 t.me/s/usinterview/29571 读到 **[高，复用 P §3.2 #6]**
- **新增一手**：Telegram 搜索命中另一条 2026 全职 fullstack 电面报告："System Design: SQL notebook interface"，与 coding 轮（React/TypeScript 做一个 Kanban 板：左右箭头移动任务、到边界隐藏箭头、无拖拽；follow-up 要求"最近变更状态的任务永远排在列表底部"）在同一场电面出现。—— https://www.1point3acres.com/bbs/thread-1186357-1-1.html，经 t.me/s/usinterview 搜索命中（访问 2026-09-13，正文 403 未读，摘要经二次 WebFetch 提炼）**[高，日期/轮次/结果未知，仅摘要]**
- **聚合站对应题**："Design an Interactive Query Execution Notebook"（Medium，Software Engineer），题面 "Design a notebook-like service in which users submit SQL queries and receive results"，PracHub 标注 42 人做过、2026-08-24（发布/收录日期，非面试日期）。—— https://prachub.com/companies/snowflake/categories/system-design（访问 2026-09-13）**[低，但与两条一手报告的题面高度吻合，可信度上调为可参照真题]**

**追问汇总**：长查询异步执行模型（submit → poll status → fetch result）；结果集过大时怎么分片/流式传输给 notebook 前端；多用户共享 notebook 的并发编辑/执行隔离；查询排队与仓库资源调度的关系（可联系 Snowflake 真实的 virtual warehouse 排队机制）。

### 1.4 "SQL engine running many queries as a cron job"

- **一手**：Blind 帖 "Snowflake IC1/IC2 System Design Interview"（2025-07-03）：题面为设计一个 **SQL 引擎，把大量查询当 cron job 跑**；面试官全程沉默（"面试官很沉默"）。—— https://www.teamblind.com/post/snowflake-ic1ic2-system-design-interview-1dd4vqt7（2025-07-03）**[高，复用 P §3.2 #9]**
- 说明：这题与 Snowflake 真实产品 **Tasks（CRON 或间隔调度、可组成 DAG）** 高度对应（见 C §2.3），面试官可能就是想看候选人能不能推导出"调度 + 幂等重试 + 失败隔离"这套 Snowflake 自己内部也在用的模型。

### 1.5 Job / Cron Scheduler（调度器）

- **聚合站**（与 §1.4 题面重合但作为独立收录条目）："Design a Cron Job Scheduler"（Medium），题面 "Design a distributed cron job scheduler — a service that triggers user-defined jobs"，PracHub 标注 **768 人做过、2026-04-12**（该题库里被做次数最高的 Snowflake SD 题之一）。—— https://prachub.com/companies/snowflake/categories/system-design（访问 2026-09-13）**[低，但样本量在该聚合站内最大，值得优先练]**
- "Design a Reliable Job Scheduler"（Hard），题面 "Design a fault-tolerant scheduler for one-time and recurring jobs"，89 人做过、2026-06-09。—— 同上 **[低]**
- "Design Multi-Core Service Startup Scheduler"（Hard）："Service Startup Scheduler on a Host with M CPU Cores"，用 DAG 表达依赖，215 人做过、2025-09-06。—— 同上 **[低]**；对应 P §3.2 #11 "Service Startup 依赖排序 (Kahn)"，来自 linkjob 2026-03-16 **[low，复用 P]**
- **复用 P**：P §3.2 #12 "Job Scheduler 等（'snowflake system design 大汇总'）"，1p3a thread-1091322（正文 403）**[medium，复用 P]**；本文件重新尝试抓取该帖仍返回 403（2026-09-13）。

### 1.6 Distributed Queue Service（分布式队列服务）

- **一手**：P §3.2 #5 "Queue class（类 Python deque）→ 扩展为云端 queue service"，讨论 enqueue/dequeue 在故障下的行为；onsite SD，候选人未通过。—— t.me/s/usinterview/29299 → 1p3a thread-1185881 **[高，复用 P]**
- **归类页证据**：StaffEngPrep 把 Snowflake SD 报告归到 "Distributed-Systems Scheduling/Queueing/Persistence"（60 min，4 篇独立报告合并——该仓库单一题族里报告数最多）、"Distributed-Systems Queueing/AI-Tools/Idempotency"（60 min，1 篇）、"Distributed-Systems Ingestion/Queueing/Frontend"（60 min，1 篇）。—— staffengprep.com/companies/snowflake（访问 2026-09-13）**[中]**

**追问汇总**：故障时 enqueue 是否需要确认落盘再返回；at-least-once vs exactly-once 消费；多消费者的公平调度/优先级队列；队列积压时的背压策略。

### 1.7 Audit-Log Service（审计日志服务）

- **索引标题**：P §3.2 #10 记录 1p3a 面经索引里的标题 "Design Audit Logs Service"（无法读到正文）。—— https://www.1point3acres.com/interview/company/snowflake **[medium，复用 P]**
- **聚合站细节**："Design an Audit Logs Service"（Medium），题面 "scalable, multi-tenant audit logging system, covering event storage"，PracHub 标注 278 人做过、2026-06-17。另一独立描述："tamper-evident retention, and efficiency" 是该题族的评分点。—— https://prachub.com/companies/snowflake/categories/system-design ；WebSearch 摘要（访问 2026-09-13）**[低-中]**
- 与 Snowflake 自身产品对照：Snowflake 官方有内建的 `SNOWFLAKE` 共享数据库暴露审计信息，增量导出依赖时间戳列——面试题很可能是这个真实痛点的简化版（详见 C §3.1 关于审计/治理团队 Horizon Catalog 的描述）。**[推断]**

### 1.8 Dynamic Blacklist Filter System（动态黑名单过滤系统）

- **唯一来源**：P §3.2 #10 记录 1p3a 面经索引标题 "Dynamic Blacklist Filter System"，无法读到正文，日期不详。—— https://www.1point3acres.com/interview/company/snowflake **[medium，复用 P]**
- 本文件用 6 条不同关键词组合的 WebSearch（blacklist filter / dynamic blacklist / IP blacklist system design snowflake 等）**均未找到第二个独立来源**。结论：**未找到补充证据**，维持 P 的单来源标题级记录，置信度不上调。

### 1.9 Password Storage（密码存储系统设计）

- **一手**：同一场电面/onsite 报告里，coding 轮是 **Happy Number**（先 O(n) 后用 Floyd 判环优化到 O(1)），SD 轮是 **"Design user password storage"**；前 ~20 min 讲候选人自己的项目。—— t.me/s/usinterview/28738 → 1p3a thread-1179571（2026 夏）**[高，复用 P §3.2 #3]**
- 本文件用 Telegram 搜索重新定位到该帖标题："General Store Interview" — "Coding: Happy Number problem (optimized to O(1)); System Design: User password storage system"，与 P 记录完全一致，属**同一手材料的重复确认**，非独立第二来源。—— t.me/s/usinterview?q=snowflake（访问 2026-09-13）**[高，确认但非新增来源]**
- 未找到该题的具体追问细节（如是否问到 bcrypt/scrypt 参数选择、彩虹表防御、密钥轮换）；聚合站搜索（password storage system design snowflake）无进一步命中。**[未找到追问]**

### 1.10 DAG Cache for Query Views / Materialized Views（查询视图/物化视图的 DAG 缓存）

- **聚合站**："Design Cache for DAG-Based Query Views"（Hard），题面 "Caching Strategy for a DAG of Materialized Views" in analytics systems，PracHub 标注 220 人做过、2025-09-06。—— https://prachub.com/companies/snowflake/categories/system-design（访问 2026-09-13）**[低]**
- **复用 P**：P §3.2 #11 提到 linkjob 2026-03-16 收录 "DAG cache for query views"，与上条同源题面。**[low，复用 P]**
- 与 Snowflake 真实产品对照：这题几乎是 **Dynamic Tables**（依赖图、增量 vs 全量刷新判断、`TARGET_LAG`）的简化面试版——见 C §2.4。面试时可直接借用 Dynamic Tables 的"依赖图 + 增量判定 + 一致快照"框架作答。**[推断]**

### 1.11 Metering & Billing（计量与计费）

- **未找到一手 SD 面试报告**直接以"设计计量/计费系统"为题面。相关的是 JD 层面的证据：**Software Engineer - Billing Platform**（Menlo Park，已下线，2025-06-03 移除）明确要求"Build a reliable and scalable Billing Platform leveraging Snowflake technologies"、"real-time usage metering"，属于团队方向而非已证实的面试题。详见 `process_and_jd.md` JD 分析部分。—— https://builtin.com/job/software-engineer-billing-platform/4472400（访问 2026-09-13）**[中，JD 证据，非面试题证据]**
- 结论：计量与计费更可能出现在 **Billing/Metering 团队的 expertise 轮或专属团队面试**里，而非通用 GenSWE SD 题库；不要按"必考题"准备，但值得知道 Snowflake 计量口径（credits/秒、10% Cloud Services 免费额度，见 C §3.1）以备追问。

### 1.12 Rate Limiter（限流器）

- **Onsite 一手/半一手**：Sliding-window rate limiter，"processing request timestamps in order, every request at time t is allowed only when fewer than limit previously allowed requests have timestamps in the half-open interval (t - windowSeconds, t]"——FastPrep 把它标注为 **Snowflake Onsite Interview** 的题目。—— https://www.fastprep.io/problems/snowflake-sliding-window-rate-limiter（访问 2026-09-13）**[中，培训站转述但题面具体到公式级别，疑似真实拿到原题]**
- **分布式版**（更像 SD 而非 coding）：Design a distributed rate limiter，"enforces a per-second throttling limit"，重点"如何在不产生 hot-spotting 或 thundering herd 的前提下让限流尽量精确"。—— staffengprep.com（访问 2026-09-13）**[中]**
- **复用 P**：P §3.2 #13 引用 prachub 汇总 "thread-safe multi-rule rate limiter"。**[low-medium，复用 P]**
- 归类页面标签 "Distributed-Systems Access-Control/Caching/Throttling"（60 min，另有 1 篇独立报告）。—— staffengprep.com **[中]**

**追问汇总**：token bucket vs sliding window 精度/内存权衡；多实例共享限流状态（Redis 原子操作）；多规则（per-user + per-IP + 全局）如何叠加；限流后的降级策略。

### 1.13 Web Crawler（网络爬虫）

- **Coding 版**：用 BFS + Queue + HashSet/Bloom Filter 去重；也有 DFS 记录深度的变体，"follow-up discussion on how to scale the solution"。—— WebSearch 综合多个聚合站（PracHub、Educative 等，访问 2026-09-13）**[低-中]**
- **SD 版**："Design a Concurrent Web Crawler"（Hard），题面 "Concurrent web crawler that starts from a given URL"，PracHub 标注 209 人做过、2025-09-06；归类页标签 "Web-Crawler/Distributed-Systems/Queueing/Scaling"（单篇报告）。—— https://prachub.com/companies/snowflake/categories/system-design ；staffengprep.com（访问 2026-09-13）**[低-中]**
- **复用 P**：P §3.2 #11 引用 linkjob 收录的 "Web Crawler (BFS)"。**[low，复用 P]**

### 1.14 其他发现的 SD 题目（原任务清单之外）

以下题目来自同一批聚合站抓取（主要是 PracHub 题库页与 StaffEngPrep 归类页），**未必对应真实 Snowflake 面经**，但因为该聚合站对其他已验证题目（KV store、Quota、Cron Scheduler、SQL Notebook、Audit Log、DAG Cache、Web Crawler）的题面描述与一手报告高度吻合，故一并收录供覆盖率参考，标注 **[低]**：

| 题目 | 题面摘要 | 来源 |
|---|---|---|
| Automated Jira-Ticket-to-PR System | "distributed systems, asynchronous job processing, queue-based architecture" | PracHub，Hard，185 人做过，2026-06-15 |
| Object Store with Deduplication | "Simplified cloud object storage service" for upload/download，内容去重 | PracHub，Medium，420 人做过，2025-12-15；对应 staffengprep "Blob Storage De-duplication" |
| Distributed Tree Node Counter | "Distributed Tree Node Count with Two Messages" | PracHub，Medium，496 人做过，2025-07-26；对应 P §3.2 #10 "Distributed Tree Counting" |
| REST API Abstraction Layer | "Internal Service-Client SDK" | PracHub，Hard，258 人做过，2026-04-05 |
| Multi-Tenant Interactive Analytics Platform | 数据摄取与查询的端到端设计 | PracHub，Hard，300 人做过，2025-09-06 |
| Distributed Metadata Catalog and Schema Registry | "Design Under Vague Distributed Requirements" | PracHub，Hard，181 人做过，2025-09-06 |
| ACL Authorization Checking Service | "centralized authorization/ACL models, API and data modeling" | PracHub，Hard，295 人做过，2026-01-06 |
| Resilient Auth with Flaky Third-Party Tokens | "Multi-region, HTTP/JSON API" 应对不可靠第三方鉴权 | PracHub，Hard，171 人做过，2025-09-06 |
| Geolocation Search Service | "requirements, architecture, trade-offs" | PracHub，Medium，338 人做过，2026-07-04 |
| Event Subscription System | 1M/s QPS 用户通知 | staffengprep.com，无日期 |
| Distributed Transaction Protocol | 跨分区 key 更新，serializability，两阶段提交 | staffengprep.com（KV store 题的 follow-up 延伸） |
| Async Task Scheduler Service | 用户自定义函数，"at-least once" 执行保证 | staffengprep.com |

**关于 Automated Jira-Ticket-to-PR System 的一手印证**：本文件在 Telegram 镜像中找到一条**独立的一手报告**与这个聚合站题目吻合——加拿大 mid-level（推测 IC2）候选人 onsite 报告："设计一个内部工具，需要构建一个自动能 handle jira ticket 的系统"，候选人形容"very unique"（不常见）。—— https://www.1point3acres.com/bbs/thread-1180916-1-1.html，经 t.me/s/usinterview 搜索命中（访问 2026-09-13，正文 403，仅摘要）**[高置信度存在，追问细节未知]**——这是本文件里少数**聚合站题库与一手面经互相印证**的条目，建议优先准备。

---

## 2. Snowflake SD 面试风格综合画像

### 2.1 时长与结构

- 60 min 是最常见的报告口径（电面阶段"两轮 back-to-back，每轮约 1 h"，见 P §1.3）；45 min 出现在部分聚合站对"经验候选人 onsite"的描述中（Aced/Exponent：virtual onsite 4-5 轮 × 60 min，含"infrastructure-oriented system design"一轮）。—— https://www.tryexponent.com/blog/snowflake-interview-process（访问 2026-09-13）**[中]**
- 三段式：开场自我介绍/项目讨论（部分报告里长达 15-20 min，见 P §4.2）→ 设计主体 → 提问环节；与 Stripe 的"45 min 含开场，真正设计约 30-35 min"结构类似，但 Snowflake 一手报告没有给出这么精确的分钟拆解。**[推断，类比 Stripe 记录方式，无 Snowflake 自己的精确数据]**

### 2.2 工具

- **未证实** Snowflake 官方指定的白板工具（不同于 Stripe 明确的 Whimsical）。聚合站泛泛提到 Excalidraw/Miro/CoderPad digital whiteboard 是"系统设计面试通用工具"，但没有任何一手报告点名 Snowflake 用的是哪一个。—— WebSearch 综合（访问 2026-09-13）**[中，工具本身未证实，仅说明行业惯例]**
- **Coding 轮确认用 CoderPad**（P §1.3 引用 Blind ICT2 帖 "2 1 hours coding rounds on coderpad"），SD 轮是否共用同一平台的白板功能未知。**[高，复用 P，仅限 coding 轮]**

### 2.3 面试官行为：两极分化

- **"人很好"一派**：多条一手报告（Telegram 镜像转述）："人都很好"，会给 hint、帮 debug（P §3.2 综合）。**[高，复用 P]**
- **"沉默"一派**：Blind 2025-07-03 IC1/IC2 SD 报告明确"面试官很沉默"（interviewer remained largely silent），候选人需要**主动推进设计、主动提出假设**，因为不会有面试官追问式的引导。—— https://www.teamblind.com/post/snowflake-ic1ic2-system-design-interview-1dd4vqt7（2025-07-03）**[高，复用 P]**
- **结论**：两种风格并存，因人/团队而异；备考策略应假设"面试官可能不主动引导"，练习**在无提示情况下自己说出假设、边界条件、trade-off**，而不是依赖面试官提问来暴露设计漏洞。

### 2.4 Infra/Data 味道

- 多个独立来源用几乎相同的措辞描述 Snowflake SD 题的性格："不像标准的'设计一个通用 web 服务'面试，更接近 data-platform 问题"（"tend to be much closer to data-platform problems"）；"skews toward distributed systems, data warehousing, and cloud-native architecture"；"避免泛泛而谈，要讨论网络协议、磁盘 I/O 优化、精确的分片 key"。—— 综合 WebSearch 结果（PracHub、SystemDesignHandbook、AlgoMonster，访问 2026-09-13）**[中，多源一致但均为聚合站转述]**
- 这与本仓库 `company_research.md` §2 记录的 Snowflake 真实架构（micro-partitions、FDB 元数据、Streams/Tasks、Dynamic Tables）高度呼应——面试题库里的 "KV store + versioning"、"DAG cache for materialized views"、"cron job scheduler"、"queue service" 几乎是这些真实系统的简化重述，说明**用 Snowflake 自己的工程博客词汇作答**（micro-partition、FDB、execution anchor、stream offset）大概率是加分项。**[推断]**

### 2.5 "Hire" 门槛与电面/onsite 的权重差异

- Blind（ex-Google, IC2, 2025-10-04）："Despite seemingly doing quite well ... on the first two tech screens, I got called in for a 3rd due to coding speed."；评论区："The first two are just screens, doesn't signal anything"；"you need to get Hire in all the remaining ones."—— https://www.teamblind.com/post/snowflake-onsite-tips-wzrlktbi（复用 P §1.3）**[高]**
- 本文件新增一手：加拿大 IC1（Product Experience org）候选人报告"两轮技术电面通过 + 三轮 onsite 通过"后进入 HM matching 阶段，说明**IC1 级别 onsite 至少 3 轮**（与 P 记录的"4-5 轮"上限并不矛盾，可能因 org 而异）。—— https://www.teamblind.com/post/passed-all-rounds-at-snowflake-then-silence-z4cg3oq0（2025-06-04 附近，帖子提及"about 1 month before June 4, 2025"启动）**[高]**

---

## 3. Contradictions / unknowns（本文件新增，供 TALLY.md 参考）

1. **白板工具未证实**——不同于 Stripe（明确 Whimsical），Snowflake 没有任何一手报告点名具体工具。
2. **Dynamic Blacklist Filter System** 仅有标题级单一来源（1p3a 面经索引），6 组关键词检索均未找到第二来源或任何追问细节。
3. **Metering & Billing 未找到独立 SD 面试题**，只有 JD 证据（Billing Platform 团队方向）；不应按"通用必考题"准备。
4. **Password Storage 的追问细节未知**（是否问 bcrypt/scrypt 参数、彩虹表、密钥轮换均未见记录）。
5. **PracHub/StaffEngPrep/FastPrep 等聚合站的可信度分层**：本文件里凡是能与至少一条一手 Telegram/Blind 报告题面吻合的（KV store、Quota、SQL Notebook、Cron Scheduler、Rate Limiter、Jira-Ticket-to-PR），可信度上调为"可参照真题"；其余仅标题匹配、无一手印证的（Object Store Dedup、REST API Abstraction Layer、ACL Service、Metadata Catalog 等）应视为**该聚合站自建题库**，练习价值仅供覆盖面，不代表已证实的 Snowflake 原题。
6. **1p3a thread-1091322（"snowflake system design 大汇总"）与 thread-978440/1049039（雪花店面系统设计/挂经）本文件仍无法直接抓取正文**（403，含标准 UA 与追加 Referer 均未测试出新路径），只能依赖标题与既有搜索摘要。
