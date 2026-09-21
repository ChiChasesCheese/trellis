# 编码题与技术筛证据（SWE / Quant Dev-Python / 早期职业；全公司范围）

> 采集日期：2026-09-21。**LEaD 自己的题目零一手报道**（Glassdoor 唯一一条 Miami 2026-02 报告说"3 轮，几乎全是 behavioral"，见 `process_and_rounds.md`）。所以本文件收的是 Millennium **SWE 类岗位**的全部可及编码题证据，按"与 45 min 一人 HackerRank 实时编码"的相关度排序。
> 置信度：**[高]** = 一手候选人原文（可读全文）；**[中]** = 一手但只读到摘要（Telegram 镜像 / 搜索摘要），或聚合站标了日期与轮次；**[低]** = SEO 站泛泛之谈。可达性见 `sources_index.md`。

## 1. 一手、可读全文

### 1.1 LeetCode Discuss 7423863 · "Bad experience interviewing at Millennium"（2025-12-19，Quant Developer – Python，5 轮）**[高]**

| 轮 | 题 | 备注 |
|---|---|---|
| R1 DSA | **Trapping Rain Water**（LC 42）+ **Container With Most Water**（LC 11） | 一轮两题，都要"working and optimized" |
| R2 DSA + Python | **Number of subarrays whose sum is divisible by K**（LC 974；前缀和取模 + nC2）· **asyncio：写出能跑的代码并解释 coroutine 等机制** | |
| R3 | **Multithreading + Pandas aggregation**："given a dataframe or csv which can contain millions of records, group them by a common identifier and find the aggregated sums" —— 候选人分块聚合再合并；**面试官允许开浏览器查语法** | 最贴近 LEaD JD（Pandas/NumPy）的一题 |
| R4 Behavioral | 闲聊：who are you、why join | 之后自动拒信；recruiter 说 3 人进终面选 1 |
| R5（重开的技术轮） | **"price data design problem"** · **decorator code writing**（少写一个括号、要求 debug 时间被拒）· 概率题：5 红 3 蓝，第一个是红的条件下再抽到红的概率 · why this/that | 之后被 ghost |

作者建议："read on **asyncio, decorators, generators, multithreading, multiprocessing, pandas, context managers**"。

### 1.2 LeetCode Discuss 6020524 · Bangalore SWE 2024-06 [Offer]**[中，搜索摘要 + WebSearch 转述；原页 Cloudflare 拦截]**

- 一整轮 = **项目讨论**："pick a project… objectives, approach, tech stack, design, challenges, database strategy"，"open conversation between employees"，同时评沟通与知识。
- Comp（Bangalore）：base ₹50L + JB ₹10L + bonus 至 100%（首年约 ₹10L 固定）≈ ₹71L 首年。

### 1.3 IIT Delhi QR 实习一手（GitHub devclub-iitd）**[高，QR]**

R2 是 DSA 一题 + "favorite data structures / algorithmic trade-offs" 口头讨论；R3 HR 讲动机与"problem-solving style"。

## 2. 一手、只读到摘要（1point3acres 经 Telegram 镜像 `t.me/s/usinterview`）**[中]**

| 1p3a thread | 岗位 | 形式 | 题 |
|---|---|---|---|
| **1090775** | **C++ Developer（Risk, Central Team）电面** | **45 min = 15 min 背景 + 30 min 一题** | **大整数字符串相加**；面试官几乎不给反馈 |
| 660546 | 技术电面（12 年经验的俄罗斯面试官，无寒暄） | 电面 | **HashMap / HashSet 细节，尤其冲突处理；Java 8+ 怎么处理冲突** |
| 1124751 | "Millennium 技术面" | 电面 | 简历项目（chatbot）：tech stack、模块关系；**异步编程**追问 |
| 1029420 | onsite | 现场 | 互相介绍后突然考 **Python 基础**，候选人"好几题答不上" |
| 1079245 | Developer OA | 2 h / 5 题 | **SQL 基础、Python decorator**、最后一题难 |
| 855488 | Quant/FE OA | 3 h / 4 题 | 3 道 Python 直白、**SQL 一题挂** |
| 939377 | DS/DE OA | 120 min / 8 题 | 3 概率选择 + 3 算法选择 + 1 SQL + 1 coding，1 h 可做完 |
| 1143768 | Quant Dev OA + 1 h 电面 | 2 h / 10 题 | 多为 **git** 与选择题 + Python3 coding |
| 1096305 | Quant Dev OA（系统化股票 pod） | HackerRank 3 题 medium | 主题 transaction cost analysis，Python |
| 1141729 | **2026 SDE intern OA** | 5 题 | **3 选择 + 1 "industrial coding" + 2 算法** |
| 668645 | Senior SWE OA | HackerRank **180 min** | "quite difficult"，多种数据结构 |
| 918431 | SWE OA（HR 筛后） | **4 h** | 内容未述 |
| 1149521 | Full Stack OA | — | 简单题，含 Angular；被三个组分别面 |
| 1158922 | SDE mid-level onsite | — | 题隐藏；评价"公司文化挺卷，强调 autonomy 与 personal accountability" |
| 1167855 | **Forward Deployed Engineer，Miami**（2026-03） | 2 轮：技术电面 + HM | 因 YOE 不够被转介其它岗 |
| 951597 | 2023 SDE Intern（C++/Java，NYC/Miami）Timeline | 完整流程帖 | 正文 403 未读到 |

## 3. Blind（正文 403；搜索摘要）**[中]**

- "millennium management second round swe"：**第二轮 = 三场技术面，每场 45 min，都在 HackerRank**。
- "interview steps at millennium management"：**HackerRank → HM call → technical screen → virtual onsite（约 5 人）→ skip-level manager phone → offer**。
- "millennium management fullstack interview"：3 轮，只给会议邀请 + HackerRank 链接、无准备材料；recruiter 说 **"frontend doesn't matter — backend: Python, SQL, maybe system design"**；另一回复："questions relevant to the job, **not very hard and not leetcode style**, some backend code, SQL, and discussion about system components like Kafka"。
- "millennium management software engineer phone interview"：**第一轮一道简单图题（LC medium）**；"about 30 minutes of a 45-minute interview on resume/experience"。
- "Millennium Hackerrank"：Millennium LP 的 HackerRank OA **75 min / 2 题**；"someone familiar with their HackerRank account: **they don't give LeetCode-type questions**"。
- "millennium technical interview"："HackerRank-style screen leaning heavily on coding, **mix of Python and SQL**, main thing is **speed**".
- "Millenium LEaD program"：早期职业 2–5 YOE SWE 问 TC；回复 "Lead is relatively new and is strictly Miami office"、"TC roughly what MSFT pays you for your YOE"。
- 另一 Blind 摘要："**The LEaD program starts with a 90 min video interview**"（日期不明；与本次 45 min 邀约不一致 → 视为旧格式或另一 req，见 `process_and_rounds.md` §矛盾）。
- "why millennium" / "interview with millennium management"：**"focus on your resume/projects and more practical problems instead of LeetCode"**（多帖共识）。

## 4. 聚合站（标了轮次与日期的优先）

### 4.1 PracHub（`prachub.com/companies/millennium`，Last Updated 2026-07-30）**[中]**

| 题 | 轮 | 日期 |
|---|---|---|
| **Implement paginated API ingestion** | Technical Screen | 2025-09-06 |
| **Debug missing output in Python async HTTP flow** | Technical Screen | 2025-10-24 |
| **Design a data structure to store anagrams** | Technical Screen | 2026-02-12 |
| How would you model stock price prediction? | Technical Screen（口头） | 2026-02-12 |
| How do you explain work to non-technical partners? | HR Screen | 2026-02-12 |
| GCC/Clang/LLVM 优化 · C++ atomics/memory ordering · mutex 如何保护共享状态 | Technical Screen（SWE/Intern，C++） | 2026-04-26 |
| Explain a project and its hardest engineering challenge | Behavioral | 2026-04-26 |

PracHub OA 页（2026-08-13）："HackerRank invitations with **multi-file Python repository tasks**"、"two practical tasks: a backend-style implementation in a Python repository and a project task involving data or APIs"、链接 7 天有效、某任务约 20 min；可能另有 **Criteria** 能力测验。**"Your invitation is authoritative."**

### 4.2 StealthCoder（社区标签统计，7 题，无轮次/日期）**[中低]**

Best Time to Buy and Sell Stock（E）· Pow(x, n)（M）· Find the Smallest Divisor Given a Threshold（M）· Broken Calculator（M）· Partition Array Into Two Arrays to Minimize Sum Difference（H）· Valid Parentheses（E）· Palindromic Substrings（M）。"six of the seven are rated medium and one easy"（页面自述，与列表不符，取列表）。

### 4.3 QuantVault（OA 捕获，2022–2026；偏 QD/SDE OA）**[中]**

- SDE/QD OA：HackerRank，**约 6 题 / 3 h**（实习 4 题）：**Multi-Currency PnL**（持仓、本币价格、每日 FX、末日平仓）· Permutation divisible by 8 · **Spreadsheet column number ↔ notation** · **Intelligent Substring**（最长子串含 ≤ k 个"普通"字符）· Multi-label scene（300 维特征 → 6 个二元标签）。
- 旧实习集：IP-region 分类 · Subsegment Sort · Product Defect（LC 221 最大正方形）· Shape Classes（OOP）· Queued Seats。
- 面试题单（多为 quant）：Balanced Job Scheduling（最多任务放到快处理器，2024-09）· **LRU Cache** · **Median from a Data Stream** · Suffix max frequency for range queries（2022-03）· Assign next free integer seat（2022-10）。

### 4.4 TechPrep 2026 / InterviewQuery 2025 / Dataford / techinterview.org **[低-中]**

- TechPrep：流程 5–6 阶段、6–10 周；**Technical Virtual Screen 1–2 轮 × 45–60 min（Webex/Zoom）"one or two medium-difficulty coding problems" + 主语言深挖**；报道题：Trapping Rain Water、Container With Most Water、**Merge Intervals**、Subarray Sums Divisible by K；SD：signal evaluation、research data pipelines、real-time risk monitor；LLD：order book、rate limiter；语言：asyncio、multithreading vs multiprocessing、decorators、Pandas aggregations、SQL optimization；另提 **Caliper** 性格/认知测评。
- InterviewQuery：技术虚拟面 45–60 min，"programming languages, tech stacks used in Millennium, **ETL pipelines**, and possibly **SQL queries**"；"first round: live coding — given a scenario, code it in Python and SQL"；Python 题：**list vs tuple**、**memory management for long-running infrastructure processes**、debugging scenario、**thread-safe singleton**、optimize a script for large datasets。
- Glassdoor 摘要（SWE 页）："mostly basic algorithms/DS"；"no leetcode — in-depth dive into your resume"；场景题：**full-stack app crashes in production → how would you RCA**；"how to get to know large systems / know what is true in an unfamiliar system"；Python：list vs tuple、memory management。
- techinterview.org（2026-04）：SWE "standard DS&A; clean, LeetCode-style problems where interviewers watch your complexity analysis"；后续 "harder coding and systems design"。**数字（pod 数、5% rule）不引用。**
- getsmartresume（2026-01）：3–5 LC hard / 80–100% 通过率等数字**无来源且与一手矛盾，不采信**。

## 5. 汇总：第一轮 45 min 最可能出现的形态（按证据权重）

1. **一道"实用"编码题**（分组聚合 / 分页拉取 / 装饰器 / 数据结构设计 / 字符串大数），面试官边看边问语言机制 —— Blind 多帖 + LC Discuss + PracHub 三源一致。
2. **一道 LC medium**（双指针 / 前缀和 / 图 BFS / 区间） —— Blind "simple graph question"、LC Discuss R1/R2、StealthCoder、TechPrep。
3. **Python 内功口头题**穿插（asyncio、GIL、list vs tuple、内存、生成器、上下文管理器）—— LC Discuss、1p3a 1029420、InterviewQuery、Glassdoor。
4. **前 15 min 简历/项目**（"pick a project"、tech stack、设计取舍、DB 策略）—— LC Discuss Bangalore、Blind、1p3a 1090775。
5. **SQL 小题**可能性存在但低于以上（OA 里常见，电面报道少）。
