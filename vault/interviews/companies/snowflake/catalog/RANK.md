# RANK — 全部技术题一张表（28 法则打分的输入）

> 由 `CATALOG.md` Table A/B/C 汇总；只保留打分需要的列。跑：
> `python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "OA,电面,PS"`
> `#refs` = 独立来源数（同一候选人跨站 1；聚合站互抄 1；同一题的 base+follow-up 1）。`最近` = 最近一次被报道（PracHub 的 Last Updated 只作下限）。

## 总表

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---:|---|
| pc01 | RBAC / DAG 权限继承题族（Effective Access Control · Role Privileges · Local-only Deny · Allow/Deny in DAG · Letter Permissions） | 电面 PS | 2026-09 | 5 | MED-HIGH |
| q02 | 元音游程 DP 题族（consecutive-vowel count · String Patterns `calculateWays` · Vowel Substring LC 1987/2062） | OA | 2026-06 | 5 | MED-HIGH |
| sd01 | KV store（分布式：versioning / time-travel snapshot / Raft / range scan） | SD 电面+onsite | 2026-09 | 5 | HIGH-MED |
| od02 | In-Memory File System（LC 588 + rm/chunk/线程安全/WAL 追问） | 电面 PS | 2026-08 | 4 | HIGH-MED |
| sd02 | Cron / Job Scheduler（含 "SQL engine running many queries as cron job"、Reliable Job Scheduler、Service Startup Scheduler） | SD 电面+onsite | 2026-07 | 4 | HIGH |
| q01 | Task Scheduling — paid vs free server（0/1 背包式调度） | OA | 2026-03 | 3 | HIGH |
| q03 | 树高压缩题族（Minimum Height 换根 · Minimum N-ary Deletions · Prune Multiway Tree） | OA+电面 PS | 2026-08 | 3 | MED-HIGH |
| od01 | Task Scheduler `addTask(id,priority,ts)` / `executeTask()`（+ 重复 ID 抑制 + 并发） | onsite | 2026-08 | 3 | HIGH |
| pc03 | Recent Event Stream Queries（最近 m 条事件：count 去重 / top 最频 key）+ 1p3a "Event Stream Problem" | 电面 PS | 2026-08 | 3 | MED |
| pc10 | Distributed Tree Counting 状态机（消息传递 fan-out/fan-in） | 电面 PS | 2026-07 | 3 | MED |
| sd03 | SQL Notebook / 查询结果分发（submit→poll→fetch，大结果集流式） | SD 电面 | 2026-08 | 3 | HIGH |
| sd04 | Quota System（多上游服务共用，强一致 vs 本地缓存） | SD | 2026-06 | 3 | MED |
| sd06 | Audit / Query-Event Log Service（"pg_stat for Snowflake"，多租户、防篡改） | SD 电面+onsite | 2026-06 | 3 | MED-HIGH |
| sd07 | Distributed Rate Limiter（per-second，防 hot-spot / thundering herd） | SD | 2026-09 | 3 | MED |
| sd10 | Concurrent Web Crawler（BFS + 去重 + 扩展） | SD/编码 | 2026-03 | 3 | LOW-MED |
| od08 | LRU Cache（warehouse SSD cache 框架 + TTL 追问） | onsite | 2026 | 3 | LOW-MED |
| q04 | Maximum Order Volume / phone calls（加权区间调度，LC 1235 型） | OA | 2025-03 | 3 | MED |
| pc02 | Closest Bathroom / Desk on a Grid（多源 BFS） | 电面 PS | 2026-09 | 2 | MED-HIGH |
| pc04 | Web Crawler Shortest Path Reconstruction | 电面 PS | 2026-09 | 2 | MED |
| od04 | Rate Limiter（onsite 滑窗单规则 + 电面多规则排队线程安全） | onsite+电面 | 2026-08 | 2 | MED |
| od05 | Cron Scheduler 类：schedule / pause / resume / tick（多实例不重复触发） | 技术筛 | 2026-06 | 2 | LOW-MED |
| od09 | Queue 类（类 deque）→ 扩展为云端 queue service（故障语义） | onsite | 2026-08 | 2 | HIGH |
| sd05 | Distributed Queue Service（enqueue/dequeue 故障行为、at-least-once、背压） | SD onsite | 2026-08 | 2 | HIGH |
| sd08 | DAG Cache for Query Views / Materialized Views（≈ Dynamic Tables） | SD | 2026-03 | 2 | LOW-MED |
| sd11 | Automated Jira-Ticket-to-PR System（异步任务、队列架构；一手印证） | SD onsite | 2026-06 | 2 | MED-HIGH |
| sd12 | Object Store with Deduplication（Blob 去重） | SD | 2025-12 | 2 | LOW |
| q05 | Paint the Ceiling（递推生成边长，计数 area ≤ a 的对） | OA | 2026-03 | 2 | MED |
| q06 | Patching Array（LC 484 原题；2019 电面也考） | OA+电面 | 2023-02 | 2 | HIGH |
| q07 | Binary Tree Inorder Traversal（LC 94 + Morris 追问） | OA+电面 | 2023-02 | 2 | MED-HIGH |
| q08 | Course Schedule II（LC 210 原题；电面拓扑排序同族） | OA+电面 | 2023-02 | 2 | MED-HIGH |
| q09 | Server Selection（m 服务器 × n 任务 2D DP，目标 O(m·n)） | OA | 2023-02 | 2 | MED |
| q10 | Minimum Clicks Between Wiki Pages（图 BFS；OA 与电面池都有） | OA+电面 | 2026-09 | 1 | MED |
| pc05 | LC 1751 Maximum Number of Events That Can Be Attended II 变体 + follow-up | 电面 PS | 2026-06 | 1 | HIGH |
| pc06 | Happy Number：O(n) → O(1)（Floyd 判环）；前 20 min 讲项目 | 电面/onsite | 2026-07 | 1 | HIGH |
| pc07 | Word Search II（LC 212）+ 审计日志设计（senior 电面二合一） | 电面 PS | 2024-02 | 1 | HIGH |
| pc08 | Array-diff removal + Inorder（Morris）+ Patching Array（2019 两轮电面三题） | 电面 PS | 2019-11 | 1 | HIGH |
| pc09 | Parallel Courses III（LC 2050 原题） | onsite | 2026-08 | 1 | MED-HIGH |
| od03 | Transactional in-memory KV store（嵌套事务 begin/commit/rollback + 线程线性一致追问） | 技术筛 | 2026-08 | 1 | HIGH-MED |
| od06 | Query Audit Log 类（record_access / accessed_in_range / unaccessed_since） | 电面 PS | 2024-02 | 1 | HIGH |
| od07 | Throne Inheritance without initial king（LC 1600 变体） | 电面 PS | 2026 | 1 | MED |
| sd09 | User Password Storage 系统设计 | SD 电面/onsite | 2026-07 | 1 | HIGH |
| sd13 | ACL Authorization Checking Service | SD | 2026-01 | 1 | LOW |
| sd14 | Distributed Metadata Catalog / Schema Registry | SD | 2025-09 | 1 | LOW |
| sd15 | Multi-Tenant Interactive Analytics Platform（摄取+查询端到端） | SD | 2025-09 | 1 | LOW |
| sd16 | Resilient Auth with Flaky Third-Party Tokens | SD | 2025-09 | 1 | LOW |
| sd17 | Geolocation Search Service | SD | 2026-07 | 1 | LOW |
| sd18 | Event Subscription System（1M/s 通知） | SD | 2026 | 1 | LOW |
| sd19 | REST API Abstraction Layer / Internal Service-Client SDK | SD | 2026-04 | 1 | LOW |
| sd20 | Dynamic Blacklist Filter System（仅 1p3a 标题） | SD | 2026 | 1 | LOW-MED |
| q11 | Generating Login Codes（New Grad OA，仅标题+标签） | OA | 2026-09 | 1 | MED |
| q12 | Merge Intervals（LC 56 原题） | OA | 2023-02 | 1 | MED |
| q13 | Minimum Interval to Include Each Query（LC 1851 原题） | OA | 2023-02 | 1 | MED |
| q14 | Palindromic Subsequences（LC 2002 原题） | OA | 2023-02 | 1 | MED |
| q15 | Graph Valid Tree（LC 261 原题） | OA | 2023-02 | 1 | MED |
| q16 | String Formation via dictionary（LC 1639 原题） | OA | 2023-02 | 1 | MED |
| q17 | Remove Stones to Minimize the Total（LC 1962 原题） | OA | 2024-12 | 1 | MED |
| q18 | Min-Height-Trees 图变体（LC 310 + twist） | OA | 2026 | 1 | LOW-MED |
| pc11 | Character Frequencies（跨字符串 / 嵌套列表） | 电面 PS | 2026-06 | 1 | MED |
| pc12 | Top Two Users by Total Purchase Amount | 电面 PS | 2026-06 | 1 | MED |
| pc13 | Service Startup / Dependency Ordering（Kahn） | 电面 PS | 2026-03 | 1 | LOW-MED |
| pc14 | Meeting Rooms II（LC 253 型，2026 实习 VO） | onsite | 2026 | 1 | LOW |
| pc15 | Parentheses Matching（栈） | 电面 PS | 2026-03 | 1 | LOW |
| pc16 | Reverse Alphanumeric Segments（1p3a 标题） | 电面 PS | 2026 | 1 | LOW-MED |
| q19 | Maximize OR-Sum（AIML 实习 OA 一手） | OA | 2026-05 | 2 | MED-HIGH |
| od10 | Student / Result OOP（OA 内嵌） | OA | 2026-05 | 2 | MED |
| sd22 | PB 级数据库间同步（IC2 一手，不许澄清需求） | SD 电面+onsite | 2026-03 | 1 | HIGH |
