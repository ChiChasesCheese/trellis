# Snowflake 面试题目总表（GenSWE / Software Engineer - Backend，IC1–IC2）

**日期：** 2026-09-13 · **输入：** `catalog/raw/{coding_oa,coding_phone_onsite,ood,TALLY,system_design,bq_hm_recruiter,process_and_jd,sources_index}.md` + `catalog/discovery/`（Reddit 35 帖全文 · HN 6 · 1p3a 镜像 21 帖；`TRIAGE.md` 46 行）+ `../raw/{process_research,company_research,chakra}.md`（AI 轮 dossier）
**排序：** `RANK.md`（打分输入）→ `tools/pareto.py` → `PARETO.md`（输出）。**cut line = 前 35 行（66 行的 53%，2026-09-13 收割回写后重跑）**，refs 分布平（大量单来源），所以宽于 Stripe 的 20/42。

## 格式事实（多源交叉，细节与 URL 在 raw/）

- **漏斗**（早期职业 GenSWE）：投递 → Chakra AI 语音筛（20 min，BQ + 项目，无 coding）→ HR/HM call 15–30 min → [HackerRank OA 2–3 题 / 90–135 min，实习与新毕业为主，2026 全职一手几乎无 OA] → **两轮 back-to-back 技术电面各 60 min**（1 coding + 1 SD，或 2 coding；10 min 介绍 / 40 min 题 / 10 min 反问）→ **onsite 4–5 轮 × 60 min**（coding ×1–2、resume/expertise、SD、BQ/manager）→ team matching → offer。官方 2–4 周；一手内推→约面 4 天。
- **OA**：HackerRank；2–3 题；90 min（2021–22 实习）→ 135 min（2025 Infra 实习，2 DP + 1 回溯）→ 120 min（2026 NG 聚合站，LOW）；语言曾限 Java/C++；题目在 OA 与电面池之间**复用**（Wiki BFS、Patching Array、Inorder 都两边出现）。
- **电面**：LC medium 为主 + 更难 follow-up；OOD/类设计频率高（task scheduler、KV、文件系统、限流器）；"coding wasn't LC style but something random" 与 "LC hard on the screens" 并存——按 org 不同。前 15–20 min 常先讲项目。
- **SD**：45–60 min；infra/data 味（KV、quota、调度器、队列、审计日志、DAG 缓存、SQL 引擎）；面试官两极（多数给 hint，至少一例全程沉默）；白板工具未证实；coding 用 CoderPad。
- **通过线**：电面"只是 screens，不 signal"；onsite **每一轮都要 Hire**；1.5 YOE 大概率 IC1（Bay Area 中位 TC $236K），可能 down-level；team matching 是真实门槛（有全过后因 headcount 被搁置的一手案例）。
- **onsite 需签 NDA**（HN 2025-01 一手，Databricks/Snowflake/Stripe 同）；被拒后可要求反馈，有人经 GDPR DPO 请求拿到面试记录（HN 2025-06，EU 适用）。
- **岗位 must-have**（6 份 JD）：SQL 5/6 · 分布式系统 5/6 · 数据库内部 5/6 · 算法与数据结构 5/6 · Java 4/6 · 大规模生产系统 4/6 · C++ 2/6 · 并发明确写出 1/6。

## 计数与置信度

`#refs` = 独立来源数：同一候选人跨站 1；聚合站互抄 1；同一题 base + follow-up 1；PracHub "Last Updated" 是重建索引日期，只作时效下限。**high** = 一手候选人原帖/逐字题面/LC 原题确认复用；**medium** = 单一结构化题库（FastPrep/PracHub/1p3a 题库）细节具体，或 ≥2 独立来源一致；**low** = 单一 SEO/AI 站（interviewfox、linkjob 的 "2026 OA 回忆" 互相矛盾，封顶 low）。lodely / vervecopilot 不采信。一条跨公司误标（"Grid Land" 实为 Lucid 2020 OA）已剔除。

轮次缩写：**OA** HackerRank · **PS** 技术电面 · **VO** onsite coding · **SD** 系统设计 · **EXP** expertise/项目深挖 · **HM/BQ** · **TM** team matching · **AI** Chakra。

---

## Table A — 编码题（OA / 电面 / onsite）

| ID | 题 · 别名 | 轮次 | Part / 递进 | 最近 | #refs | 置信度 | 来源（细节见 raw §） |
|---|---|---|---|---|---:|---|---|
| **pc01** | **RBAC / DAG 权限继承题族**：Effective Access Control · Effective Role Privileges · ACL Local-only Deny · Resolve Inherited Allow/Deny · Letter Permissions | PS | 4：直接权限 → 祖先继承（DAG 多父）→ deny 覆盖 allow / 仅本地 deny → 反向查询（谁拥有某权限 / 按角色过滤）| 2026-09 | 5 | MED-HIGH | fastprep ×3 · prachub ×2；raw/coding_phone_onsite #8–12；Stripe 的 ps10 同族 |
| **q02** | **元音游程 DP 题族**：长度 n、连续元音 ≤ k 的串数 · String Patterns `calculateWays(wordLen,maxVowels)` mod 1e9+7 · Vowel Substring（LC 1987/2062）| OA | 3：计数 DP(位置, 游程) → 模数与 n ≤ 2500 → 子串变体 | 2026-06 | 5 | MED-HIGH | LC 2550834（2022 逐字）· fastprep calculate-ways · 2023 索引 · linkjob；raw/coding_oa #2 #3 #14 #18 |
| **q03** | **树高压缩题族**：Minimum Height（换根 ≤ max_ops）· Minimum N-ary Tree Deletions（删最少叶子使深度 ≤ k，输出 id 升序）· Prune Multiway Tree（只计数）| OA + PS | 3：深度计算 → 贪心/DP 选删 → 换根操作 | 2026-08 | 3 | MED-HIGH | fastprep ×2 · prachub；raw/coding_oa #41、coding_phone_onsite #15–16 |
| **q01** | **Task Scheduling — paid vs free server**（cost[i]/time[i]，付费机忙时可选免费机 1 单位时间；求最小成本）| OA | 2：DP over (i, 付费机剩余时间) → 复杂度优化 | 2026-03 | 3 | HIGH | LC 2550834（逐字）· linkjob 2026 · 2023 索引；raw/coding_oa #1 |
| **pc03** | **Recent Event Stream Queries**：保留最近 m 条事件；`record ts key` / `count ts`（ts 前不同 key 数）/ `top`（最频 key，字典序 tie）· 1p3a "Event Stream Problem" | PS | 3：滑窗 deque → 计数哈希 → top 维护 | 2026-08 | 3 | MED | fastprep · prachub · 1p3a 索引；raw/coding_phone_onsite #13 |
| **pc10** | **Distributed Tree Counting 状态机**：root 广播 GET_COUNT，叶子回 1，内部节点等齐子节点再上报；FIFO exactly-once 消息日志 | PS | 2：模拟消息总线 → 日志格式与顺序 | 2026-07 | 3 | MED | fastprep · prachub "Distributed Tree Node Count" · 1p3a 索引；raw/coding_phone_onsite #14、ood #7 |
| **q04** | **Maximum Order Volume / phone calls**：start/duration/volume，不重叠选最大 volume（LC 1235 型） | OA | 2：排序 + 二分 + DP → n ≤ 1e5 | 2025-03 | 3 | MED | LC 1033329（2021）· fastprep phone-calls · 2023 索引；raw/coding_oa #4 |
| **pc02** | **Closest Bathroom / Desk on a Grid**：多源 BFS，每个 D 到最近 B 的曼哈顿步数，无 B 则 -1 | PS | 2：多源 BFS → 1000×1000 内存 | 2026-09 | 2 | MED-HIGH | 1p3a 题库（公开预览）· fastprep "High Frequency"；raw/coding_phone_onsite #4 |
| **pc04** | **Web Crawler Shortest Path Reconstruction**：BFS 找最短点击路径并重建 | PS | 2：BFS + parent 表 → 扩展讨论 | 2026-09 | 2 | MED | fastprep · linkjob；raw/coding_phone_onsite #5 |
| **q05** | **Paint the Ceiling**：`s_i = ((k·s_{i-1}+b) mod m)+1+s_{i-1}` 生成 n ≤ 6e6 边长，数 area ≤ a 的对 | OA | 2：生成 → 排序双指针/二分计数 | 2026-03 | 2 | MED | fastprep · linkjob 2026；raw/coding_oa #23 |
| **q06** | **Patching Array**（LC 484 原题）| OA + PS | 1 | 2023-02 | 2 | HIGH | LC 424385（2019 电面逐字）· 2023 索引；raw/coding_oa #9 |
| **q07** | **Binary Tree Inorder Traversal**（LC 94）+ **Morris** 追问 | OA + PS | 2 | 2023-02 | 2 | MED-HIGH | 2019 电面 · 2023 索引；raw/coding_oa #22 |
| **q08** | **Course Schedule II**（LC 210）· 电面"prerequisite 拓扑排序" | OA + PS | 2 | 2023-02 | 2 | MED-HIGH | 2023 索引 · 2022 电面；raw/coding_oa #16 |
| **q09** | **Server Selection**：m 服务器 × n 项 2D DP，目标 O(m·n)（题面仅截图） | OA | 2 | 2023-02 | 2 | MED（image-only） | LC 2594968 / 2794537；raw/coding_oa #5 |
| **q10** | **Minimum Clicks Between Wiki Pages**（图 BFS；OA 与 PS 池都有） | OA + PS | 1 | 2026-09 | 1 | MED | fastprep；raw/coding_oa #29 |
| **pc05** | **LC 1751 Maximum Number of Events That Can Be Attended II 变体** + follow-up（40 min） | PS | 2 | 2026-06 | 1 | HIGH | 1p3a thread-1179486 / t.me 28733；../raw/process_research §3.2 |
| **pc06** | **Happy Number**：O(n) → O(1) Floyd 判环；同场前 20 min 讲项目 | PS/VO | 2 | 2026-07 | 1 | HIGH | t.me 28738 → 1p3a thread-1179571 |
| **pc07** | **Word Search II**（LC 212）+ 审计日志设计（senior 电面二合一） | PS | 1 + SD | 2024-02 | 1 | HIGH | LC 4727339 逐字 |
| **pc08** | 2019 两轮电面：Array-diff removal → Inorder（Morris）→ Patching Array | PS | 3 | 2019-11 | 1 | HIGH | LC 424385 |
| **pc09** | **Parallel Courses III**（LC 2050 原题） | VO | 1 | 2026-08 | 1 | MED-HIGH | fastprep；Stripe 库有 qA09 可直接复用 |
| **pc11** | Character Frequencies（跨字符串 / 嵌套列表） | PS | 2 | 2026-06 | 1 | MED | fastprep |
| **pc12** | Top Two Users by Total Purchase Amount | PS | 1 | 2026-06 | 1 | MED | fastprep |
| **q11** | Generating Login Codes（New Grad OA，仅标题+标签 Two-Pointers） | OA | ? | 2026-09 | 1 | MED | fastprep |
| q12–q17 | LC 原题复用：Merge Intervals 56 · Min Interval to Include Each Query 1851 · Palindromic Subsequences 2002 · Graph Valid Tree 261 · String Formation 1639 · Remove Stones 1962 | OA | 1 | 2023-02 / 2024-12 | 1 each | MED | 2023 Canada 索引（链接指向 LC 原题） |
| q18 | Min-Height-Trees 图变体（LC 310 + twist） | OA | ? | 2026 | 1 | LOW-MED | interviewfox |
| pc13 | Service Startup / Dependency Ordering（Kahn） | PS | 1 | 2026-03 | 1 | LOW-MED | linkjob；Stripe cd/int 有同族 |
| pc14 | Meeting Rooms II（LC 253 型，2026 实习 VO） | VO | 1 | 2026 | 1 | LOW | 1p3a post/7546739（登录墙） |
| pc15 | Parentheses Matching | PS | 1 | 2026-03 | 1 | LOW | linkjob |
| pc16 | Reverse Alphanumeric Segments | PS | ? | 2026 | 1 | LOW-MED | 1p3a 索引标题 |
| **q19** | **Maximize OR-Sum**（k 次翻倍操作最大化按位或之和；贪心 + 位运算） | OA（AIML 实习） | 2：暴力 → 前后缀 OR + 把所有翻倍给一个数 | 2026-05 | 2 | MED-HIGH | Reddit r/cscareerquestions 1t0ogu7 一手（2026-05-01）· interviewfox；discovery/TRIAGE #4 |

**Table A：30 行**（含 6 条 LC 原题合并行；q19 由 2026-09-13 收割一手升级）。

## Table B — OOD / 类设计 / 并发（每题都有并发追问，见 raw/ood.md "Cross-cutting"）

| ID | 题 | 轮次 | 递进 | 最近 | #refs | 置信度 | 来源 |
|---|---|---|---|---|---:|---|---|
| **od01** | **Task Scheduler** `add(id,priority,ts)` / `execute()`：优先级 → 早时间戳 → 小 id；**重复 ID**：任一执行后其余永久失效；并发；持久化 | VO | 4：优先队列 → 重复抑制 → 线程安全 → 崩溃恢复 | 2026-08 | 3 | HIGH | fastprep ×2（一题两半）· 1p3a 一手 t.me 29167（挂经）；raw/ood #1 |
| **od02** | **In-Memory File System**（LC 588）：ls/mkdir/addContentToFile/readContentFromFile；追问 rm/rmdir、分块大文件、锁、快照 + WAL | PS | 4 | 2026-08 | 4 | HIGH-MED | fastprep · GitHub(darkinterview) · prachub · techprep；raw/ood #3 |
| **od03** | **Transactional in-memory KV store**：get/put/delete/begin/commit/rollback 嵌套；追问多线程线性一致（每线程事务栈） | 技术筛 | 3：单事务 → 嵌套 → 并发 | 2026-08 | 1 | HIGH-MED | prachub（Hard）；xAI 同形题提示非 Snowflake 独有；raw/ood #2 |
| **od04** | **Rate Limiter** 两变体：onsite 滑窗单规则 `acceptRequests`；电面**多规则排队线程安全** `simulateRateLimiter`（所有规则同时有余量的最早时刻） | VO + PS | 3：单规则 → 多规则 → 原子/线程安全 | 2026-08 | 2 | MED | fastprep ×2；Stripe q23/cd04 可复用骨架；raw/ood #4 |
| **od05** | **Cron Scheduler 类**：schedule/pause/resume/tick；多实例不重复触发（lease/claim）、崩溃不丢触发 | 技术筛 | 4：API → 数据模型 → tick 循环 → 多副本 lease | 2026-06 | 2 | LOW-MED | prachub ×2；与 Snowflake Tasks 产品对应；raw/ood #5 |
| **od06** | **Query Audit Log 类**（"pg_stat for Snowflake"）：record_access / accessed_in_range / unaccessed_since | PS | 2 | 2024-02 | 1 | HIGH | LC 4727339 逐字；raw/ood #6 |
| **od07** | **Throne Inheritance without initial king**（LC 1600 变体，空族谱起步） | PS | 2 | 2026 | 1 | MED | fastprep（Source Match 86%）；raw/ood #8 |
| **od08** | **LRU Cache**（warehouse SSD cache 框架）+ TTL / 多级缓存追问 | VO | 3 | 2026 | 3（主题级） | LOW-MED | staffengprep · interviewchamp · techprep；raw/ood #9 |
| **od09** | **Queue 类（类 deque）→ 云端 queue service**：enqueue/dequeue 在故障下的语义 | VO | 2 + SD | 2026-08 | 2 | HIGH | 1p3a 一手 t.me 29299（挂经）· staffengprep 归类 |

## Table C — 系统设计（细节、追问、对应 Snowflake 产品见 raw/system_design.md）

| ID | 题 | 轮次 | 面试官会压的点 | 最近 | #refs | 置信度 |
|---|---|---|---|---|---:|---|
| **sd01** | **KV Store**：PUT/GET/DELETE + getRange + point-in-time snapshot；分布式版：global versioning、time travel、单 key 强一致、Raft、跨分区事务（2PC） | PS + VO | 一致性协议、快照不无限增长（compaction）、版本号 vs 向量时钟、LSM 上的 range scan | 2026-09 | 5 | HIGH-MED |
| **sd02** | **Cron / Job Scheduler**（"SQL engine running many queries as cron job"，Blind IC1/IC2 一手；Reliable Job Scheduler；Service Startup Scheduler） | PS + VO | 幂等重试、失败隔离、多副本 lease、cron 粒度、1e6 job / 分钟级峰值 | 2026-07 | 4 | HIGH |
| **sd03** | **SQL Notebook / 查询结果分发**（两条一手） | PS | 长查询异步 submit→poll→fetch、大结果集分片/流式、多用户隔离、排队与仓库资源 | 2026-08 | 3 | HIGH |
| **sd04** | **Quota System**（多上游共用；多租户；文件上传场景） | PS/VO | 强一致 vs 本地缓存 + 定期同步；多区域无单点；client 限流分层 | 2026-06 | 3 | MED |
| **sd06** | **Audit / Query-Event Log Service**（多租户、防篡改、"哪些表/列在 t 内没被访问"） | PS/VO | 存储模型、时间窗查询、不可变、保留策略 | 2026-06 | 3 | MED-HIGH |
| **sd07** | **Distributed Rate Limiter**（per-second，多规则叠加） | PS/VO | token bucket vs 滑窗、Redis 原子、hot-spot / thundering herd、降级 | 2026-09 | 3 | MED |
| **sd05** | **Distributed Queue Service**（一手 onsite 挂经） | VO | 落盘确认、at-least-once vs exactly-once、优先级/公平、背压 | 2026-08 | 2 | HIGH |
| **sd11** | **Automated Jira-Ticket-to-PR System**（一手 + 聚合站互证） | VO | 异步任务、队列、幂等、失败重试、人审门 | 2026-06 | 2 | MED-HIGH |
| **sd08** | **DAG Cache for Query Views / Materialized Views**（≈ Dynamic Tables） | PS/VO | 依赖图、增量 vs 全量刷新判定、一致快照、失效传播 | 2026-03 | 2 | LOW-MED |
| **sd10** | **Concurrent Web Crawler** | PS/VO | 去重（Bloom）、礼貌性、分布式分片、扩展 | 2026-03 | 3 | LOW-MED |
| **sd09** | **User Password Storage**（一手，配 Happy Number 同场） | PS/VO | 哈希算法与参数、盐、密钥轮换、泄露响应 | 2026-07 | 1 | HIGH |
| **sd22** | **在两个 PB 级数据库之间同步数据**（IC2 Backend 一手；**不允许需求澄清**，候选人称"worst 30 minutes"） | PS/VO | CDC vs 快照 + 增量、一致性校验、回填、限速、schema 演进、断点续传 | 2026-03 | 1 | HIGH |
| **sd12** | Object Store with Deduplication | VO | 内容寻址、引用计数、GC | 2025-12 | 2 | LOW |
| sd13–sd19 | ACL Authorization Service（TrueInterview 另报 Access Management，+1）· Metadata Catalog/Schema Registry · Multi-Tenant Analytics Platform · Resilient Auth with Flaky Tokens · Geolocation Search · Event Subscription（1M/s）· REST API Abstraction Layer（TrueInterview 2026-05 独立收录，升 MED） | VO | — | 2025–2026 | 1–2 | LOW–MED |
| sd23 | Cross-Platform Logging Library（TrueInterview 2026-03） | VO | 库设计：有界缓冲、丢弃策略、脱敏、动态调级 | 2026-03 | 1 | MED-LOW |
| sd21 | Metering & Billing —— **未见面试报道**，仅 Billing Platform JD；作为 expertise 轮/team 面试话题准备，不当必考 | — | credits/秒、10% Cloud Services 免费额、AI token 计量 | — | 0 | JD |

## Table D — 非编码轮（题库在 `loop/rounds/0{1,6,7,8}_*`，答案在 `../../core/answers/`）

| 轮 | 形式 | 问什么 | 评什么 / 挂点 | 来源 |
|---|---|---|---|---|
| **AI（Chakra）** | 20 min 语音，摄像头+全屏+单显示器 | 经历 / 场景 / 协作决策 / 反问（无 coding） | transcript 证据：clarity · ownership · structured reasoning · specific examples；theoretical = Not Met | `../03-chakra-playbook.md`、`../raw/chakra.md` |
| **Recruiter/HR** | 15–30 min | 背景、infra 经验、方向偏好、why Snowflake、时间线；不报薪资数字 | 具体化的 why（不是"大厂"）| raw/bq_hm_recruiter §1 |
| **Expertise / 项目深挖** | 早期职业：嵌在 coding 轮前 15–20 min + onsite 一轮 resume；IC3 独立 40 min | 选一个项目：why/how 每个决策、备选方案、外部库、可用性/容错 | 只会"做了什么"讲不出"为什么、还有什么选项、现在怎么重做" | raw/bq_hm_recruiter §3 |
| **HM / BQ** | onsite 一轮 30–45 min，逐题记笔记 | mistake · ownership · 陌生团队协作 · teamwork · conflict · pushback（disagree-and-commit）· prioritize · customer first · raise the bar | 8 条价值观逐条对应（Own It / Get It Done / Integrity Always 最常）| raw/bq_hm_recruiter §2 |
| **Team Matching** | GenSWE 最后一步，HM 30–45 min | 团队需求、scope、工作方式、长期匹配 | headcount 真实风险（全过后被搁置的一手案例；另一例拿到带数字的 offer 后被推去换组再失联，HN 2026-07）；主动问 org 与 headcount | raw/bq_hm_recruiter §4 · discovery/TRIAGE #41 |

## Table E — 仅题名 / 未证实（不建题，留档）

OA：Drawing Edge · Horizontal Pod Autoscaler（pod count）· Efficient Deployments · Minimum Total Weight · Unequal Elements · Person and Cake · Simple Array Rotation Game · Grid Traversal（min jumps）· Good Subsequence I · Text Scoring · String Transformation · Non-Overlapping Intervals 变体 · Lexicographically Largest Array（MEX）· Minimize/Maximum Array Value · Largest Sub Grid · Same Bit Pair · Prime String / Work Schedule（2025 Infra 实习，403）· Solve Matrix Equations · Max Element Indexes After Rotations。
电面/前端：React Kanban（前端赛道）· GFE coding。
**剔除**：Grid Land / Kth Smallest Instructions（Lucid 2020 OA 误标）。

---

## Table F — GitHub 优先蒸馏补充（2026-09-13，来源与题面要点见 `raw/github_repos.md` §2–§3）

来源：TrueInterview 同步清单（经 GitHub `kevin-2023-code/Tech-Interview-Questions` 镜像，MED，题面付费、预览可见开头与分段提纲）+ JoeBao22/SDE-OA-2024（q20）。凡超出预览的部分在 `problem.md` 标 **(reconstructed)**。原 Table C 的 sd20 Dynamic Blacklist Filter 改归 od11（TrueInterview 归 LLD；1p3a 标题 + TrueInterview = 2 refs）。
LeetCode 原题（Calculate Amount Paid in Taxes、Merge k Sorted Lists、N-Queens 等 19 道）**不建 kit**，统一见 [`core/leetcode/companies/snowflake.md`](../../../core/leetcode/companies/snowflake.md)（链接 + 标签 + 频率分档）。

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---:|---|
| pc16 | Reverse Alphanumeric Segments（1p3a 标题 + TrueInterview） | PS | 2026-06 | 2 | MED |
| pc17 | Forest Parent Array Delete Node | PS | 2026-06 | 1 | MED |
| pc18 | Number Transformation Path（+2 / −2 / ⌊÷2⌋） | PS | 2026-06 | 1 | MED |
| pc19 | Rewrite Tree With Subtree Sums | PS | 2026-06 | 1 | MED |
| pc20 | Four-in-a-row `canPlayWin` + Design Connect Four | PS | 2026-06 | 1 | MED |
| pc21 | SnowCal / String-Command Calculator | PS | 2026-05 | 1 | MED |
| pc22 | Document Predicate Search Engine（3 Part） | PS | 2026-04 | 1 | MED |
| pc23 | Min Coins to Pay with Change Allowed | PS | 2026-02 | 1 | MED |
| pc24 | Service Failure Forensics（二分 → 级联 → 最长链） | PS | 2026-02 | 1 | MED |
| pc25 | Grep With Context Lines | PS | 2026-02 | 1 | MED |
| pc26 | Top K Hash Tags（去重用户数） | PS | 2026-02 | 1 | MED |
| pc27 | Recipe Sequence Matcher（+ O(1) 空间追问） | PS | 2026-01 | 1 | MED |
| pc28 | Preorder Traversal Without Invalid Nodes | PS | 2025-12 | 1 | MED |
| pc29 | Valid Tic-Tac-Toe State（N×N、K 连） | PS | 2025-11 | 1 | MED |
| od11 | Dynamic Blacklist Filter System（两条并发流） | PS/LLD | 2026-06 | 2 | MED |
| od12 | Top K Book Sales `bestSellers` | LLD | 2026-02 | 1 | MED |
| od13 | Serialize / Deserialize Dictionary Trie | PS | 2025-12 | 1 | MED |
| od14 | Durable KV Store Serialization（自定义编码 + 1 KB 分块） | LLD | 2025-11 | 1 | MED |
| od15 | JSON Parser（最小化 / INVALID） | LLD | — | 1 | MED |
| q20 | Sequential String（前缀凑排列） | OA | 2024 | 1 | MED |
| q21 | Maximum Profit Query Selection | OA | 2026-01 | 1 | MED |
| q22 | Dropped Requests（多窗口限流） | OA | 2025-11 | 1 | MED |
| q23 | Work Schedule（`?` 填充枚举） | OA | 2025-07 | 1 | MED |
| q24 | Maximum Throughput（二分答案） | OA | — | 1 | MED |
| q25 | Distance from Each 1 to the Nearest 2 | OA | — | 1 | MED |

**SQL 三题**（Webinar Popularity、Marketing Touch Streak、Project Duration & Budget per Employee）与**前端**一题（Robot Eats Candies）属数据 / 前端岗，SDE 不建，留档于此。

## 28 法则与建题顺序（`PARETO.md` 完整输出）

cut line 以内 33 行 = 建题库的第一批；按轮次分给三路：

- **OA / 电面 coding（`problems/`）**：q02 q03 q01 q04 pc03 pc02 pc04 q05 q06 q07 q08 q09 pc05 pc06 pc10 q10（16 题；pc09 直接复用 Stripe qA09，q06 的 LC 484 与 pc08 合一）
- **OOD（`loop/rounds/04_ood/`）**：od01 od02 od03 od04 od05 od09 od06 od08（8 题）
- **SD（`loop/rounds/05_system_design/`）**：sd01 sd02 sd03 sd04 sd06 sd07 sd05 sd11 sd08 sd09 sd10（11 题）
- **RBAC 题族 pc01** 是 #1，单独做成 4-part 电面题（`loop/rounds/03_phone_coding/pc01`），题面参考 Stripe 镜像里 RBAC 真题四阶段（Stripe HANDOFF §3 P1）。

第二批（cut line 外但有题面）：q11–q18、pc11–pc16、od07、sd12。Table E 不建。
