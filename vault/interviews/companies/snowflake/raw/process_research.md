# Snowflake 后端 SWE（GenSWE, Menlo Park / Bellevue）面试流程调研

调研日期：2026-09-13。对象：Chi Zhang 收到的两封邮件——(a) Ashby 发的 "Initial Intake Instructions | Software Engineer - Backend"（Chakra 上 20–30 min "Talent Intake"）；(b) HackerRank-for-Work 发的 "Technical Screening Round — GenSWE - Menlo Park, CA/Bellevue, WA"（20 分钟 voice-to-voice AI interview）。

置信度标签：**high** = 一手候选人帖子或官方页面；**medium** = 转述/聚合但细节一致；**low** = SEO/AI 农场页。
无法抓取的页面已明确标注。1point3acres 全站（含 Playwright 浏览器）返回 Cloudflare 403，Glassdoor 同样 403；1p3a 内容通过其 Telegram 镜像频道 `t.me/s/usinterview` 与搜索摘要间接获取。

---

## 1. 2025–2026 Snowflake SWE / 后端 SWE 招聘流程（GenSWE, Menlo Park / Bellevue）

### 1.1 "GenSWE" 是什么

- **GenSWE = General Software Engineering Program**，Snowflake 官方的早期职业（early-career）通用 SWE 项目。官网原文："Designed for early career engineers"；"candidates are paired with teams based on experience, skill, and preference"；"Applications are accepted on a rolling basis, year-round"。列出的地点正是 **Menlo Park, CA 和 Bellevue, WA**。官方描述的流程："an initial conversation with a recruiter or hiring manager, technical interviews, panel interviews, and a team matching round." — https://careers.snowflake.com/us/en/generalsoftwareengineeringprogram（2026-09-13 抓取）**[high]**
- 含义：不是某个具体团队的岗位，而是**先过统一的技术 loop，再做 team matching**。候选人 1.5 年经验属于该项目目标人群（early career，通常对应 IC1/IC2）。
- Blind 上有 2026-02-09 的提问帖 "How is Gen SWE interview at Snowflake?"（ex-Amazon 用户），但页面抓取不到任何回复内容。— https://www.teamblind.com/post/how-is-gen-swe-interview-at-snowflake-ouhoegc5 **[high 帖子存在 / 无内容]**
- Blind 2022-10 的实习帖里 Snowflake 员工说："The hiring bar is probably pretty consistent across teams but interview processes may differ depending on which organization you interview with, e.g. product vs cloud" — https://www.teamblind.com/post/snowflake-team-selection-and-hiring-bar-for-swe-intern-d3zo2ycq **[high，但偏旧]**

### 1.2 官方流程（careers.snowflake.com/gethired）

官方 "Hiring Process" 页面对工程岗写明 4 个阶段，"up to two to four weeks"，并注明可能要求至少一次现场面试：— https://careers.snowflake.com/us/en/gethired（2026-09-13 抓取）**[high]**
1. **Initial Screen（30 min）**："a member of our recruiting team and/or the hiring manager will schedule a call to get to know you and your technical skill set"
2. **Technical Interviews（每轮 60 min）**："coding and/or system design interviews"，"live coding questions and assessments"
3. **Panel Interviews（3–5 轮 × 60 min）**："technical, expertise, system design, behavioral, and collaboration interviews"；"A 30-minute Tech Talk presentation may be included depending on the level and role"
4. **Decision**：debrief "typically within a few days"；30 天无回音视为不匹配。
- 官方页面**没有**提到 OA 或 AI 面试，但链接了一篇官方博客 "AI Cheat Sheet: How (and When) to Use AI in Your Snowflake Interview"（2026-06-09）。该博客正文抓取失败（只返回页面骨架）。— https://careers.snowflake.com/us/en/blogarticle/ai-cheat-sheet-how-and-when-to-use-ai-in-your-snowflake-interview **[页面存在，正文未获取]**

### 1.3 候选人报告拼出的实际 2025–2026 loop（早期职业 / IC1–IC2）

综合一手帖子，实际顺序大致是：

| 阶段 | 形式 / 时长 | 来源与置信度 |
|---|---|---|
| (0) HR call / 内推后 recruiter call | 15–30 min；Infra 岗一例 "不到 15 分鐘"，只聊过往 infra 经验、平台项目、方向偏好 | t.me/s/usinterview/29383（1p3a 镜像，2026 夏）**[high]** |
| (1) **AI 语音筛选（Chakra）** | ~20 min，开麦克风+摄像头+全屏共享，单显示器；BQ + 过往项目 | t.me/s/usinterview/28661, 28991, 29267（详见 §2）**[high]** |
| (2) HackerRank OA（部分候选人） | 3 题 / 90–120 min，Proctor mode | interviewfox / linkjob / prachub（§3）**[medium]** |
| (3) 技术电面 | 常见 **两轮 back-to-back**：1 coding + 1 system design，或 2 coding；每轮约 1 h（10 min 介绍 + 40 min 题 + 10 min 提问） | 1p3a thread-1179486（2026-06）、thread-1187965、Blind ict2 帖 **[high]** |
| (4) Onsite / panel | 4–5 轮：coding（可能加一轮）、resume/project deep dive（"expertise"）、system design、BQ/manager；IC2 有 "4 hour onsite in-person" 报告 | 1p3a thread-1113703、Blind snowflake-ic2-onsite-ctuk0fyl **[high]** |
| (5) Team matching | GenSWE 官方流程最后一步 | 官网 **[high]** |

具体一手证据：
- **2026-06 SDE 电面**（1p3a thread-1179486，搜索摘要）："1-hour interview with a Chinese interviewer: ~10 min intros, 40 min coding with follow-ups, 10 min Q&A"，题目为 **LC 1751 Maximum Number of Events That Can Be Attended II** 变体。— https://www.1point3acres.com/bbs/thread-1179486-1-1.html **[high，正文 403，来自搜索摘要+Telegram 28733]**
- **2026-08 IC1 时间线**（Telegram 29627 镜像 1p3a）："8.3 内推 8.4 约 hr call 8.7 hr call后当天约面"，"两轮coding"，"人都很好"。— https://t.me/s/usinterview/29627 **[high]**
- **电面两轮 back-to-back**（Telegram 29571 → 1p3a thread-1187965）：coding 一道简单 LC 风格题；system design 为 "a notebook similar to SQL that supports users running queries"，重点讨论 client 如何拿结果。— https://www.1point3acres.com/bbs/thread-1187965-1-1.html **[high]**
- **Onsite 结构**（1p3a thread-1113703 搜索摘要）：4 轮 = 2 coding（其中一轮可能是因初轮 coding 表现加的）+ 1 resume-based + 1 BQ。— https://www.1point3acres.com/bbs/thread-1113703-1-1.html **[medium，正文 403]**
- Blind 2025-10-04（ex-Google, IC2）："Despite seemingly doing quite well ... on the first two tech screens, I got called in for a 3rd due to coding speed."；评论："The first two are just screens, doesn't signal anything"；"you need to get Hire in all the remaining ones." — https://www.teamblind.com/post/snowflake-onsite-tips-wzrlktbi **[high]**
- Blind 2025-03-26（IC2）："Have a 4 hour onsite in-person interview"；电面 "2 rounds DSA (2 questions in each) medium to hard"，需要提示但都解出。— https://www.teamblind.com/post/snowflake-ic2-onsite-ctuk0fyl **[high]**
- Blind 2025-03-09（Global Platform 团队，"ICT2"）："2 1 hours coding rounds on coderpad"，回复多为 "Mediums"，一条 "Hard also"。— https://www.teamblind.com/post/snowflake-ict2-phone-screen-interview-7x0pcrot **[high]**
- Blind 2025-03-05 拒信帖：两轮 coding（LC mediums + 1 OOD）后无 onsite 直接拒，无反馈。— https://www.teamblind.com/post/snowflake-interview-rejected-for-no-reason-gsuxeszj **[high]**
- Blind 2026-09-05 "Snowflake expectations interview from senior swe"（仅列表可见）："initial will be screening rounds which will be 1 coding 1 system design"。— https://www.teamblind.com/company/Snowflake/posts/snowflake-interview **[medium，仅摘要]**

### 1.4 时长 / 回复节奏

- 官方："up to two to four weeks" **[high]**。
- linkjob（2026-03-16，自称一手）："around two weeks" if smooth **[low-medium]**。
- Leon Consulting（2026-05-04）：电面后 3–5 天回复；onsite 后 1–2 周；总体 4–6 周 — https://leonstaff.com/blogs/snowflake-interview-process/ **[low]**
- Aced/Exponent 指南（2026-08 更新）：2–4 周典型，senior 4–6 周 — https://www.tryexponent.com/guides/snowflake-software-engineer-interview **[medium]**
- 一手：内推→HR call→当天约面仅 4 天（Telegram 29627）**[high]**。

### 1.5 "没有经典 behavioral 轮 / 以 resume deep dive 为主" 的说法——核实结果

- **部分正确，且随 level 与 org 变化**：
  - 官方 panel 组成明确列出 "behavioral" 与 "collaboration" 两轮 **[high]**。
  - 但 Snowflake 的 "**expertise**" 轮实质是 project walkthrough：Blind 2024-06（Asana 用户，IC3）："They asked me to pick a project from past/recent job and deep dive into it for good 40 mins"，追问 "why/how I made the decisions ... technical architecture, approach and external libraries"，并延伸到 availability / fault tolerance。— https://www.teamblind.com/post/snowflake-expertise-interview-xcavd10l **[high]**
  - Blind 2024-11-15 "Why is snowflake interview so weird?"（ex-Google）："no challenging coding problem, weird presentation interview for 90 mins"；Snowflake 员工回复 loop 是 "past projects, no leetcode style coding questions, no overly difficult system design questions"。— https://www.teamblind.com/post/why-is-snowflake-interview-so-weird-xaazhjnx **[high，偏 senior]**
  - 早期职业一手帖：Telegram 28723 "15-minute behavioral question about recent projects and technical challenges" 嵌在 coding 轮里；28738 onsite 第一轮 "extensive project discussion (~20 min)" 再做 coding；1p3a onsite 帖单独有 "1 resume-based + 1 BQ"。**[high]**
  - Blind 2021 老帖："2-3 coding rounds, one sys design and one behavioral" — https://www.teamblind.com/post/snowflake-interview-swe-hdursof4 **[high，旧]**
- **结论**：对 IC1/IC2，behavioral 通常不是纯 STAR 独立轮，而是 (a) 嵌在技术轮开头 15–20 min 的 "讲你最近的项目 + 技术挑战"，以及 (b) onsite 里的 resume/project deep dive 轮 + manager 轮。准备重点是**能被追问三层的项目故事**，而不是背 STAR 模板。

---

## 2. Snowflake AI 筛选面试（Chakra / HackerRank AI）2026 候选人报告

### 2.1 Chakra 本身（官方）

- Chakra 是 HackerRank 的 AI interviewer，2026 年 2 月正式发布；YC launch 页 "Chakra: AI interviewer that finally works"。官网："an AI interviewer from HackerRank"，voice/video、实时自适应追问、integrity 监控（tab 切换等）、给招聘方 "transcript-backed rationales"。— https://www.chakra.sh/ ，https://www.ycombinator.com/launches/PQb-chakra-ai-interviewer-that-finally-works **[high]**
- HackerRank 说明：三阶段 "interview creator builds the plan → interviewer conducts → reporter evaluates the transcript"；每条 expectation 打 3 (Met)→0 (Not Assessed)，归一到 0–5 给 recruiter；报告 "within minutes"，包含逐维度分数、转录、摘录、推荐；候选人异步在窗口期内完成。— https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work **[high]**
- HackerRank 2026-07 release notes：Chakra 新增 **in-line code editor**（可要求写代码并追问），"must-have requirements" 权重更高；Desktop App 下检测多显示器 / 退出全屏会 "pauses the interview until required interview conditions are restored"；有 gaze detection、全程录像回放、CSV 导出分数。— https://support.hackerrank.com/articles/8142080826-july-2026-release-notes **[high]**
- 官网示例里 "candidate background section" 约 5–8 分钟。**[high]**

### 2.2 Snowflake 候选人一手报告（2026）

以下三条来自 1point3acres（正文 403），通过 Telegram 镜像 `t.me/s/usinterview` 读到摘要。日期按帖子 ID 序推断（1178789 ≈ 2026-06；1181800 ≈ 2026-07；1185571 ≈ 2026-08），Telegram 只显示时分。

- **"Snowflake General SWE AI Interview"**（全职跳槽，video interview）：一周内完成，**约 20 分钟**，需开麦克风、摄像头、全屏共享；界面左侧显示 AI 对话与候选人回答的实时转录。— https://t.me/s/usinterview/28661 → https://www.1point3acres.com/bbs/thread-1178789-1-1.html **[high]**
  - 注意标题就叫 "General SWE"，与 GenSWE 一致——说明 GenSWE 通道 2026 年中已经在用这个 AI 环节。
- **"雪花 AI Screening"**（全职，标为 HR 筛选阶段）：第一次遇到 AI 筛选；要求摄像头+麦克风+屏幕共享，**禁止外接显示器**；左侧实时文字转录双方对话，右侧自己的摄像头画面；问题是**常规 HR 问题**（背景、资格）。— https://t.me/s/usinterview/28991 → https://www.1point3acres.com/bbs/thread-1181800-1-1.html **[high]**
- **"Snowflake OA ai 面试"**（全职跳槽）原文："刚刚面完 snowflake 的 oa。挺新奇的一种面试方式，20分钟跟ai 聊天，会跟你提一些bq 和 聊一下你过去的项目。然后他会根据你说的进行一下ai 总结。ai 语音识别能力还挺强..." — https://t.me/s/usinterview/29267 → https://www.1point3acres.com/bbs/thread-1185571-1-1.html **[high]**
  - 要点：**无 coding**；BQ + 项目；AI 会对你说的内容做总结（可能是复述确认）。
- Blind 2026-05-12 "Snowflake chakra AI"（Amazon 用户，SWE 岗）："Anyone know how this chakra ai round thingy is supposed to look like? I applied for swe role and got an invite for it"。回复：Meta 用户 "Me too lol what on earth is this"；Snowflake 员工只贴了 chakra.sh 链接；2026-08-20 Microsoft 用户追问 "SDE/Backend Software Engineer" 岗的格式（resume/project-based? behavioral? technical?），**无人给出实质答案**。— https://www.teamblind.com/post/snowflake-chakra-ai-wg7wd28k **[high]**
  - 说明：5 月起全职 SWE 就在收 Chakra 邀请；Snowflake 内部员工也不清楚这个环节。
- 1point3acres 面经索引列出 "Snowflake 2026 Fall Intern Software Engineer **Video Interview** Questions"（2026-08-24）以及 "Snowflake HR Screening Experience for Software Engineer Position"（2026-09-03）、"Fulltime Software Engineer Tech Phone Screen"（2026-09-04），但具体条目 URL 抓不到。— https://www.1point3acres.com/interview/company/snowflake **[medium]**

### 2.3 聚合站对 Chakra@Snowflake 的转述

- PracHub（2026-08-16，实习向）：引用 "July 2026 report: self-introduction, a project deep dive, and tailored follow-ups"；另一报告 "voice conversation about experience, applied scenarios, collaboration, and decision-making"（与候选人邮件措辞一致）；"recent Snowflake reports lean more toward background, project, collaboration, and decision-making questions"；"In a May 2026 discussion, candidates described receiving both links, only Chakra, or a delayed HackerRank link"。— https://prachub.com/resources/snowflake-swe-intern-oa-2027-hackerrank-chakra-ai-interview-and-what-comes-next **[medium]**
- Aced/Exponent（2026-08）："Some Snowflake software engineer candidates in 2026 have reported an AI-conducted screening interview early in the process"，"No live engineer joins it, and it isn't confirmed as a standard part of the loop"。**[medium]**
- interviewfox（2026-08-01）：Chakra "sits before or alongside the coding OA"，"some candidates getting Chakra and then the OA, some getting both at once, and some getting Chakra with no coding OA at all"。— https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/ **[low-medium]**
- Blind 2026-07-03 "Hackerrank AI interview, auto fail?" —— **不是 Snowflake**（某 startup），60 min AI 面含 LC hard graph 题；仅说明 HackerRank AI 面在别处可含 coding。— https://www.teamblind.com/post/hackerrank-ai-interview-auto-fail-e74cui4j **[high，非 Snowflake]**

### 2.4 对候选人两封邮件的解读

- 邮件 (a) Ashby "Talent Intake" 20–30 min on Chakra，"Chakra only gathers information, human recruiter reviews" ——对应 1p3a "雪花 AI Screening" 那种 **HR 类问题**的环节；Ashby 是 Snowflake 的 ATS（Ashby 客户列表含 Snowflake）。
- 邮件 (b) HackerRank "Technical Screening Round — GenSWE" 20 min voice-to-voice，四块内容（经验/应用场景/协作与决策/提问）——对应 "Snowflake General SWE AI Interview"（28661）和 "20分钟跟ai聊天 bq+项目"（29267）。一手报告**均未提到写代码**；但 Chakra 技术上支持内嵌编辑器，且邮件写了 "applied scenarios"，应准备口头讲一个后端场景（如限流/幂等/重试/一致性）的推理。
- 两封邮件可能是**同一 Chakra 会话的两种通知**（Ashby 触发 + HackerRank 发链接），也可能是两个环节（intake → technical screening）。PracHub 提到 "receiving both links" 的混乱情况。建议直接问 recruiter 是否是同一环节。
- 之后环节：一手报告的顺序是 AI 筛 → HR call → 两轮 back-to-back 技术电面（coding + SD 或 2 coding）→ onsite。AI 筛后的拒信时间线**没有找到一手数据**。

### 2.5 环境硬要求（多源一致）

摄像头 + 麦克风 + 全屏共享；**单显示器**（外接屏会被暂停）；关闭其他应用；有 gaze detection；全程录像。建议用 HackerRank Desktop App 提前测试。**[high]**

---

## 3. OA 格式与技术电面题型（后端 SWE）

### 3.1 OA（HackerRank）

- 格式：**3 题 / 120 min**（也有 90 min、135 min 报告），HackerRank Proctor Mode（每 15 s 截屏）；分数按 "correctness + efficiency"。— interviewfox（2026-08-01）**[low-medium]**；linkjob（2025-10-14）3 题 120 min **[low-medium]**；1p3a 实习 OA 帖 "135 分钟 3 题（2 DP + 1 backtracking）" **[medium，搜索摘要]**
- 拒信可 "within hours"（interviewfox）**[low]**。
- 是否所有 GenSWE 候选人都有 OA：**不确定**——2026 一手全职帖里多数直接从 AI 筛/HR call 进电面，OA 报告以实习/新毕业为主。
- 报告过的 OA 题名（多为 HackerRank 自定义题）：
  - "Prime String", "Text Scoring", "String Transformation" — linkjob 2025-10-14 https://www.linkjob.ai/interview-questions/snowflake-hackerrank-oa/ **[low-medium]**
  - "Prime String", "Work Schedule", "String Formation" — 1p3a 实习 OA https://www.1point3acres.com/bbs/thread-1092121-1-1.html **[medium，搜索摘要]**
  - "String Patterns", "Paint the Ceiling", "Task Scheduling" — linkjob 2026-03-16 https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ **[low]**
  - "Maximize OR-Sum", "Student Enrollment System (OOP)", "Min-Height-Trees variant"；轮换池含 "Calculate Amount Paid in Taxes", "Tree Levels After Node Deletions", "Happy Number", "SnowCal", "Recipe Sequence Matcher", "N-Queens", "Design a Quota System", "Parallel Courses III", "Meeting Rooms II", "Cheapest Flights K Stops", "Word Search" — interviewfox 2026-08-01 **[low]**
  - Medium（Berlin 实习 OA）页面 403，未能核实。

### 3.2 技术电面题（一手，2025–2026）

| # | 题目 | 轮次 / 备注 | 来源（URL, 日期） | 置信 |
|---|---|---|---|---|
| 1 | **LC 1751 Maximum Number of Events That Can Be Attended II** 变体 + follow-up | 2026-06 电面，40 min | 1p3a thread-1179486（2026-06）；t.me/s/usinterview/28733 | high |
| 2 | **Happy Number**，先 O(n) 再优化到 O(1)（Floyd 判环）；前 ~20 min 讲项目 | onsite/电面 round 1 | t.me/s/usinterview/28738 → 1p3a thread-1179571（2026 夏） | high |
| 3 | **Design user password storage**（系统设计） | 同上 round 2 | 同上 | high |
| 4 | **OOD: `addTask(taskId, priority, timestamp)` / `executeTask()`**，同一 task 可在不同 timestamp 重复 add | onsite coding，挂 | t.me/s/usinterview/29167 | high |
| 5 | **Queue class（类 Python deque）→ 扩展为云端 queue service**，讨论 enqueue/dequeue 在故障下的行为 | onsite SD，挂 | t.me/s/usinterview/29299 → 1p3a thread-1185881 | high |
| 6 | **SQL notebook（类 LeetCode 运行 SQL）设计**，重点 client 如何取结果 | 电面 SD（2 轮 back-to-back） | t.me/s/usinterview/29571 → 1p3a thread-1187965 | high |
| 7 | **KV store 系统设计** | 2025-12 两轮 back-to-back 电面 | 1p3a thread-1158595（搜索摘要） | medium |
| 8 | **Design a Quota System used by multiple upstream services** | SD 轮（"可用 AI" 帖） | 1p3a thread-1137616（搜索摘要） | medium |
| 9 | **Design a SQL engine running loads of queries as a cron job** | IC1/IC2 SD，面试官很沉默 | https://www.teamblind.com/post/snowflake-ic1ic2-system-design-interview-1dd4vqt7（2025-07-03） | high |
| 10 | "Event Stream Problem", "Distributed Tree Counting", "Reverse Alphanumeric Segments", "Design Audit Logs Service", "Dynamic Blacklist Filter System" | 1p3a 2026 面经索引标题 | https://www.1point3acres.com/interview/company/snowflake | medium |
| 11 | Web Crawler (BFS), Parentheses Matching, Service Startup 依赖排序 (Kahn), DAG cache for query views | 电面/SD | linkjob 2026-03-16 | low |
| 12 | Job Scheduler 等（"snowflake system design 大汇总"） | SD 汇总 | 1p3a thread-1091322（403） | medium |
| 13 | Cron Job Scheduler, transactional in-memory KV store, thread-safe multi-rule rate limiter, distributed tree node counter | 指南汇总 | https://prachub.com/interview-guide/snowflake-software-engineer-interview-guide（2026-09-03 更新） | low-medium |
| 14 | Patching Array（LC 330） | 老电面 | https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/（页面 403） | medium |

- 题型规律：**LC medium 为主、常带更难 follow-up**；**OOD / 类设计**（task scheduler、deque、stream processor）出现频率高；系统设计偏 **infra / data**（queue、KV、quota、audit log、query notebook）而非 product。Blind 2024-09 senior 帖："They ask extremely hard LC questions and most of those hard questions includes 1 follow up"；"they ask db heavy questions" — https://www.teamblind.com/post/snowflake-senior-software-engineer-interview-x6sjbqfs **[high，偏 senior]**
- 面试官风格：一手帖说 "人都很好"、会给 hint 与帮 debug；但也有 "interviewer remained largely silent" 的 SD 报告。**[high]**
- 语言/内部机制追问：多家指南称电面含 "Java/C++ 内存模型 / 并发" 15 min（Leon、Aced）**[low-medium]**；一手帖未见。

---

## 4. Behavioral / Hiring-manager 问题与 Snowflake 价值观

### 4.1 官方价值观（8 条）

Put Customers First, Integrity Always, Think Big, Be Excellent, Get It Done, Own It, Make Each Other the Best, Embrace Each Other's Differences。— Comparably / Built In 汇总 https://builtin.com/company/snowflake/faq/culture-values **[medium]**。Aced/Exponent 与 spacecomplexity 等指南只列 5 条（漏 Integrity Always / Be Excellent / Embrace Differences），以官方 8 条为准。

### 4.2 候选人报告的 BQ / 项目追问

- 一手：技术轮开头 15–20 min "最近的项目 + 技术挑战"（Telegram 28723, 28738）**[high]**；HR call 问 infra 经验、平台项目、方向动机（29383）**[high]**；onsite 有单独 resume 轮 + BQ 轮（1p3a thread-1113703）**[medium]**。
- Blind IC2 帖（搜索摘要）："The behavior/manager round matters even for IC2, and you should clearly articulate what you've done in the past and what the impact was." **[medium]**
- Expertise 轮追问方式：为什么选这个架构 / 这个库，替代方案，availability / fault tolerance 怎么做（Blind expertise 帖）**[high]**。

### 4.3 指南列出的典型问题（非一手，但多源一致）

- "Tell me about a time you made a mistake."
- "Tell me about a time when you took ownership over a project, and why."
- "Describe a time when you had to work effectively with another team that you had never worked with before."
- "Tell me about a time when you wouldn't have successfully completed a project without teamwork."
  — Exponent 博客镜像（U. Miami，2026-05-14）https://customcareer.miami.edu/blog/2026/05/14/get-a-job-at-snowflake-interview-process-and-top-questions/ **[medium]**
- 价值观映射（spacecomplexity，2026-06-01，引用 Glassdoor）：Own It ↔ 未被指派就承担责任 / 承认错误并说出具体改了什么流程；Get It Done ↔ 砍什么、保什么、slip 前先沟通；Make Each Other the Best ↔ disagree-and-commit、主动帮同事、接受批评；Think Big ↔ 扩大 scope 的证据。— https://spacecomplexity.ai/blog/snowflake-behavioral-interview-questions **[low-medium]**
- Aced/Exponent 指南（2026-08）：behavioral 信号 "surface across the final panel, not only in a dedicated behavioral slot"；主题 "a time you put the customer first when it was inconvenient / raised the bar / took ownership outside your scope"。**[medium]**

### 4.4 对 AI 筛选环节的推论

邮件 (b) 的四块（experience & background / applied scenarios / collaboration & decision-making / questions for them）与 Chakra 一手报告（"bq + 过去的项目"）一致。结合 Snowflake 价值观，最可能被追问：Own It（端到端负责的事）、Get It Done（deadline 取舍）、Make Each Other the Best（冲突/反馈）、Put Customers First（PayPal/Braintree 的商户/支付场景可直接对上）。AI 会针对模糊处追问，所以每个故事要有可量化结果与一个"当时不那么做会怎样"的反事实。

---

## 5. 早期职业（IC1/IC2）薪酬，Menlo Park / Bellevue，2026

Snowflake 级别：IC1 = Software Engineer I，IC2 = SWE II，IC3 = Senior，IC4 = Staff，IC5/6 = Principal，IC7 = Distinguished。— https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic1 **[high]**

| 级别 / 地区 | 中位 TC | Base | 年股票 | Bonus | 来源（2026-09-13 抓取） |
|---|---|---|---|---|---|
| IC1 US | $232K | $166K | $58K | $8.6K | levels.fyi ic1 **[high]** |
| IC1 SF Bay Area | $236K | $168K | $58K | $9.9K | https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic1/locations/san-francisco-bay-area **[high]** |
| IC2 US | $348K | $196K | $145K | $7.6K | https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2 **[high]** |
| IC2 SF Bay Area | $341K | $197K | $133K | $10.8K | https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2/locations/san-francisco-bay-area **[high]** |
| IC2 Greater Seattle | $323K | $192K | $120K | $11.7K | https://www.levels.fyi/companies/snowflake/salaries/software-engineer/levels/ic2/locations/greater-seattle-area **[high]** |

- Blind 一手 offer：IC1 Seattle 实习 return offer（2025-01-19）base $140K + equity $55K + bonus $14K + sign-on $3K = **$209K** — https://www.teamblind.com/post/New-Grad-Snowflake-vs-Optiver-Nx8HaORt **[high]**；IC1 Snowflake AI 团队 new grad（2025-12-16）"~200k" TC 与 Google 持平 — https://www.teamblind.com/post/google-vs-snowflake-ai-new-grad-d8uhgv6r **[high]**。
- levels.fyi 单条：IC2 Bellevue，7 YOE，TC $396K（2025-03）— https://www.levels.fyi/offer/4d968a49-6c0d-4bcc-8950-fa4dbe551441 **[high，但非早期职业]**
- 结构：RSU 4 年，首年 25% 后按月/季；bonus 目标约 15% base（jobsbyculture 2026-05-13，称 SNOW ~$174，YTD -20%）— https://jobsbyculture.com/blog/snowflake-compensation-2026 **[low]**。
- 对 1.5 YOE 候选人：大概率定 **IC1**，争取 IC2 需两轮电面 + onsite 全 Hire；Blind 有 "Snowflake downlevel" 讨论。

---

## Contradictions / unknowns

1. **AI 面试是否包含 coding**：Snowflake 三条一手报告均为纯对话（BQ + 项目）；但 HackerRank 2026-07 起 Chakra 支持内嵌代码编辑器，且邮件写 "applied scenarios"。不能排除口头技术场景题，写代码可能性低。
2. **两封邮件是一个环节还是两个**：Ashby "Talent Intake"（20–30 min）与 HackerRank "Technical Screening Round"（20 min）措辞不同；PracHub 描述过候选人 "receiving both links" 的混乱。未找到明确一手解释。建议问 recruiter。
3. **AI 筛选后的顺序**：有报告 AI 筛 → HR call → 电面，也有 HR call 在前的（29627 时间线未提 AI 环节）。GenSWE 的 OA 是否必经：2026 全职一手帖里几乎没人提 OA，OA 报告集中在实习/新毕业。
4. **AI 筛后的拒信时间线**：无一手数据。
5. **电面轮数**：两轮 back-to-back（coding + SD）与两轮纯 coding 都有 2025–2026 报告，取决于 org（product vs cloud/infra）。
6. **Behavioral 轮**：官方 panel 列有 behavioral + collaboration；但候选人体验多为嵌在技术轮的项目讨论 + resume 轮 + manager 轮，senior 另有 tech talk。IC1/IC2 是否有 tech talk：官方说 "depending on the level"，一手早期职业帖未见。
7. **难度矛盾**：Blind 上既有 "extremely hard LC + follow-up"（senior/DB org），也有 "Mediums"（Global Platform, ICT2）和 "no leetcode style"（senior loop）。早期职业一手题目多为 medium + OOD。
8. **面试题数据来源风险**：interviewfox / linkjob / prachub / spacecomplexity 为 AI 生成或带推广的聚合页（linkjob 明写靠 "undetectable AI interview assistant" 拿 offer），其题目列表只能当参考。
9. **未能抓取**：1point3acres 全部帖子正文（Cloudflare 403，含 Playwright）、Glassdoor（403）、LeetCode Discuss（403）、Medium Berlin 实习 OA（403）、Snowflake 官方 "AI Cheat Sheet" 博客正文（仅页面骨架）、Blind GenSWE 提问帖的回复（页面无内容）。1p3a 的三条 AI 面试帖日期为按帖子 ID 推断（2026-06 至 2026-08）。
