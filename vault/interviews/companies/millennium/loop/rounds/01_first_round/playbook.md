# R1 Playbook · 45 min · Webex + HackerRank · 面试官 = 一位 Millennium SWE

> 依据：`catalog/raw/inbox.md`（邀约原文）· `catalog/raw/coding_first_round.md` §5（题型权重）· `catalog/raw/process_and_rounds.md` §3（评什么）。一手同形态 = **15 min 背景 + 30 min 一题**（1p3a 1090775）。面试官几乎不给反馈、少一个括号没 debug 时间就挂——**自己推进、自己验证**。
> 练：`python3 loop/mock.py start pc02 -m 30`（30 min 计时，只做一题）；口头题 `python3 loop/mock.py bq py -n 5 -m 2`。

## 0. 前 24 小时清单

- HackerRank 环境：登录测试链接，切 **Python 3**，试跑 `print()`；确认能不能看到"Run tests"/自定义输入；关掉内置 AI 助手面板（面试官能看到你和 AI 的交互 —— 产品页原文；除非对方明说允许，不用）。
- Webex：摄像头、耳机、共享屏幕权限；副屏关闭（HackerRank 有 proctoring 迹象时以邀请说明为准）。
- 桌面只留：HackerRank、Webex、一张纸。**不开 IDE**。
- 复习卡：`study/20-cards/python_internals.md`、`study/20-cards/finance_vocab.md`；项目口播 §2 读三遍。

## 1. 时间线（45 min）

| 分钟 | 段 | 目标 | 我做什么 |
|---|---|---|---|
| 0–2 | 寒暄 | 能听清、能被听清 | "Hi <name>, thanks for taking the time." 一句，不多 |
| 2–5 | 自我介绍 | **headline first**（Chakra 复盘教训：无 headline、每答 > 90 s 是丢分点） | §2.1（60–75 s） |
| 5–15 | 简历 / 项目 | 一个项目讲到第三层（why · alternatives · failure modes）；把 JD 词说出口 | §2.2 首选 Quant-Stroller，备选 [[S1]]/[[S5]] |
| 15–17 | 题目 | 复述 + 确认输入输出/规模/语言 | §3.1 |
| 17–20 | 方案 | 先讲方案 + 复杂度，再动手 | §3.2 |
| 20–35 | 写代码 | 函数化、命名清楚、边写边说 | §3.3 |
| 35–40 | 自测 | **自己走样例 + 至少两个边界**；写完自己念一遍括号/缩进 | §3.4 |
| 40–43 | 追问 | 复杂度、并发/规模化、"如果数据是 10 亿行" | §3.5 |
| 43–45 | 反问 | 2 个问题（`../../../06-questions-to-ask.md` §A） | |

若对方先出题再聊简历（Blind："30 of 45 on resume" 也有反例），顺序换，内容不变。

## 2. 口播（English）

### 2.1 自我介绍（60–75 s）

> I'm a backend engineer at PayPal, about a year and a half full-time plus a summer internship there before that, all on Braintree's payments platform. I own the American Express settlement and fee pipeline end to end — it runs natively on Snowflake and PostgreSQL, processes hundreds of millions of dollars a year, and I'm the on-call authority for it. Outside work I built a quantitative research and backtesting platform in Python — about 66 thousand lines, DuckDB and Parquet for the data plane, purged cross-validation and deflated Sharpe as the anti-overfitting gates, and a FastAPI/React research console. That's what pulled me toward finance technology, and it's why the LEaD program is the role I actually want: rotating across front, middle and back office technology with mentors, rather than one narrow seat.

中文注释：三个 JD 词已埋入 —— **Python / FastAPI / backend distributed** + **data pipeline** + **finance**。不说 $600B（诚实红线：说 hundreds of millions 或 "billions in volume"——[[S1]] 口径表）。

### 2.2 项目首选：Quant-Stroller（对齐 Steve Johnson "build and back test a simple trading strategy in Python"）

**Headline（15 s）**
> The project I'd pick is Quant-Stroller, a multi-market research and backtesting platform I built this year — US equities, crypto, China A-shares and FX — whose whole point is to make it hard to fool yourself with a backtest.

**Mechanism（60 s）**
> Three layers. A point-in-time data plane: raw vendor files → bars → a panel, on DuckDB and Parquet, with a factor catalog of about 2,300 factors across nine vendors, and every join is as-of so there's no look-ahead. A strategy layer with narrow seams — DataSource, Factor, Strategy, Broker — so a new market or vendor is a thin adapter and strategy code doesn't change. And a validation gate: purged cross-validation, the deflated Sharpe ratio and probability of backtest overfitting, then an execution replay on NautilusTrader with calibrated per-market transaction-cost models. Every experiment goes to an append-only ledger — around 340 so far.

**Decision I made（30 s）**
> The decision I'd defend is the dual gate. Most hobby backtesters stop at "Sharpe looks good". I made a strategy pass a statistical gate and an execution gate before it can touch the paper-trading loop. One China small-cap monthly strategy passed both — excess Sharpe about 1.4 net of 10 basis points — and it's running in a paper loop with pre-trade risk checks and a five-factor risk report.

**Hardest challenge（30 s；PracHub 2026-04 原题）**
> The hardest engineering problem was the point-in-time panel: a 5,500-stock A-share universe with survivorship and restatement issues. I solved it with an as-of join over vendor snapshot dates instead of "latest value", and a validation that replays a random date and checks nothing from the future leaked in.

**Alternatives（追问时）** DuckDB vs Postgres（列存 + 本地 Parquet 扫描比行存快一个量级，且零运维）；NautilusTrader vs 自写撮合（要的是成交与滑点模型，不是重写引擎）；为什么不用 pandas 全内存（面板太大，DuckDB 下推谓词）。

**诚实边界**：不是生产资金；paper trading；A 股数据源是商用/公开混合；"66K 行"含测试。

### 2.3 项目备选：[[S1]] Amex 结算管线（若对方更想听生产系统）

用 [[S1]] §5 英文首答（90 s）。JD 对应词：backend distributed system、data pipeline、messaging（Streams/Tasks 是事件驱动）、relational DB、on-call。追问三层在 [[S1]] §2 表格。

### 2.4 被问 "why finance / why Millennium / why LEaD"（30 s）

`../../../fit.md` §1–§2。

## 3. 编码段打法

### 3.1 复述与确认（2 min）
> "Let me make sure I have it: input is …, output is …, and I should assume … Is that right? Any constraints on size — thousands of rows, or millions? Python is fine?"
写下 1–2 个样例（自己造，含空输入）。

### 3.2 先讲方案（3 min）
> "I'll do X with a dict keyed by …, one pass, O(n) time and O(k) memory. Then I'll handle … as edge cases. Sound good?"
面试官不回应也继续（一手："minimal feedback"）。

### 3.3 写（15 min）
- 函数签名 + docstring 一行 → 主逻辑 → 边界。**不写 `main()` 读 stdin 除非题目要求**。
- 边写边说每个决定："I'm using `defaultdict(int)` so I don't branch on first-seen keys."
- 用 `Decimal`/整数处理金额；排序写全 tie-break。
- **每 5 分钟看一眼括号与缩进**（一手挂点）。

### 3.4 自测（5 min）
> "Let me trace the example: … Now the empty case … Now a duplicate key …"
真的跑：在 HackerRank 里加 `print(f(...))` 跑一遍；跑完删掉调试输出。

### 3.5 追问的标准答法（每题 20–30 s）
- 复杂度：时间/空间各一句 + 瓶颈在哪。
- "millions of rows"：流式/分块（`csv` 迭代器、`chunksize`）、多进程（CPU-bound 绕过 GIL）vs 线程（I/O-bound）、或者直接说 "at that size I'd push it into DuckDB/SQL and let the engine do the group-by"。
- 并发/多线程：说锁在哪、无共享状态更好、`concurrent.futures` 接口。
- 持久化/生产：幂等、重试、可观测（Datadog 是我在 PayPal 的日常）。

## 4. 题型 → 题库映射（练习顺序 = PARETO 顺序）

| 若题目像… | 直接套 | 30 min 内目标 |
|---|---|---|
| 分页 API / async | pc02 | Part 1 + Part 2 |
| 装饰器 / retry / cache | pc03 | Part 1 + Part 2 |
| 价格/行情数据结构 | pc09 | Part 1 |
| SQL | pc10 | Part 1–3 |
| CSV/DataFrame 聚合 | pc01 | Part 1 + Part 2 口头 |
| 前缀和 / 子数组 | pc05 | Part 1 + Part 2 |
| 双指针 / 数组 | pc06 | Part 1 + Part 2 |
| 字符串分组 / 括号 | pc07 | 热身 + Part 1 |
| 大数字符串 | pc04 | Part 1 + Part 2 |
| LRU / 中位数 | pc08 | Part 1 或 Part 3 |
| 图 BFS | Snowflake `pc02` / `pc04`（`../../../../snowflake/loop/rounds/03_phone_coding/`） | 一题 |
| 区间合并 | LC 56 原题 | 15 min |

## 5. 红线

- 不用内置 AI；不切窗口查资料除非对方说可以（一手：R3 面试官允许查语法——**问一句** "Mind if I look up the exact signature?"）。
- 不说 $600B、#1 committer、"no bugs"（[[Core]] 诚实红线）。
- 不报薪资数字；不说在面别家的进度。
- 不贬低 PayPal；"why leave" 用 `fit.md` §3。
