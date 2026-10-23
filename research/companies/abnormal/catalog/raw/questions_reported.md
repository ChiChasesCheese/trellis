# 被报道的题目（Abnormal AI / Abnormal Security）

访问日期 2026-10-06。可信度：[高] 一手/官方 · [中] 一手但只有摘要 / 带日期聚合 · [低] SEO/无日期。
LeetCode Discuss 链接说明：正文通过 `POST https://leetcode.com/graphql`（`ugcArticleDiscussionArticle(topicId:…)`）取得；下表 URL 写作 `leetcode.com/discuss/post/<topicId>`，由 topicId 构造（网页 HTML 403，未直接打开核对 slug）。
"一亩三分地" 条目只有 Telegram 镜像的摘要（thread 全文被作者隐藏或 403）。

| # | 类别 | 题目 / 任务（原话为主） | 轮次 | 角色 | 日期 | 来源 | 可信度 |
|---|---|---|---|---|---|---|---|
| Q1 | AI screen · coding（feature） | "We've to allow users to suppress some rules (it can be complex rules like based on geo-ip (existing in code) and other rules)."——面试官先给的"错题" | AI-assisted Screening Round | SDE（印度） | 2026-06-15 | LeetCode Discuss #8335187 | [中] |
| Q2 | AI screen · coding（feature） | "The enrichment layer currently hardcodes based on some threats (geo-ip, history, 1 more) clients want more configurability without touching platform code. Implement a plugin based mechanism to ensure no code touching by clients."（作者评：very vague；他先提 decorator pattern，20 分钟后用 Claude 全写）。代码库："processed all security events like collection/ingestion, ranking, threat levelling based on some rules, created alerts, created apis on top of it and put it to database." | 同上 | 同上 | 同上 | 同上 | [中] |
| Q3 | AI screen · coding | 练习题标题 "Extensible Security-Event Pipeline: Rule Suppression and Plugin-Based Enrichment"（正文付费） | Screening（Jun 2026 报告） | Software Engineer | 发布 2026-08-25 | https://prachub.com/interview-experiences/abnormal-ai-software-engineer-interview-experience-screening-round-built-on-a-live-security-events-codebase | [中]（与 Q1/Q2 互相印证；PracHub 标题即由 1p3a 1181621 派生可能性高） |
| Q4 | AI screen · coding（摘要） | "Screening Round面试要求基于一个现有的处理 Security Events 的 codebase 进行代码阅读与功能实现。该系统涵盖了数据 Collection/Ingestion、Ranking、基于规则的 Threa ..." | Screening Round | Abnormal AI 技术电面 | 2026-06-29 | 1p3a thread 1181621 via https://t.me/usinterview/28974 | [中] |
| Q5 | AI screen · coding | "Go through the codebase and explain how it worked … Implement an additional feature based on a problem statement provided by the interviewer. Discuss possible extensions and modifications"（feature 内容未披露） | Live coding / codebase walkthrough | SWE II | 2026-09-02 | LeetCode Discuss #8496901 | [中] |
| Q6 | AI machine coding | "I was given a problem to implement … explicitly allowed the use of AI tools"（题目未披露；评architecture/maintainability/why this approach） | Round 1 | SDE II | 2026-07-10 | LeetCode Discuss #8387564 | [中] |
| Q7 | AI screen · coding | "implement the feature with AI assistance, and add tests"（feature 未披露） | Technical Screen | SWE（NYC） | Jul 2026 | PracHub a2857641b5 | [中] |
| Q8 | incident | "given access to an AWS environment and had to investigate an incident": what went wrong / root cause / signals, logs, monitoring tools / immediate mitigation / long-term fixes | Round 3 part 1 | SWE II | 2026-09-02 | #8496901 | [中] |
| Q9 | incident | "started with a production incident that I had to investigate and resolve"（细节未披露） | Round 2 part 1 | SDE II | 2026-07-10 | #8387564 | [中] |
| Q10 | system design | "given an **existing system** and asked how I would scale it … Scaling reads / Scaling writes / Identifying bottlenecks / how the existing architecture would behave as traffic increased" | Round 3 part 2 | SWE II | 2026-09-02 | #8496901 | [中] |
| Q11 | system design | "in-depth system design discussion covering scalability, reliability, bottlenecks, and architectural trade-offs" | Round 2 part 2 | SDE II | 2026-07-10 | #8387564 | [中] |
| Q12 | code review | "given a small repository and asked to perform a code review … Identify issues / Prioritize them (P0/P1/etc.) / Explain why … / Suggest concrete improvements" | Round 4 part 1 | SWE II | 2026-09-02 | #8496901 | [中] |
| Q13 | system extension | "extending the system and discussing how it would behave at larger scale … Concurrency / Parallelism / Worker scaling / Message queue scaling / Throughput / Bottlenecks / Failure scenarios" | Round 4 part 2 | SWE II | 2026-09-02 | #8496901 | [中] |
| Q14 | code review + SD（旧） | "code review + system design这轮面试前有一个link给你预先code review,面试分两部分,开始就讨论一下你的comments,大概二十分钟换成system design" | Round 3 of 4 | SDE/General | 2025-10-05 | 1p3a thread 1148780 via https://t.me/usinterview/25663 | [中] |
| Q15 | coding + project（旧） | "coding+past project deep dive … 第二部分你要自己present一个problem dom ..."（题目被作者隐藏） | Round 4 of 4 | 同上 | 2025-10-13 | 1p3a 1149759 via https://t.me/usinterview/25767 | [中] |
| Q16 | coding（旧，非 LC） | "How do you identify duplicate images" / "给你一堆图片 找出duplicate的图片如果memory有限 怎么做如果要hashing 怎样做 如果有hashing coll(ision)…"；"写出main function，我写的python，给了os.walk的用法提示，直接call他给的_calculate_hash会有hash collision，问解决方法，最后问syst(em design)…"；"如果你的file system里面有很多照片，如何删除重复的照片" | Phone screen / 第一轮（"20 min 讨论 + 30 min 写"） | General | 2024-04-08 / 2024-06-19 / 2024-06-30 / 2025-07-15 | 1p3a 1059585 / 1072363 / 1074077 / 1137132（t.me/usinterview/17969, 18681, 18790, 24194） | [中] 四帖互相印证（疑似同类题持续使用；是否同一人未知） |
| Q17 | manager（旧） | "Tell me about yourself. What does your current team structure look like? What is a project you hav(e)…" | 第二轮 manager chat | 同上 | 2025-09-21 | 1p3a 1146766 via https://t.me/usinterview/25419 | [中] |
| Q18 | behavioral | "Why do you want to join Abnormal?" / "Why do you want to work at Abnormal?"（多条 Glassdoor 重复） | HM / screen | SWE / Sr SWE | 2025-07 ~ 2026-06 | Glassdoor https://api.glassdoor.com/Interview/Abnormal-AI-Senior-Software-Engineer-Interview-Questions-EI_IE3146005.0,11_KO12,36.htm 等 | [中] |
| Q19 | behavioral | "How did I use AI for my personal as well as professional work to better myself?" / "how I used AI in everyday work" | HM | Sr SWE / SWE | 2026-07-10 / Jul 2026 | Glassdoor Sr SWE（Bengaluru）；PracHub a2857641b5 | [中] |
| Q20 | behavioral | "Tell me about the most challenging project" / "What is the project that you are most proud of in your career?" | HM / manager | SWE / Sr SWE | 2026-02-23 / 2024-09-12 | Glassdoor（SF，Accepted；Toronto） | [中] |
| Q21 | behavioral | Round 5：Past projects / Technical decisions / Challenges / Impact / situational | Managerial | SWE II | 2026-09-02 | #8496901 | [中] |
| Q22 | deep dive | "technical deep dive into my experience and decision-making"；被拒原因 "lacked sufficient judgment in a few areas" | Additional round | SWE II | 2026-09-02 | #8496901 | [中] |
| Q23 | take-home（2026） | "develop an application … how you prompt AI to tackle the problem. The end product was an application that can support certain features." | Take-home | SWE（Singapore） | 2026-05-05 | Glassdoor https://api.glassdoor.com/Interview/Abnormal-AI-Software-Engineer-Interview-Questions-EI_IE3146005.0,11_KO12,29.htm | [中] |
| Q24 | take-home（2026） | "Assignment review & iteration"（四轮之首） | Round 1 | SWE | 2026-04-16 | Glassdoor 同上 | [中] |
| Q25 | take-home（旧） | "Online assignment was around JSON Schema Parsing" | OA | SWE | 2024-09 面 | Glassdoor …KO12,29_IP2.htm | [中] |
| Q26 | take-home（旧） | "a take-home assignment with a strong focus on security. The problem statement was quite open-ended … around 2 days … 1 week" | OA | SWE II | 2025-01-30 | #6347241 | [中] |
| Q27 | OA（旧） | "one real world coding challenge … using Python (not focused on DSA)" | OA | SWE 2 | Jun 2023 面 | Glassdoor SWE 2 …KO12,31.htm | [中] |
| Q28 | coding（SRE） | CSV `(userid, session time, session state)` → 每个用户平均 session 时间（类 LC 1396 Design Underground System）；"strip() the data"；CodeSignal，必须 Python；有 bonus/part 2 | Coding 1h | SSE-Site Reliability | 2025-07-09 | #6939818 | [中]（SRE，不同岗位） |
| Q29 | ops fundamentals（SRE） | "What happens when you type url in the browser / DNS / TCP vs UDP / TLS / two identical DB servers one slower—how to debug" | Operational Fundamental | SSE-SRE | 2025-07-09 | #6939818 | [中]（SRE） |
| Q30 | system design（DS/ML，非 SWE） | "design a system to detect and flag anomalous email attachments in real-time for a large enterprise"（搜索摘要，出处疑为 InterviewQuery 数据科学指南，429 未核） | DS | Data Scientist | 无日期 | https://www.interviewquery.com/interview-guides/abnormalsecurity-data-scientist（搜索摘要） | [低] |

## 对"AI 技术电面"最相关的归并

- 题型 1：给现有代码，**对已有行为加规则/开关**（rule suppression，含 geo-ip 复杂规则）。Q1
- 题型 2：把**硬编码的 enrichment 层改成可插拔（plugin/decorator）**，"clients 不碰平台代码"。Q2
- 两题描述刻意含糊；面试官改题；评分点在澄清、取舍（decorator vs registry vs config）、是否自己控制 AI，而非只让 AI 写完。（推断；原帖作者因没推进被评"No"的预期）
- 面试时间线对不上之处：#8335187 作者说看代码 ~10 min、再给 3 min、之后 20 min 挣扎；官方 60 min（~10 探索 + ~35 feature）。吻合。

## 未取得 / 待核

- 1p3a 1181621、1148780、1149759、1074077 全文（直连 403/Cloudflare；镜像仅摘要）。若 Chi 有账号，这四帖值得手动补读。
- PracHub 付费文 "Screening Round Built on a Live Security Events Codebase" 正文。
- "Fourth Round Video" 在任何渠道均无对应文字。
