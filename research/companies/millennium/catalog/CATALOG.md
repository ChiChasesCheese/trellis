# Millennium 面试题目总表（LEaD Program · Software Engineer · Miami）

**日期：** 2026-09-21 · **输入：** `catalog/raw/{inbox,official_lead,github_repos,coding_first_round,process_and_rounds,interviewer,sources_index}.md`
**排序：** `RANK.md` → `tools/pareto.py` → `PARETO.md`。**当前轮次 = 第一轮 45 min（Webex + HackerRank，一位 SWE）**，`--focus` 权重给"第一轮"。
**口径：** `#refs` = 独立来源数（同一候选人跨站 1；聚合站互抄 1；同一帖里的 base + follow-up 1）。**LEaD 专属题目一手报道 = 0**，全部行来自 Millennium SWE / QD-Python 岗位，按"与 45 min 单人 HackerRank 实时编码的相关度"入表。

## 格式事实（细节与 URL 在 raw/）

- **LEaD 漏斗（推断）**：简历筛（批处理拒信）→ **R1 45 min SWE：~15 min 简历/项目 + ~30 min 一题 live coding** → 2–3 轮更多人（HM / tech leader；Miami 2026-02 一例"全 behavioral"）→ 决定。无 OA、无 Caliper 提及。投递到 R1 邀约 38 天。
- **通用 SWE 流程**（类推）：HackerRank OA（75 min/2 题 ~ 3 h/6 题，形态含 repo 任务）→ HM call → 技术筛 45–60 min（"15 + 30"）→ 第二轮三场 45 min 技术（HackerRank）→ virtual onsite ~5 人 → skip-level → offer。
- **题风**：三源一致"实用、贴工作、不是 LC 式"（Blind ×3、PracHub、LC Discuss R3/R5）；同时一手也有 LC 42/11/974、"简单图题"。**两手准备。**
- **语言**：不限；Python 为主；Java 基础口答（HashMap 冲突处理是一手电面题）。面试官允许查语法的一手案例 ×1；少写括号没给 debug 时间就挂的一手案例 ×1。
- **评分**：官方四条（abstract reasoning/creativity · ownership/initiative · teamwork · talk through code live）；"面试官几乎不给反馈"→ 自己推进：复述 → 方案 → 复杂度 → 写 → 自测样例 → 边界。

## Table A · 第一轮编码题（`loop/rounds/01_first_round/`，`pc`）

| ID | 题（别名） | 形态 | 最近 | #refs | 置信度 | 来源 |
|---|---|---|---|---:|---|---|
| pc01 | Grouped aggregation over millions of rows（CSV/DataFrame group-by sum，分块 + 多线程/多进程） | 实用编码 + Python 机制追问 | 2025-12 | 2 | HIGH | LC Discuss 7423863 R3（一手）· InterviewQuery "optimize a script for large datasets" |
| pc02 | Async paginated API ingestion（asyncio 翻页拉取、并发上限、重试；"debug missing output in async HTTP flow"） | 实用编码 | 2025-12 | 3 | HIGH | PracHub 2025-09-06 / 2025-10-24 · LC 7423863 R2（asyncio）· 1p3a 1124751（异步追问） |
| pc03 | Decorators（timing / memoize / retry / rate-limit，`functools.wraps`） | Python 内功编码 | 2025-12 | 3 | HIGH | LC 7423863 R5（一手）· 1p3a 1079245（OA）· TechPrep/InterviewQuery |
| pc04 | Big-integer string arithmetic（字符串大数加 → 减/乘/进制） | LC-style 一题 30 min | 未知（thread 1090775） | 1 | HIGH | 1p3a 1090775（C++ dev 45 min 电面：15 背景 + 30 编码） |
| pc05 | Subarray sums divisible by K（LC 974 → LC 560 → 最长子数组） | LC medium | 2025-12 | 2 | HIGH | LC 7423863 R2（一手）· TechPrep |
| pc06 | Water problems（Container With Most Water LC 11 + Trapping Rain Water LC 42） | LC medium ×2 一轮 | 2025-12 | 2 | HIGH | LC 7423863 R1（一手）· TechPrep |
| pc07 | Anagram store（按 anagram 分组的数据结构；热身 Valid Parentheses） | 数据结构设计 | 2026-02 | 2 | MED-HIGH | PracHub 2026-02-12 · StealthCoder（Valid Parentheses、Palindromic Substrings） |
| pc08 | LRU cache with TTL + Median from data stream | 经典设计 | 未知 | 1 | MED | QuantVault 题单（未标轮次） |
| pc09 | Price data store（写入/最新价/as-of/区间聚合；多币种换算） | LLD 编码 | 2026-02 | 3 | HIGH | LC 7423863 R5 "price data design"（一手）· PracHub 2026-02-12 "model stock price prediction" · QuantVault OA "multi-currency PnL" |
| pc10 | SQL drill（sqlite3：分组、窗口、join+FX、gaps-and-islands、NULL 陷阱） | SQL 小题 | 未知（threads 1079245/855488/939377） | 4 | MED-HIGH | 1p3a 1079245 · 855488 · 939377 · Blind "Python+SQL, speed" |
| pc11 | Merge Intervals（LC 56）—— **未建**，LC 原题直接刷 | LC medium | 2026 | 1 | LOW-MED | TechPrep |
| pc12 | "A simple graph question"（BFS/DFS，LC medium）—— **未建**，用 `code-core` 图遍历叶 + Snowflake pc02/pc04 | LC medium | 未知 | 1 | MED | Blind ghkhxn3o |

## Table B · 设计题（`loop/rounds/04_system_design/`，`sd`；后续轮）

| ID | 题 | 最近 | #refs | 置信度 | 来源 |
|---|---|---|---|---|---|
| sd01 | Market / price data service（采集 → 存储 → as-of 查询 → 下游订阅；对应 pc09 的系统版） | 2025-12 | 2 | MED | LC 7423863 R5 · TechPrep "research data pipelines / real-time risk monitor" |
| sd02 | Rate limiter / order book（LLD） | 2026 | 1 | LOW-MED | TechPrep；Snowflake kit `od04` 可直接复用 |
| sd03 | "Full-stack app crashes in production — how do you RCA" · "how do you know what's true in an unfamiliar system"（口头场景） | 2026 | 1 | MED | Glassdoor SWE 摘要 |

## Table C · 口头技术题（`loop/rounds/02_python_internals/bank.json`，`py`）

| 主题 | 一手/聚合 | 来源 |
|---|---|---|
| asyncio：coroutine vs thread、event loop、漏 `await`、`gather`/`Semaphore` | 一手 | LC 7423863 R2；PracHub 2025-10；1p3a 1124751 |
| multithreading vs multiprocessing、GIL、什么时候用哪个 | 一手 | LC 7423863 R3；TechPrep |
| decorators / generators / context managers | 一手 | LC 7423863；1p3a 1079245 |
| list vs tuple；Python 长驻进程的内存管理；thread-safe singleton | 聚合 | InterviewQuery；Glassdoor 摘要 |
| Python 基础"突袭"（onsite 开场） | 一手 | 1p3a 1029420 |
| Java：HashMap/HashSet 冲突处理，Java 8+ 树化 | 一手 | 1p3a 660546 |
| "favorite data structure and its trade-offs" | 一手（QR） | devclub-iitd |
| pandas：chunking、groupby、内存 | 一手 | LC 7423863 R3 |
| C++（若声称）：atomics/memory ordering、mutex、编译器优化 | 聚合 | PracHub 2026-04（intern） |

## Table D · 非编码题库

| 轮 | 目录 | 题数 | 来源 |
|---|---|---|---|
| Recruiter / 排期回复 | `loop/rounds/00_recruiter/` | 8 | TechPrep（why finance、pod 结构、薪资预期）· 1p3a 1078136 |
| 项目深挖（R1 前 15 min + 后续轮） | `loop/rounds/03_project_deep_dive/` | 14 | LC 6020524（objective/approach/stack/design/challenges/DB）· PracHub "hardest engineering challenge" · Blind "30 of 45 min on resume" |
| HM / behavioral | `loop/rounds/05_hm_behavioral/` | 12 | 官方 4 条 · PracHub "explain work to non-technical partners" · TechPrep（pressure、tech debt、incidents）· 1p3a 1158922（autonomy/accountability） |

## Table E · 不入库（原因）

- getsmartresume 的"3–5 LC hard / 80–100% 通过率 / 60–80 h 周"——无来源，与一手矛盾。
- techinterview.org 的 pod 数、"5% rule"——SEO folklore。
- QuantVault 的概率/期权/统计题——QR/QT 岗，LEaD SWE 不考；只保留 LRU/Median/OA 编码题。
- Angular/前端题（1p3a 1149521）——LEaD 不是前端岗。
