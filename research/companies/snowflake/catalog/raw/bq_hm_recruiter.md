# Snowflake 招聘/HR 筛选、HM、行为面试、Expertise 轮、Team Matching 原始资料汇编

> 采集日期：2026-09-13。方法：WebSearch + WebFetch。来源覆盖 Blind（浏览器 UA 直连）、
> 1point3acres（正文 403，经 Telegram 镜像 `t.me/s/usinterview?q=snowflake` 与其自带搜索摘要读到）、
> careers.snowflake.com 官方页面、Aced(Exponent)/PracHub/spacecomplexity 等聚合站（不采信
> lodely/vervecopilot）。与 `../../raw/process_research.md`（下称"P"）§2 §4 互补，P 已有的一手 Chakra
> AI 筛选报告、8 条官方价值观、部分 BQ 追问方式本文件**复用**并标注"复用 P + 原采集日期 2026-09-13"。
> 置信度：**[高]** = 一手候选人叙述；**[中]** = 聚合站转述但多源一致；**[低]** = 单一聚合站/疑似 AI 生成。

---

## 1. 招聘方/HR 筛选轮（Recruiter Screen）

### 1.1 格式与逻辑性问题

- 标准时长 **30 分钟**，官方原文："a member of our recruiting team and/or the hiring manager will schedule a call to get to know you and your technical skill set"。—— https://careers.snowflake.com/us/en/gethired（复用 P §1.2，原采集 2026-09-13）**[高]**
- 聚合站对内容的描述："The recruiter screen is a 30-minute conversation covering your background, technical interests, and why you want to join Snowflake. Expect high-level questions about your experience rather than anything technical."—— WebSearch 综合（Aced/Exponent 等，访问 2026-09-13）**[中]**
- 早期职业一手：HR call 问"infra 经验、平台项目、方向偏好"，Infra 岗一例报告"不到 15 分钟"就结束。—— t.me/s/usinterview/29383（复用 P §1.3）**[高]**
- 新增一手（HR 筛选，Infrastructure 岗）：Telegram 镜像命中一条 2026 年"HR Screening (Infrastructure Role)"报告，内容围绕候选人的 infra 经验展开讨论。—— https://www.1point3acres.com/bbs/thread-1186534-1-1.html，经 t.me/s/usinterview 搜索命中（访问 2026-09-13，正文 403，仅摘要）**[高，细节有限]**

### 1.2 "Why Snowflake"

- 聚合站统一建议："prepare thoughtful answers that demonstrate genuine interest in Snowflake as a data cloud platform company"——即不能只说"大厂/薪资好"，需要能具体讲出对 Snowflake 产品/技术方向的理解。—— WebSearch 综合（访问 2026-09-13）**[中]**
- 结合本仓库 `company_research.md` §6 已经准备好的"候选人 Braintree Snowglobe → Snowflake 内部系统"桥梁话术，"why Snowflake" 应该具体化到"我是 Snowflake 最重度的一类用户，踩过 Streams/Tasks 的坑"，而不是背模板。**[推断，复用 company_research.md]**

### 1.3 薪资/Level 处理

- 聚合站明确建议："It's really important, at this stage, not to reveal your salary expectations, your salary history, or where you are in the process with other companies. The recruiter may pressure you on this, but you should avoid naming a number first."—— WebSearch 综合（访问 2026-09-13）**[中，通用求职建议，非 Snowflake 独有，但反复被套用到 Snowflake 语境]**
- Level 处理：见本文件 §5 Down-level 部分；recruiter screen 阶段通常还不会明确定级，定级更多在 onsite 后由 HM/招聘委员会决定（推断，无一手数据反驳）。

---

## 2. Hiring-Manager / 行为面试问题

### 2.1 官方角度：behavioral 不是永远独立一轮

- 官方 panel 组成明确列出 "behavioral" 与 "collaboration" 两轮。—— https://careers.snowflake.com/us/en/gethired（复用 P §1.2）**[高]**
- 但候选人体验的早期职业（IC1/IC2）loop 里，behavioral 更多是**嵌在技术轮开头的 15-20 min 项目讨论**，而非独立轮（复用 P §1.5 结论）。**[高，复用 P]**
- 新增一手佐证：Telegram 镜像 "Snowflake Store Interview"（两轮 coding）报告——"第一轮完成用了 30 分钟；第二轮以 15 分钟的行为面试问题开场（关于近期项目和技术挑战），随后才是 coding"。—— https://www.1point3acres.com/bbs/thread-1179343-1-1.html，经 t.me/s/usinterview 搜索命中（访问 2026-09-13，正文 403，仅摘要）**[高，与 P §4.2 的 15-20 min 项目讨论模式再次吻合]**
- 新增一手：IC2 mid-level onsite 报告结构为**一轮 coding + 一轮 behavioral（独立成轮）+ 一轮 system design**——说明至少部分 org（该报告为 Canada、mid-level）在 onsite 阶段**确实把 behavioral 设成独立的一轮**，与"嵌入技术轮"的说法并存，取决于 org/level。—— https://www.1point3acres.com/bbs/thread-1180916-1-1.html，经 t.me/s/usinterview 搜索命中（访问 2026-09-13）**[高]**

### 2.2 典型行为面试问题（多源一致，非一手逐字但被多个独立聚合站反复引用相同措辞）

- "Tell me about a time you made a mistake."
- "Tell me about a time when you took ownership over a project, and why."
- "Describe a time when you had to work effectively with another team that you had never worked with before."
- "Tell me about a time when you wouldn't have successfully completed a project without teamwork."
  —— University of Miami 职业中心镜像 Exponent 博客（2026-05-14）https://customcareer.miami.edu/blog/2026/05/14/get-a-job-at-snowflake-interview-process-and-top-questions/（复用 P §4.3）**[中]**
- 追加检索命中的同源问题（其他聚合站转述，未见新增独立一手来源）：
  - "Tell me about a time you had a conflict with a coworker/stakeholder and how you resolved it."
  - "Tell me about a time you had to push back on a decision you disagreed with." （对应 Integrity Always 的 "disagree and commit"）
  - "Tell me about a time you had to prioritize between competing deadlines."
  - "Tell me about a time you put the customer first when it was inconvenient."
  - "Tell me about a time you raised the bar / took ownership outside your scope."
  —— Aced/Exponent 指南（2026-08 更新，复用 P §4.3）**[中]**

### 2.3 与 8 条官方价值观的映射

Snowflake 官方 8 条价值观逐字见 `company_research.md` §4（Global Code of Conduct and Ethics，2026-02-23 版）。行为面试问题 → 价值观映射（综合 P §4.3 与本文件新检索）：

| 价值观 | 典型问题 / 追问角度 | 来源 |
|---|---|---|
| **Put Customers First** | "put the customer first when it was inconvenient"；候选人的支付/商户场景故事可直接对应 | spacecomplexity（复用 P）**[中]** |
| **Integrity Always** | 冲突/分歧处理、"speak up… commit fully when decisions are made"（disagree-and-commit）；金融数据场景下的"说真话" | 官方价值观原文 + spacecomplexity **[高/中]** |
| **Think Big** | "扩大 scope 的证据"；候选人主动拓展项目边界的故事 | spacecomplexity（复用 P）**[中]** |
| **Be Excellent** | 未见聚合站给出专属问题模板，推断对应"你如何保证代码/设计质量"类追问 | **[推断]** |
| **Get It Done** | "砍什么、保什么、slip 前先沟通"；deadline 取舍 | spacecomplexity（复用 P）**[中]** |
| **Own It** | "未被指派就承担责任"；"承认错误并说出具体改了什么流程"；"took ownership over a project" | spacecomplexity + University of Miami 镜像（复用 P）**[中]** |
| **Make Each Other the Best** | disagree-and-commit、主动帮同事、接受批评；team conflict 类问题 | spacecomplexity（复用 P）**[中]** |
| **Embrace Each Other's Differences** | 未见聚合站给出专属问题模板 | **[推断]** |

### 2.4 面试官在场记录方式

- 聚合站描述（非一手但具体到行为细节）："someone asks you things like 'tell me about a time you took ownership' while writing notes and deciding whether you're the kind of person they want on their team"，暗示行为面试官会**逐条记笔记打分**，而非闲聊。—— WebSearch 综合（访问 2026-09-13）**[低-中，聚合站描述性语言，非一手确认]**

---

## 3. "Expertise" 轮（项目深挖，约 40 分钟）

### 3.1 一手描述（复用 P + 本文件新增）

- Blind 2024-06（Asana 用户，IC3）："They asked me to pick a project from past/recent job and deep dive into it for good 40 mins"，追问"why/how I made the decisions ... technical architecture, approach and external libraries"，并延伸到 availability / fault tolerance。—— https://www.teamblind.com/post/snowflake-expertise-interview-xcavd10l（复用 P §1.5）**[高]**
- **新增一手**（Blind 2024-02-04，Senior SWE，L64，TC $270K）候选人发帖问"Expertise 轮会考什么、难度如何"；评论区回应：
  - "This round proves your depth of knowledge, aka expertise, in your domain"——强调考察系统设计决策背后的理解深度。
  - Amazon 员工评论："a project deep dive with some system design elements"——即 expertise 轮不是纯讲故事，会掺杂系统设计追问。
  - 建议："Contact your recruiter—they're your best source as they work with that specific interview committee"；"be prepared to discuss the 'why' behind every system design decision"；候选人需要"demonstrate senior-level capability by articulating tradeoffs in your past projects"。
  —— https://www.teamblind.com/post/expertise-round-in-snowflake-3tbrdamq（2024-02-04）**[高]**

### 3.2 什么会导致 Expertise 轮失败

综合两条一手帖的追问方向（架构选型理由、备选方案、可用性/容错、trade-off 深度），**大概率的失败模式**是：
1. 只能复述"做了什么"而讲不出"为什么这么做、当时还有什么别的选项"；
2. 遇到"这个设计现在看有什么问题/你会怎么重做"类追问时给不出具体答案；
3. 项目故事停留在功能层面，没有触及可用性、容错、扩展性等系统属性。
（**[推断]**，基于两条一手帖的追问模式反推，未见候选人明确自述"因为 XX 挂了 expertise 轮"的第一手失败复盘）

### 3.3 早期职业（IC1/IC2）版本的 Expertise / Resume 轮

- P §1.3 记录 onsite 结构里的"1 resume-based"轮（1p3a thread-1113703，搜索摘要）**[medium，复用 P]**；早期职业候选人报告"onsite 第一轮'extensive project discussion (~20 min)'再做 coding"（t.me/s/usinterview/28738，复用 P §1.5）**[高，复用 P]**。
- 结论：IC1/IC2 的"expertise"强度弱于 IC3 报告的独立 40 min 深挖轮，更多是嵌在 coding 轮开头的 15-20 min 项目讨论；但 onsite 阶段仍可能有一轮独立的 resume-based 面试。

---

## 4. Team Matching 轮（GenSWE 专属，onsite/技术轮之后的最后一步）

### 4.1 官方描述

- GenSWE 官方流程原文："an initial conversation with a recruiter or hiring manager, technical interviews, panel interviews, and a **team matching round**."；"candidates are paired with teams based on experience, skill, and preference"。—— https://careers.snowflake.com/us/en/generalsoftwareengineeringprogram（复用 P §1.1，原采集 2026-09-13）**[高]**

### 4.2 候选人报告的实际情况

- 聚合站转述："A team-fit or hiring-manager conversation often comes late in the process (commonly 30-45 minutes) and judges your match with a specific team's needs, scope, working style, and longer-term fit."—— WebSearch 综合（访问 2026-09-13）**[中，无具体来源站点名，综合摘要]**
- Blind 提及"实习 team matching"的负面情绪帖："snowflake swe intern fall 2025 team matching losing hope"——说明团队匹配阶段可能存在**长时间等待、候选人被动等团队挑选**的体验，即使技术轮已通过。—— https://www.teamblind.com/post/snowflake-swe-intern-fall-2025-team-matching-losing-hope-bkgoqjdw（标题级，访问 2026-09-13，正文未读）**[中，仅标题确认存在该焦虑，实习场景，全职 GenSWE 是否相同流程未证实]**
- **一手：全职 IC1（Product Experience org）候选人"通过 HM 对话"后被"新的 HM 重新面谈"，因为原始 headcount 已被占用**——说明 team matching 不是走过场，可能出现"技术轮全过、但没有匹配的团队/HM 而被搁置甚至石沉大海"的情况：候选人在 HM 对话后等待 10+ 天无回音，Snowflake 员工在 Blind 上回复"recruiting resources are spread thin"，另一条冷评论"Manager found someone better"。—— https://www.teamblind.com/post/passed-all-rounds-at-snowflake-then-silence-z4cg3oq0（2025-06-04 附近）**[高]**

### 4.3 对候选人的实操含义

- Team matching **不是形式流程**，是真实的"团队要不要你"环节，即便前面所有技术轮都拿到 Hire，也可能因为**没有合适 team/HM 而被无限期搁置**。建议：面试过程中主动了解自己在匹配哪些 org（如 Product Experience / Database Engineering / Query Processing / Cloud Services），并在合适时机向 recruiter 询问 headcount 情况。**[推断，基于 §4.2 一手案例]**

---

## 5. 拒信 / Down-level 一手引述

### 5.1 拒信（无反馈）

- Blind 2025-03-05：两轮 coding（LC mediums + 1 OOD）后**无 onsite 直接拒，无反馈**。—— https://www.teamblind.com/post/snowflake-interview-rejected-for-no-reason-gsuxeszj（复用 P §1.3）**[高]**
- Blind（IC1，Product Experience org，2025-06-04 附近）：两轮技术电面 + 三轮 onsite 全部通过后，因原岗位已被填补，转由另一 HM 面谈；面谈后**10 天以上无回音**，recruiter 未回复候选人的跟进邮件；Snowflake 员工在评论区坦白"招聘资源分散"，另一条评论直接说"Manager found someone better"。—— https://www.teamblind.com/post/passed-all-rounds-at-snowflake-then-silence-z4cg3oq0（2025-06-04 附近）**[高，全套技术轮通过≠拿到 offer 的典型案例]**

### 5.2 Down-level（降级 offer）

- 综合 Blind 讨论（"Snowflake downlevel"帖等）：Snowflake 可能因为**当前 title、面试表现、目标 level 无 headcount**而降级；候选人观察"Snowflake 不太相信空降 senior title——如果你现在的 title 不是 senior，他们不会给你 senior"。—— https://www.teamblind.com/post/snowflake-downlevel-txc5g5ub（访问 2026-09-13，摘要）**[中，聚合摘要转述 Blind 讨论内容，未直接读到原贴逐字]**
- 具体案例：一位 IC3 候选人拿到"positive feedback"，但因**该 hiring team 没有 IC3 headcount**，recruiter 提议降为 IC2，并说"trend toward hiring more 'Sr IC2' than IC3 at the moment"；建议是**不要接受降级 offer**，因为会影响未来 title 认定且无晋升保证。—— WebSearch 摘要综合多个 Blind 帖（访问 2026-09-13）**[中]**
- 另一案例：一位有 5 年经验、面 senior DS 的候选人被降到 **IC1**；还有一位因"behavioral 轮表现不佳"（尽管技术轮通过）被从 Senior 降为 **SDE 2**。—— WebSearch 摘要（访问 2026-09-13）**[中，非 backend SWE 案例，但说明 behavioral 轮可以单独否决定级]**
- **对本候选人（1.5 年经验，目标 IC1，争取 IC2）的含义**：behavioral/expertise 轮的表现可能独立影响定级，不只是"技术过了就行"；如果技术轮都是 Hire 但 behavioral 偏弱，存在被降级到 IC1 而非 IC2 的风险。**[推断，基于 §5.2 案例外推]**

---

## 6. Chakra AI 筛选（复用 P §2，不重复展开）

Chakra AI 语音筛选的完整一手报告、环境要求、官方说明已在 `process_research.md` §2 详细记录（3 条 1point3acres 一手报告 + Blind 员工确认帖 + PracHub/Aced 转述），本文件不重复摘录，仅在此提示：**AI 筛选环节的问题结构（背景/项目/协作决策/提问）与本文件 §2 的 HM behavioral 问题高度同构**，可以用同一套 STAR 故事应对两个环节。**[高，复用 P]**

---

## 7. Contradictions / unknowns（本文件新增）

1. **Behavioral 是否独立成轮**：早期职业候选人报告里既有"嵌在技术轮开头 15-20 min"（多条一手），也有"onsite 里独立一轮 behavioral"（thread-1180916，IC2，Canada）——取决于 org/level/面试委员会安排，无法给出统一规则。
2. **Team Matching 的具体形式**（一对一 HM 面谈 vs 多个 HM 轮流"挑人" vs 纯谈话不筛选）未见任何一手报告给出流程细节，只能确认它是**真实的筛选点而非形式流程**（见 §4.2 一手案例）。
3. **Expertise 轮在 IC1/IC2 是否以独立 40 min 轮存在**：IC3+ 报告明确是独立 40 min 轮；IC1/IC2 报告显示强度更弱（嵌入技术轮或"1 resume-based 轮"），具体分界线未知。
4. **Down-level 的触发条件**：headcount 不足、behavioral 表现、title 认定三种原因都有案例支持，无法确定哪个是主因，也未找到 backend/GenSWE 专属的 down-level 一手案例（现有案例多为 DS/Senior 岗位）。
5. **thread-1179343、thread-1186534、thread-1180916、thread-1186357 均为经 Telegram 镜像间接读到摘要**，1point3acres 原帖正文本身仍 403，无法核实更多细节（如具体日期、完整追问列表）。
