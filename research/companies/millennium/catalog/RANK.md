# RANK — 全部技术题一张表（28 法则打分的输入）

> 由 `CATALOG.md` Table A/B 汇总；只保留打分需要的列。跑：
> `python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "第一轮"`
> `#refs` = 独立来源数（同一候选人跨站 1；聚合站互抄 1；同一帖的 base + follow-up 1）。`最近` = 最近一次被报道；"未知"= 只有 1p3a thread id 或聚合站无日期。

## 总表

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---:|---|
| pc01 | Grouped aggregation over millions of rows（分块 + 多线程/多进程） | 第一轮 | 2025-12 | 2 | HIGH |
| pc02 | Async paginated API ingestion（asyncio、并发上限、重试） | 第一轮 | 2025-12 | 3 | HIGH |
| pc03 | Decorators（timing / memoize / retry / rate-limit） | 第一轮 | 2025-12 | 3 | HIGH |
| pc04 | Big-integer string arithmetic | 第一轮 | 未知 | 1 | HIGH |
| pc05 | Subarray sums divisible by K（LC 974 / 560 / 最长） | 第一轮 | 2025-12 | 2 | HIGH |
| pc06 | Water problems（LC 11 + LC 42） | 第一轮 | 2025-12 | 2 | HIGH |
| pc07 | Anagram store（+ Valid Parentheses 热身） | 第一轮 | 2026-02 | 2 | MED-HIGH |
| pc08 | LRU cache with TTL + Median from stream | 第一轮 | 未知 | 1 | MED |
| pc09 | Price data store（as-of、OHLC/VWAP、多币种） | 第一轮 | 2026-02 | 3 | HIGH |
| pc10 | SQL drill（sqlite3 五题） | 第一轮 | 未知 | 4 | MED-HIGH |
| pc11 | Merge Intervals（LC 56，未建） | 第一轮 | 2026-01 | 1 | LOW-MED |
| pc12 | Simple graph question（BFS/DFS，未建） | 第一轮 | 未知 | 1 | MED |
| sd01 | Market / price data service | 后续 SD | 2025-12 | 2 | MED |
| sd02 | Rate limiter / order book（LLD） | 后续 SD | 2026-01 | 1 | LOW-MED |
| sd03 | Production crash RCA / unfamiliar-system 场景（口头） | 后续 | 2026-01 | 1 | MED |
