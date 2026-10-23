# 流程与轮次（Abnormal AI / Abnormal Security 面经聚合）

访问日期均为 2026-10-06。可信度：[高] 一手/官方 · [中] 一手但只有摘要 / 带日期的聚合 · [低] SEO/无日期。
**阅读提示**：公司 2025 年中后品牌从 Abnormal Security 改称 Abnormal AI；各站混用。下文先给新流程（2025 年中以后，AI-assisted），再给旧流程，再给逐条来源。所有"轮次序号"是不同候选人的描述，**角色/国家不同（美国 / 印度 / 新加坡 / 伦敦），不保证与 Chi 的 SWE II – Insider Risk 完全一致**。

## 0. 综述（我的归纳，非原文）

1. 2026 年的报道几乎一致：**不是 LeetCode**；允许/要求用 AI（Claude / Cursor）；任务落在**已有代码库**上（读懂 → 加 feature → 加测试）。[中]
2. 后续轮次反复出现的组合：**incident（AWS 环境排障）+ system design（给现有系统做 scale）**、**code review（给小仓库按 P0/P1 排序）+ 系统扩展**、**manager / behavioral**、**project deep dive**。[中]
3. 结局是"是否有 judgment"：LeetCode Discuss #8496901 作者通过所有正式轮、因 additional deep dive 被判 "lacked sufficient judgment in a few areas"。[中]（呼应官方 Judgment 评分维度）
4. 已报道的 Screening 代码库领域 = **security events 处理管线**（ingestion → ranking → 规则判定 threat level → alert → API → DB）。Insider Risk 岗位的练习库很可能同域，但**只有一人（印度，2026-06）明确报道**。[中/低]

## 1. 新流程（2025 年中以后，AI-assisted）

### 1.1 Technical Screening（AI-assisted live coding in existing codebase）

| # | 日期 | 来源 | 角色/地点 | 内容原话 | 可信度 |
|---|---|---|---|---|---|
| a | 2026-06-15 | LeetCode Discuss #8335187 https://leetcode.com/discuss/post/8335187 （GraphQL 取得） | SDE，印度（推测） | "They ask you to read a codebase which I skimmed through in like 10 mins and claude (allowed)." / 开始后面试官说 "sorry I gave the wrong question and it was still a vague question." / "This was a HLD cum LLD plus coding round." | [中] 一手，带负面情绪 |
| b | 2026-06-29 | 1p3a thread 1181621（Telegram 镜像 https://t.me/usinterview/28974 摘要） | Abnormal AI 技术电面 | "Screening Round面试要求基于一个现有的处理 Security Events 的 codebase 进行代码阅读与功能实现。该系统涵盖了数据 Collection/Ingestion、Ranking、基于规则的 Threa ..."（摘要被截断；全文 1p3a 直连 403） | [中] 摘要 |
| c | Jun 2026 报告 / 2026-08-25 发布 | PracHub https://prachub.com/interview-experiences/abnormal-ai-software-engineer-interview-experience-screening-round-built-on-a-live-security-events-codebase | Software Engineer, Technical Screen | 标题 "Screening Round Built on a Live Security Events Codebase"；正文付费墙；关联练习题标题 "Extensible Security-Event Pipeline: Rule Suppression and Plugin-Based Enrichment"（分类 Software Engineering Fundamentals） | [中] 仅标题 |
| d | 2026-07-10 | LeetCode Discuss #8387564 https://leetcode.com/discuss/post/8387564 | SDE II | "Round 1 – AI-Assisted Machine Coding … the interview explicitly allowed the use of AI tools during development. The focus wasn't just on writing working code—it was equally about explaining the implementation, code structure, design decisions, and trade-offs." 面试官 "spent a significant amount of time discussing the architecture, maintainability, and why I had chosen a particular approach."（通过此轮） | [中] |
| e | 2026-09-02 | LeetCode Discuss #8496901 https://leetcode.com/discuss/post/8496901 | Software Engineer II | "I was given an **existing codebase** and was expected to: 1. Go through the codebase and explain how it worked. 2. Understand the existing architecture/flow. 3. Implement an additional feature based on a problem statement provided by the interviewer. 4. Discuss possible extensions and modifications." / "The extensions were mostly discussion-based; I wasn't required to implement every extension." / Tip: "Don't prepare only for DSA." | [中] |
| f | Reported Jul 2026（发布 2026-09-04） | PracHub https://prachub.com/interview-experiences/abnormal-security-software-engineer-interview-ai-assisted-work-in-a-large-codebase-a2857641b5 | Software Engineer，纽约 | "About a week later, I had an AI-assisted technical screen. I received a large codebase and a feature requirement, and was expected to understand the existing structure with AI help, implement the feature with AI assistance, and add tests." | [中]（PracHub 为"curated and edited"） |
| g | Reported Jul 2026 | PracHub https://prachub.com/interview-experiences/abnormal-ai-software-engineer-interview-feature-implementation-in-an-existing-codebase-874b1387d9 | Software Engineer，Bengaluru | "I was placed in a fairly large existing codebase and first had to make sense of it with AI tools … The challenging part was how much depended on the AI interpreting both the codebase and my intent." Feedback: neutral, no offer | [中] |
| h | 2026-06-03（Interview May 2026） | Glassdoor Senior SWE https://api.glassdoor.com/Interview/Abnormal-AI-Senior-Software-Engineer-Interview-Questions-EI_IE3146005.0,11_KO12,36.htm | Senior SWE | "Recruiter screen followed by manager screen, then a coding exercise with AI assistant, then a take-home code review." | [中] |

**要点（a 的细节，对 Chi 最重要）**：feature 故意模糊；面试官甚至先给错题再改题；a 的候选人 20 分钟没推进、改用 Claude 全写——结果自评 "I'll mostly get a No"。说明**"先把含糊的需求问清、陈述假设、拆里程碑"比"让 AI 写完"更被看重**，但这是候选人自评推断，非面试官口径。

### 1.2 Hiring Manager（HM）

- PracHub (f)："After a recruiter call, I met the hiring manager. They explained the company and likely day-to-day work, then asked about my background, why I was changing roles, and how I used AI in everyday work." [中]
- Glassdoor Senior SWE（Jul 10, 2026，Bengaluru）："the first one was the HM round, where they described what the company does and how the day-to-day work for me will look like. Then on my introduction part, they asked how I have used AI in my day-to-day work and why I am switching." Q："How did I use AI for my personal as well as professional work to better myself?" [中]
- Glassdoor Senior SWE（Jun 3, 2026，Interview May 2026，**负面**）："The manager is bragging about how he wants 10x results from his team with the help of AI. He questioned my experience … Even asked me how many lines of code on a service I built." [中，单一负面来源；对 Chi 的启示：HM 可能压 scope 与 AI 杠杆，但 Chi 已过 HM]
- Glassdoor SWE（Feb 23, 2026，SF，referral，Accepted）："the hiring manager put emphasis on the ownership mentality." Q："Tell me about the most challenging project" [中]

### 1.3 Incident + System Design

- #8496901（2026-09-02）：Round 3 "Incident Reporting + System Design"。Incident："I was given access to an AWS environment and had to investigate an incident. The goal was to figure out: What was going wrong / How I would identify the root cause / What signals/logs/monitoring tools I would look at / What the immediate mitigation should be / What long-term fixes I would recommend." System design："I was given an **existing system** and asked how I would scale it … Scaling reads / Scaling writes / Identifying bottlenecks." [中]
- #8387564（2026-07-10）："Round 2 – Incident Management + System Design … started with a production incident that I had to investigate and resolve. After that, we had an in-depth system design discussion covering scalability, reliability, bottlenecks, and architectural trade-offs." 该候选人次日被拒。[中]
- PracHub 'AI agents used throughout a real-work loop'（Reported Jul 2026）："The later loop included a system-design and incident-management-style conversation plus a PR or code-review discussion where I could use AI agents throughout." [中]
- Glassdoor SWE（Apr 16, 2026，Accepted，Feb 2026 面）："Take-home assignment screener. Four rounds: - Assignment review & iteration - System design & Incident handling - Code review & fix implementation with AI - Engineering manager interview. Overall strong focus on AI utilisation. No leetcode, more grounded in real world skills." [中]

### 1.4 Code Review

- #8496901 Round 4 "Code Review + System Extensions"："I was given a small repository and asked to perform a code review … Identify issues / Prioritize them (P0/P1/etc.) / Explain why certain issues were more important / Suggest concrete improvements. The second part involved extending the system and discussing how it would behave at larger scale … Concurrency / Parallelism / Worker scaling / Message queue scaling / Throughput / Bottlenecks / Failure scenarios." / "going beyond 'add more workers' or 'use a queue.'" [中]
- 旧流程（2025-10）1p3a 第三轮同形态："code review + system design这轮面试前有一个link给你预先code review,面试分两部分,开始就讨论一下你的comments,大概二十分钟换成system design"（见 §2）。**新流程里 code review 是否预先发链接**：Glassdoor（h）称 "take-home code review"，与 1p3a 2025-10 "面试前有一个 link 预先 code review" 一致；#8496901 称"given a small repository"（未说是否预发）。[中/低，不确定]

### 1.5 Manager / Behavioral

- #8496901 Round 5："Managerial / Behavioral Round … Past projects / Technical decisions I had made / Challenges I had faced / Impact of my work / General behavioral/situational questions." [中]
- Glassdoor (Jun 29, 2026，Senior SWE，Accepted)："Recruiter Screen, HM round, technical round, virtual onsite (3 more technical rounds). All were organized well … Good focused questions that felt pertinent to the work, not just abstract LeetCode" Q："Why do you want to work at Abnormal?" [中]

### 1.6 额外的 Technical Deep Dive（"Fourth Round Video"？）

- #8496901 Round 6："After completing the above rounds, I was asked to take one additional technical round because the team wanted some additional signal … a **technical deep dive** into my experience and decision-making … The feedback was that the interviewer felt I lacked sufficient **judgment in a few areas**." [中]
- **"Fourth Round Video"** 这一名称：本次所有渠道**未找到**对应原文（任务书线索，可能来自官方候选人页，归 Agent B）。[待核]

### 1.7 其它（新流程周边）

- Take-home 版本（2026，部分地区）：Glassdoor SWE（May 5, 2026，Singapore）"Take Home Assessment to develop an application. They want to see your thinking and how you prompt AI to tackle the problem."；Glassdoor（Mar 12, 2026）"I spent more than 8 hours on it, only to be rejected 5 minutes after the screening call"。[中]
- 时间线：PracHub 指南聚合 "candidates report 4 rounds · ≈ 3-5 weeks"（"not a published process"）[低]；Glassdoor Senior SWE 平均 14 天/Software Engineer 平均 23 天/公司整体 30 天 [中]。
- 反馈与 ghosting：Glassdoor Senior SWE（Aug 1, 2025，London）"verbal offer … came back saying they were no longer making an offer"；LeetCode #8387564 "rejection email without any feedback"。与此相对 Glassdoor（Sep 14, 2026，PMM）"incredibly valuable feedback"。[中，混合]

## 2. 旧流程（2024 – 2025 年中，LC-adjacent / CodeSignal / take-home）

### 2.1 一亩三分地（经 Telegram 镜像 https://t.me/s/usinterview?q=abnormal，发帖时间取自 t.me 消息页；全文 1p3a 403，仅摘要）

| 日期（t.me） | thread | 摘要原话 | 可信度 |
|---|---|---|---|
| 2024-04-08 | 1059585 "Abnormal 店面" | "地里好像没有abnormal的面经 最近面的店面 不考利口题目是给你一堆图片 找出duplicate的图片如果memory有限 怎么做如果要hashing 怎样做 如果有hashing coll ..." | [中] |
| 2024-06-19 | 1072363 "tech screening 店面" | "非力扣题给images找duplicate，写出main function,我写的python,给了os.walk的用法提示直接call他给的_calculate_hash会有hash collision，问解决方法最后问syst ..." | [中] |
| 2024-06-30 | 1074077 "abnormal security 全套面经" | "abnormal 的面试跟其他公司有点不一样。每轮都会用一半时间讨论一个问题剩下时间做题。Phone Screen: 一小时时间 20 讨论 How do you identify duplicate images.Com ..." | [中] |
| 2025-07-15 | 1137132 "Abnormal 第一轮面经" | "一共4轮第一轮image deduplication不是力扣20 分钟讨论，30分钟写出来讨论如果你的file system里面有很多照片，如何删除重复的照片。**** 本内容被作者隐藏 ****变化 ..." | [中] |
| 2025-09-21 | 1146766 "Abnormal 第二轮面经" | "一共4轮第二轮manager chat单纯的聊天， 以下是我被问过的问题Tell me about yourself.What does your current team structure look like?What is a project you hav ..." | [中] |
| 2025-10-05 | 1148780 "Abnormal 第三轮面经" | "一共4轮第三轮 code review + system design这轮面试前有一个link给你预先code review,面试分两部分,开始就讨论一下你的comments,大概二十分钟换成system design*** ..." | [中] |
| 2025-10-13 | 1149759 "Abnormal 第四轮面经" | "一共4轮最后一轮了，跟第三轮一样分成两部分这轮是coding+past project deep divecoding 的题目是**** 本内容被作者隐藏 ****第二部分你要自己present一个problem dom ..." | [中] |

结论：2025-07 ~ 2025-10 的"4 轮"版本 = ① 图片去重（20 min 讨论 + 30 min 写）② manager chat ③ code review + system design（预发 link，~20 min 评论后换 SD）④ coding + past project deep dive（自己 present 一个 problem domain）。**这条线是 2025 年中前后，已被 2026 的 "AI + 已有代码库 + incident/SD + code review + manager + deep dive" 取代或演化**；二者共同点：每轮"一半讨论 + 一半做题"、code review + SD 同轮。

### 2.2 其它旧流程报道

| 日期 | 来源 | 内容原话 | 可信度 |
|---|---|---|---|
| 2023-11-20~22 | LeetCode Discuss #4308298/#4313040/#4315979（Bangalore SDE-2 offer 帖，三帖同一人） | "Interview - 1 OA + 1 Pair Programming + 2 Technical (Managerial) + 1 HR" | [中] |
| 2024-07-28 / 2024-11-20 / 2025-01-08 | Blind 帖 https://www.teamblind.com/post/interview-process-at-abnormal-security-india-mslv57b6 / .../abnormal-security-interview-ioxm8wuu / .../interview-process-abnormal-security-yofhrsz0 | 只有提问，无实质回复；ioxm8wuu 评论 "The recruiter said it's not leetcode, what exactly is it"（2025-05-15）；yofhrsz0（Staff SWE）评论里有人"free mock security interviews" | [低] 无内容 |
| 2024-01-12 | Blind https://www.teamblind.com/post/interview-at-abnormal-security-enowilwg | "I have an on-site interview with Abnormal Security with technical, project discussion and Manager interview." 无回答 | [低] |
| 2024-09 (Glassdoor 2025-09-16 发布) | Glassdoor SWE https://api.glassdoor.com/Interview/Abnormal-AI-Software-Engineer-Interview-Questions-EI_IE3146005.0,11_KO12,29_IP2.htm | "1st round was an online coding round. Then a take home assignment, which was discussed in another round. Had a final round which was discussion around past work." Q："Online assignment was around JSON Schema Parsing" | [中] |
| Jun 2023 面（Glassdoor 2024-06-12） | Glassdoor SWE 2 https://api.glassdoor.com/Interview/Abnormal-AI-Software-Engineer-2-Interview-Questions-EI_IE3146005.0,11_KO12,32.htm | "Had the first online assessment. Need to do using Python … The assessment had one real world coding challenge which is needed to be done using Python (not focused on DSA)." | [中] |
| 2025-01-30 | LeetCode Discuss #6347241 SWE II OA | "The OA was not a typical 1-hour assessment; it was a take-home assignment with a strong focus on security. The problem statement was quite open-ended, and completing it took me around 2 days. I was given 1 week" 被拒无反馈 | [中] |
| 2025-07-09 | LeetCode Discuss #6939818 SSE-Site Reliability | 两轮各 1h：Operational Fundamental + CodeSignal Python coding（CSV session → 每用户平均 session 时间，"Very similar to the leetcode design-underground-system"） | [中]（SRE 岗位，与 SWE II 不同） |
| 2024-09-12 | Glassdoor Senior SWE（Toronto） | 招聘人员电话 + 另一个 HM（senior engineering manager）电话；Q："What is the project that you are most proud of in your career?" | [中] |
| (官方 take-home 描述) | 搜索摘要：builtin.com 职位页 / resumegeni.com 提到 "AI-powered Development Challenge … Cursor and Copilot … 2-4 hours … within one week" | 仅搜索摘要，未直接抓取原页 | [低] |

## 3. 公共评价 / 综合指南（非一手，仅作线索）

- PracHub 公司页 https://prachub.com/companies/abnormal-security ：2 道公司题、1 条经验；更新 07.16.2025。指南页（"3 rounds · ≈ 3-5 weeks … not a published process"）：Recruiter Screen → Technical Assessment → Virtual Interviews Loop。[低，编辑撰写的通用指南；含"expected to leverage modern AI coding assistants"]
- PracHub Abnormal AI 指南 https://prachub.com/interview-guide/abnormal-ai-software-engineer-interview-questions-guide-2026 ：4 轮 Recruiter / HM / Technical Assessments / Interactive Pair-Programming，"AI leverage" 被评；明确 "No. It is PracHub's own research"。[低]
- Scoutify https://scoutify.com/companies/abnormal/interview/ ：19 条 "likely questions inferred from Abnormal's open roles"（面向销售/SE），**自述推断，不采信**。[低]
- Dataford / InterviewQuery / Jobmentis：429（Dataford `https://dataford.io/interview-guides/abnormal-security` 与 `/abnormal-ai/software-engineer/experiences` 均 429/Vercel checkpoint；InterviewQuery `/guides/abnormalsecurity-software-engineer` 429；Jobmentis 429）。**未取得内容，不判死刑**。
- Reddit：`search.rss`（全站与 r/cscareerquestions、csMajors、leetcode、ExperiencedDevs；部分 429）无相关帖（仅 r/techsales 2024-09-30 "Abnormal Security Interview"、r/sales 2024-01-15，均为销售岗，与 SWE 无关）。HN Algolia：无相关结果。
- 小红书/知乎/牛客：WebSearch 无结果。YouTube（David Hagar / Shrivu 视频）：WebSearch 无结果，留给 Agent B。

## 4. 关于 Chi 的 AI Technical Screen 的可验证点

| 问题 | 报道 | 来源 |
|---|---|---|
| Python？ | LeetCode #6071134（SWE3，2024-11）"it was mentioned something to do with Python"；SRE CodeSignal "You must write code in Python only"；旧 OA "Need to do using Python" | [中] |
| Django/Flask/FastAPI | 现场 AI screen：未提及框架（只有代码库名 "Sentinal"）；**take-home 多次明说 Django**（2026-10-09 更正，见 `glassdoor_2026-10-09.md`） | — |
| email / 安全领域 | 一人明确报道 security-events 管线（ingestion/ranking/rule-based threat level/alerts/API/DB） | #8335187 [中] |
| feature 类型（原话） | (1) "allow users to suppress some rules (it can be complex rules like based on geo-ip (existing in code) and other rules)"（面试官自称给错的题）；(2) "The enrichment layer currently hardcodes based on some threats (geo-ip, history, 1 more) clients want more configurability without touching platform code. Implement a plugin based mechanism …（very vague）" | #8335187 [中] |
| 同一代码库？ | 无直接证据；#8335187 与 PracHub 标题 "Live Security Events Codebase" 同域，推测 screen 代码库相同 | [低/中] |
| AI 工具 | "claude (allowed)"（#8335187）；搜索摘要称 "implement the feature … using Claude Code"（来源摘要，未核实原页）；旧 take-home 提 Cursor/Copilot | [中/低] |
