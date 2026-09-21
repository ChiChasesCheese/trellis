# 目录 — 按轮次读，按分数练

> 由 `python3 tools/contents.py` 从 `loop/tree/interview-loop.yaml` + `catalog/RANK.md` 生成，**勿手改**。
> 每个技能下的题按 28 法则分数（#refs × 时效 × 轮次权重）降序；**★ = cut line 以内**（累计 80% 流出次数）。
> 每题：题集目录（题面 + 测试 + 参考解）→ 题解文章（先做后读）。LeetCode 原题的公司标签全表见 `../../core/leetcode/companies/snowflake.md`。

## 00_recruiter · Recruiter / 邮件往来（LEaD 无单独 call）

先读：[03-reply-email](03-reply-email.md) · [fit](fit.md)

- **具体化的 why Millennium / why LEaD / why finance（Quant-Stroller 证据）** — 题库：`loop/rounds/00_recruiter/`
- **Miami onsite、年限口径、薪资不报数字** — 题库：`loop/rounds/00_recruiter/`

## 01_first_round · R1 45 min · SWE · Webex + HackerRank（15 简历 + 30 一题）

先读：[playbook](loop/rounds/01_first_round/playbook.md) · [python_internals](study/20-cards/python_internals.md)

通用能力（[[Code Core MOC|code-core]] 卡组与练习）：[[round.time]] · [[algorithms.recognition]] · [[verification.edge-catalog]] · [[performance.budget]]

### 实用数据任务：流式分组聚合、分块 + 并行、金额用 Decimal

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc10** SQL Drill — 分组聚合 → 窗口函数 → join+FX → gaps-and-islands → NOT IN 的 NULL 陷阱 | [`loop/rounds/01_first_round/pc10_sql_drill/`](loop/rounds/01_first_round/pc10_sql_drill/) | [题解](study/30-articles/pc10_sql_drill.md) | 4 | 未知 | MED-HIGH |
| ★ | **pc01** Grouped Aggregation — 单遍 dict 累加 → 分块聚合再合并 → 多键多聚合 | [`loop/rounds/01_first_round/pc01_grouped_aggregation/`](loop/rounds/01_first_round/pc01_grouped_aggregation/) | [题解](study/30-articles/pc01_grouped_aggregation.md) | 2 | 2025-12 | HIGH |

### Python 机制编码：asyncio 分页拉取、装饰器（retry / memoize / rate-limit）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc02** Async Paginated API Ingestion — 顺序翻页 → 并发限流保序 → 退避重试 + 幂等去重 | [`loop/rounds/01_first_round/pc02_async_paginated_ingestion/`](loop/rounds/01_first_round/pc02_async_paginated_ingestion/) | [题解](study/30-articles/pc02_async_paginated_ingestion.md) | 3 | 2025-12 | HIGH |
| ★ | **pc03** Decorators — retry / memoize / timing / rate-limit，从裸装饰器到带参数、带状态 | [`loop/rounds/01_first_round/pc03_decorators/`](loop/rounds/01_first_round/pc03_decorators/) | [题解](study/30-articles/pc03_decorators.md) | 3 | 2025-12 | HIGH |

### 数据结构设计：anagram 分组、LRU + TTL、中位数流、价格 as-of 存储

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc09** Price Data Store — upsert/latest/as-of → OHLC/VWAP → 多币种换算 | [`loop/rounds/01_first_round/pc09_price_data_store/`](loop/rounds/01_first_round/pc09_price_data_store/) | [题解](study/30-articles/pc09_price_data_store.md) | 3 | 2026-02 | HIGH |
| ★ | **pc07** Anagram Store：设计一个按 anagram 分组的存储结构 | [`loop/rounds/01_first_round/pc07_anagram_store/`](loop/rounds/01_first_round/pc07_anagram_store/) | [题解](study/30-articles/pc07_anagram_store.md) | 2 | 2026-02 | MED-HIGH |
|  | **pc08** LRU Cache + TTL + Median From Stream：两道经典设计题打包成一题 | [`loop/rounds/01_first_round/pc08_lru_ttl_median/`](loop/rounds/01_first_round/pc08_lru_ttl_median/) | [题解](study/30-articles/pc08_lru_ttl_median.md) | 1 | 未知 | MED |

### LC medium：前缀和取模、双指针盛水、字符串大数

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **pc05** Subarray Sums Divisible by K → 和恰为 K → 最长子数组 | [`loop/rounds/01_first_round/pc05_subarray_sums_div_k/`](loop/rounds/01_first_round/pc05_subarray_sums_div_k/) | [题解](study/30-articles/pc05_subarray_sums_div_k.md) | 2 | 2025-12 | HIGH |
| ★ | **pc06** Water Problems：Container With Most Water → Trapping Rain Water → 二维版 | [`loop/rounds/01_first_round/pc06_water_problems/`](loop/rounds/01_first_round/pc06_water_problems/) | [题解](study/30-articles/pc06_water_problems.md) | 2 | 2025-12 | HIGH |
|  | **pc04** Big-Integer String Arithmetic — 手写高精度加减乘（不用 `int()`） | [`loop/rounds/01_first_round/pc04_big_integer_strings/`](loop/rounds/01_first_round/pc04_big_integer_strings/) | [题解](study/30-articles/pc04_big_integer_strings.md) | 1 | 未知 | HIGH |

- **穿插口头题：GIL / asyncio / 内存 / list vs tuple / Java HashMap** — 题库：`loop/rounds/02_python_internals/`

## 02_python_internals · Python / Java 内功口头题（R1 穿插 · onsite 突袭）

先读：[python_internals](study/20-cards/python_internals.md) · [questions](loop/rounds/02_python_internals/questions.md)

- **线程 / 进程 / asyncio / GIL / race** — 题库：`loop/rounds/02_python_internals/`
- **装饰器 / 生成器 / 上下文管理器 / 内存 / 拷贝** — 题库：`loop/rounds/02_python_internals/`

## 03_project_deep_dive · 项目深挖（R1 前 15 min · 后续整轮）

先读：[questions](loop/rounds/03_project_deep_dive/questions.md) · [playbook](loop/rounds/01_first_round/playbook.md)

- **Quant-Stroller：headline → 三层机制 → 我决定 → 最难挑战 → 替代方案** — 题库：`loop/rounds/03_project_deep_dive/`
- **PayPal 生产系统：S1 管线 · S3/S9 事故 · S5 迁移** — 题库：`loop/rounds/03_project_deep_dive/`

## 04_system_design · 系统 / 数据设计（R2+，可能）

先读：[LOOP_GUIDE](loop/LOOP_GUIDE.md)

### 行情/价格数据服务：point-in-time、迟到修正、多币种、订阅推送

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd01** Market / Price Data Service（多经理对冲基金的行情数据服务） | [`loop/rounds/04_system_design/sd01_market_data_service/`](loop/rounds/04_system_design/sd01_market_data_service/) | [model_answer](loop/rounds/04_system_design/sd01_market_data_service/model_answer.md) | 2 | 2025-12 | MED |


## 05_hm_behavioral · HM / Behavioral（R2+）

先读：[questions](loop/rounds/05_hm_behavioral/questions.md) · [stories](loop/rounds/05_hm_behavioral/stories.md) · [fit](fit.md)

- **ownership · abstract reasoning · teamwork · feedback（官方四维 → S1–S11）** — 题库：`loop/rounds/05_hm_behavioral/`
- **why finance / why LEaD / pod 结构 / 非技术沟通** — 题库：`loop/rounds/05_hm_behavioral/`
