# Snowflake 招聘流程分轨道整理 + JD 技能频率分析

> 采集日期：2026-09-13。方法：WebSearch + WebFetch。JD 来源为 careers.snowflake.com 原始职位页
> （多数已下线，返回 "OH SNAP! THIS JOB HAS BEEN CLOSED" 或 HTTP 410，但内容仍可从 **builtin.com /
> zapply.jobs 等招聘聚合镜像**读到完整原文，这些镜像会保留 Snowflake 官方 JD 的逐字文本并标注下线时
> 间）；流程/timeline/pass-line/down-level 证据来自 Blind、1point3acres（经 Telegram 镜像
> `t.me/s/usinterview?q=snowflake`）、levels.fyi。与本仓库已有 `../../raw/process_research.md`
> （下称"P"）、`../../raw/company_research.md`（下称"C"）互补，重叠内容标注"复用 P/C + 原采集日期
> 2026-09-13"。置信度：**[高]**=一手/官方；**[中]**=聚合站转述但多源一致；**[低]**=单一聚合站转述。

---

## 1. GenSWE 官方流程事实（复用 P §1.1-1.2，不重复展开）

- GenSWE = General Software Engineering Program，官方定义"early career engineers"，地点 Menlo Park /
  Bellevue，流程"an initial conversation with a recruiter or hiring manager, technical interviews,
  panel interviews, and a team matching round"，滚动招聘全年开放。—— https://careers.snowflake.com/us/en/generalsoftwareengineeringprogram（复用 P，本文件 2026-09-13 重新抓取确认页面结构不变，额外确认了 FAQ 明确写出"team matching round"为流程第四步）**[高]**
- 官方 "Hiring Process" 4 阶段（Initial Screen 30min → Technical Interviews 60min/轮 → Panel Interviews 3-5 轮×60min → Decision，几天内 debrief，30 天无回音视为不匹配）。—— https://careers.snowflake.com/us/en/gethired（复用 P §1.2）**[高]**

---

## 2. 按赛道拆分：GenSWE 早期职业 vs 有经验 Backend

| 维度 | GenSWE 早期职业（IC1/IC2） | 有经验 Backend（IC3+/Senior/Staff） |
|---|---|---|
| Recruiter screen | 30 min（部分报告更短，~15 min） | 30 min，同款 |
| AI 筛选（Chakra） | 2026 年起明确出现，"General SWE"专属邀请（复用 P §2.2） | 未见一手报告，Blind 上 Senior/Staff 讨论帖未提及 Chakra |
| OA（HackerRank） | 部分候选人有，3 题/90-120 min；2026 全职一手帖多数**跳过 OA** 直接进电面（复用 P §3.1） | 未见相关报告，推测更少见 |
| 技术电面 | 常见两轮 back-to-back：1 coding + 1 system design，或 2 coding；每轮约 1h（复用 P §1.3） | 类似结构，但题目难度报告更高（"extremely hard LC + follow-up"，复用 P §3.2） |
| Onsite/Panel | 3-5 轮：coding（1-2 轮）+ resume/project 讨论 + system design + BQ/manager；一手案例显示 IC1 至少 3 轮全过 | 4-5 轮，含独立 **Expertise 轮（40 min 项目深挖）**（复用 bq_hm_recruiter.md §3）；Senior+ 可能多一轮 30 min **Tech Talk 演示**（官方原文，复用 P §1.2） |
| Team matching | GenSWE 官方流程最后一步，本文件 bq_hm_recruiter.md §4 证实**不是走过场**，可能因无 headcount 被搁置 | 未见"team matching"措辞用在有经验候选人身上，更可能直接对应具体 team 的 HM 面 |
| 定级基准 | 大概率 IC1，争取 IC2 需要电面+onsite 全 Hire（推断，复用 P §5） | IC3 起，存在因 headcount 或 behavioral 表现被 down-level 到 IC2 的案例（本文件 §4，复用 bq_hm_recruiter.md §5.2） |

**关键差异总结**：GenSWE 是"先固定的技术 loop，再谈 team matching"，有经验候选人更可能是"针对具体 team 的定向面试链路"，其中 Expertise 轮 40 min 深挖 + Tech Talk 是有经验候选人独有、早期职业候选人报告中强度明显更弱的环节。**[推断，基于 P + bq_hm_recruiter.md 综合]**

---

## 3. 按地点拆分：Menlo Park vs Bellevue

结合 JD 抓取结果（见 §6）与 `company_research.md` §1.3/§3.1 的团队地理分布：

| 地点 | 已确认在招/曾招的 Backend 相关团队 | 依据 |
|---|---|---|
| **Menlo Park** | Software Engineer - Backend（GenSWE，通用）、Software Engineer - Database Engineering、Software Engineer Backend - Apps & Collaboration、Software Engineer - Billing Platform、Senior Software Engineer - AI Platform for User Experiences | 本文件 §6 JD 抓取 |
| **Bellevue** | Software Engineer - Backend（GenSWE，通用）、Software Engineer - Database Engineering（与 Menlo Park/Berlin 共享招聘）、Backend Software Engineer, AI Platform for User Experiences、Software Engineer / Senior Software Engineer - Query Processing (SnowTrail)（部分与 San Mateo 共享） | 本文件 §6 JD 抓取；C §1.3 "Bellevue 办公室是西雅图地区工程中心" |
| **Berlin** | Database Engineering 团队分布地之一（招聘页面明示） | C §3.1 |

- **结论**：GenSWE 的 "Software Engineer - Backend" 岗位本身是 **Menlo Park / Bellevue 双地点同一条 JD**，说明 GenSWE 不按地点分派不同技术栈要求，地点差异主要影响的是**后续 team matching 匹配到哪个具体 org**（Bellevue 更偏 AI Platform for User Experiences / Query Processing，Menlo Park 覆盖面更广，含 Billing、Apps & Collaboration 等产品向后端团队）。**[推断，基于 JD 地点分布]**

---

## 4. 时间线 / Pass Line / Down-level（复用并补充 P + bq_hm_recruiter.md）

- 官方口径："up to two to four weeks"。—— https://careers.snowflake.com/us/en/gethired（复用 P §1.4）**[高]**
- 一手最快案例：内推 → HR call → 当天约面，仅 4 天（Telegram 29627，复用 P §1.4）**[高]**。
- 一手最慢/中断案例：IC1 候选人两轮电面 + 三轮 onsite 全过后，HM 环节卡住 10+ 天无回音，最终疑似"manager found someone better"（本文件 bq_hm_recruiter.md §5.1）**[高]**。
- **Pass line**：电面轮"doesn't signal anything"（不计入通过线），**onsite 每一轮都要 Hire**（复用 P §1.3，Blind ex-Google IC2 2025-10-04）**[高]**。
- **Down-level**：无 IC3 headcount → 建议接受"Sr IC2"；behavioral 轮表现不佳可以把已过技术轮的 Senior 降为 SDE2 级别；"Snowflake 不太相信空降 senior title"（本文件 bq_hm_recruiter.md §5.2）**[中，多为聚合摘要转述 Blind 讨论，非直接读到原贴逐字]**。

---

## 5. 早期职业薪酬（levels.fyi，2026-09-13 二次核对）

本文件对 `company_research.md` §5 的 levels.fyi 数字做了**同日二次抓取**，数值有小幅波动（levels.fyi 是实时更新的众包数据，两次抓取相差几小时属正常）：

| 级别 | company_research.md（2026-09-13 早些时候） | 本文件二次抓取（2026-09-13） |
|---|---|---|
| IC1 US 中位 TC | $232K | $230,350（约 $233K，来自另一检索口径 $233K-$952K 区间起点） |
| IC2 US 中位 TC | $348K | $334,266 |

来源：https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic1 ；
https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2 ；
https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2（另一检索口径给出 $276K–$395K+ 区间）；
https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic1（另一检索口径给出 $210K–$260K+ 区间）
（访问 2026-09-13）**[高，但数字本身随时间浮动，取区间而非单点更可靠：IC1 约 $210K-$260K 中位数附近，IC2 约 $276K-$395K 中位数附近]**

- Backend Software Engineer 专属 title 页：$223K–$712K+ 区间（跨所有 level）。—— https://www.levels.fyi/companies/snowflake/salaries/software-engineer/title/backend-software-engineer（访问 2026-09-13）**[高]**
- 其余细分（Bay Area/Seattle 分地区中位数、Blind 一手 offer）见 `company_research.md` §5，不重复。

---

## 6. JD 技能频率分析（careers.snowflake.com，6 份职位原文）

### 6.1 抓取方法与来源说明

careers.snowflake.com 的职位 ID 轮换很快，直接访问搜索命中的 URL 大多数返回 "OH SNAP! THIS JOB HAS
BEEN CLOSED" 或 HTTP 410；**builtin.com 与 zapply.jobs 会镜像 Snowflake 官方发布的 JD 原文**（包括已下
线的），并标注下线/更新时间戳，本节 6 份 JD 均以这些镜像的逐字引用为准，链接见每行末尾。唯一一份**当前
仍在线**的是 #1（GenSWE Software Engineer - Backend，zapply.jobs 镜像标注 "Posted: August 21, 2026"，
且 careers.snowflake.com 的 GenSWE 官方页面在 2026-09-13 抓取时仍在链接同一职位 ID）。

### 6.2 六份 JD 摘要

| # | 职位 | 地点 | 状态/日期 | 语言要求 | 核心领域 |
|---|---|---|---|---|---|
| 1 | **Software Engineer - Backend**（GenSWE 通用岗，本仓库目标岗位本身） | Menlo Park, CA / Bellevue, WA | **在线**，2026-08-21 发布 | Java, Python, C++, 或 SQL（任一即可，"fluency in one or more of"） | 2-7 年大规模生产系统经验；分布式平台；端到端客户产品；偏好：数据库内部、数据治理、支付系统 |
| 2 | Software Engineer - Database Engineering | Menlo Park / Bellevue / Berlin | 已下线，2026-05-22 移除 | Java **或** C++ | PB 级云数据库；查询优化；分布式数据处理；多线程/并发；测试/调试/文档；提到 FoundationDB/RocksDB/InnoDB/BerkeleyDB/MySQL/PostgreSQL 内部/Hadoop/Spark/HDFS/Cassandra/列式数据库 |
| 3 | Senior Software Engineer - Query Processing (SnowTrail) | Bellevue, WA / San Mateo, CA | 已下线，2025-10-13 移除 | 未明确指名语言，聚焦 SQL/数据库技术 | 查询优化、查询执行、编译器设计与实现；MySQL/PostgreSQL 内部；偏好 Release Validation Pipelines、生产环境测试基础设施 |
| 4 | Software Engineer Backend - Apps & Collaboration | Menlo Park, CA | 已下线，2025-05-08 移除 | Java **且** SQL（"fluency in Java and SQL"） | 2-5 年后端大规模数据处理系统；数据库与分布式系统；数据共享/协作功能 |
| 5 | Software Engineer - SnowTrail | Bellevue, WA（可选 San Mateo, CA） | 已下线，2026-01-06 移除 | 未明确指名语言 | CS 基础（数据结构/算法/分布式系统）；团队协作与 mentor；偏好 SQL/数据库技术、Release Validation Pipelines、生产测试基础设施 |
| 6 | Software Engineer - Billing Platform | Menlo Park, CA | 已下线，2025-06-03 移除 | Java **且** SQL | 2-4 年经验；数据摄取与建模；计费系统；实时用量计量（real-time usage metering） |

来源逐条：
1. https://zapply.jobs/jobs/c2382f97-dcee-4d0e-85e7-eb7e8b27562c/ （镜像，访问 2026-09-13）+ https://builtin.com/job/software-engineer-backend/4472801 （同一职位的另一镜像，标"Reposted One Month Ago"）+ 官方在招链接 https://careers.snowflake.com/us/en/job/SNCOUSDD524B932E4E4E3B84B44684A46E9148EXTERNALENUS3EB872AF0AB149868F72E7321FCD1538/Software-Engineer-Backend
2. https://builtin.com/job/software-engineer-database-engineering/4472390 （访问 2026-09-13）
3. https://builtin.com/job/senior-software-engineer-query-processing-snowtrail/4471461 （访问 2026-09-13）
4. https://builtin.com/job/software-engineer-backend-apps-collaboration/4588620 （访问 2026-09-13）
5. https://builtin.com/job/software-engineer-snowtrail/7767539 （访问 2026-09-13）
6. https://builtin.com/job/software-engineer-billing-platform/4472400 （访问 2026-09-13）

**[高，逐字引用均取自 builtin/zapply 镜像的 quoted requirement 文本，但需注意 #2-6 均为历史快照（已下线），不代表当前措辞，仅 #1 确认当前在招]**

### 6.3 技能出现频率表（分母 = 6 份 JD）

| 技能/关键词 | 出现次数 | 出现在 |
|---|---|---|
| SQL | 5/6 | #1 #3 #4 #5(偏好) #6 |
| 分布式系统（distributed systems） | 5/6 | #1(distributed platforms) #2 #3 #4 #5 |
| Java | 4/6 | #1 #2(或C++) #4 #6 |
| 数据库内部/技术（database internals / technologies） | 5/6 | #1(偏好) #2 #3 #5(偏好) #6(偏好) |
| 算法与数据结构 | 5/6 | #1 #2 #3 #4 #5 |
| 大规模/生产系统经验（large-scale, in production） | 4/6 | #1 #2(PB级) #4 #6(隐含) |
| C++ | 2/6 | #1 #2(或Java) |
| Python | 1/6 | #1 |
| 并发/多线程（concurrency, multi-threading） | 1/6 明确写出 | #2（"Systems programming skills including multi-threading, concurrency"） |
| 测试/调试/文档 | 3/6 | #2(核心) #3(偏好，Release Validation) #5(偏好，Test infra) |
| Cloud / Data Cloud 平台 | 6/6（均在职责描述中提及 "Data Cloud" 或云平台） | 全部 |
| 查询优化/执行（query optimization/execution） | 2/6 明确 | #2 #3 |
| 计费/计量（billing/metering） | 1/6 | #6 |
| 数据治理（data governance） | 1/6（偏好） | #1 |
| 支付系统（payment systems） | 1/6（偏好） | #1 |
| 团队协作/mentor 明确写出 | 2/6 | #3 #5 |
| Linux 环境 | 1/6 | #2 |

**解读**：
- **SQL + 分布式系统 + 数据库内部 + 算法数据结构**是四条几乎必考的通用线（5/6 出现率），与本文件 system_design.md 里 KV store/Quota/Cron Scheduler/SQL Notebook 等 infra 题族的选材逻辑完全对应。
- **Java 明显是 Snowflake 后端的默认语言**（4/6 直接点名，另 1/6 是 Java-or-C++ 二选一），Python/C++ 只在 GenSWE 通用岗（#1）里作为"任选其一"的选项出现，说明**如果目标是 Database Engineering / Billing / Apps 这类具体团队，Java 权重高于 Python**；GenSWE 通用岗本身对语言最宽容。
- **并发/多线程只在 Database Engineering 岗明确写出**，但结合 C §3.1 "C++ 写 XP 执行引擎、Java 写 GS 控制面"的说法，并发/GC 停顿相关知识对 Database Engineering / Query Processing 方向的追问概率应高于通用 Backend GenSWE 岗。
- **计费/计量只在 Billing Platform 一个团队专属岗位出现**，与 system_design.md §1.11 的结论一致：不应作为通用必考点准备，但若 team matching 分到 Billing 相关团队，需要单独补课。

---

## 7. GenSWE 项目页面事实补充（本文件新增，超出 P 已记录范围）

- FAQ 明确写出面试流程 4 步（"an initial conversation with a recruiter or hiring manager, technical
  interviews, panel interviews, and a **team matching round**"），并提供"面试准备资源，包括高级工程师
  谈 coding 面试预期的视频"。—— https://careers.snowflake.com/us/en/generalsoftwareengineeringprogram（访问 2026-09-13）**[高]**
- 页面当前仅列出**一个**在招职位入口："Software Engineer - Backend"（Menlo Park / Bellevue 双地点同一
  条 JD，见 §6.2 #1），说明 GenSWE 目前对外只开放这一个通用后端职位漏斗，其余方向（前端/全栈等）走各自
  独立 JD，不在 GenSWE 品牌下。—— 同上（访问 2026-09-13）**[高]**
- 申请方式为"滚动招聘，全年开放"（复用 P §1.1）。**[高，复用 P]**

---

## 8. Contradictions / unknowns（本文件新增）

1. **levels.fyi 数字的时间敏感性**：同一天两次抓取（本文件 vs `company_research.md`）IC1/IC2 中位数已
   有几千到一万美元级别的浮动，说明该数据源是准实时众包统计，引用时应给区间而非单点数字。
2. **builtin/zapply 镜像的 JD 是否与当前 careers.snowflake.com 原文完全一致**：镜像是 Snowflake 官方发
   布时的快照，若 Snowflake 后续修改过同一职位描述再重新发布，镜像可能落后于最新版本；本文件 #1 已用
   zapply（2026-08-21）与 builtin（"Reposted One Month Ago"）两个镜像互相核对，文本一致，可信度较高；
   #2-6 均为已下线职位，只能代表该职位存在过的某一版本文本。
3. **Query Processing (SnowTrail) 团队的语言要求未明确写出**（#3 #5 两份 JD 都没有像 #1/#2/#4/#6 那样
   点名 Java/C++），只能从"MySQL/PostgreSQL internals、查询优化、编译器设计"反推该团队更偏 C++/系统语
   言，未获 JD 文本直接证实。
4. **有经验 Backend 赛道是否也叫"GenSWE"**：GenSWE 官方定义明确是"early career"，本文件未找到证据说明
   有经验候选人会被计入 GenSWE 项目；§2 表格中"有经验 Backend"栏目的流程差异是从 Blind/1p3a 案例反推，
   并非官方文档区分的两条命名赛道。
