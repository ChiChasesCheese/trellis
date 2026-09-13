# PARETO — 28 法则排序输出（2026-09-13）

> 命令：`python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "OA,电面,PS,技术筛" --title-col 题`
> 规则：score = #refs × 时效（≤3 月 1.0 / ≤12 月 0.8 / ≤24 月 0.6 / 更早 0.4）× 轮次权重（要面的轮次 1.0 / 其它技术轮 0.8 / 非编码轮 0.6）；cut line = 累计 80%。

| # | 题 | 轮次 | #refs | 最近 | score | 累计 |
|---|---|---|---:|---|---:|---:|
| 1 | RBAC / DAG 权限继承题族（Effective Access Control · Role Privileges | 电面 PS | 5 | 2026-09 | 5.00 | 5% |
| 2 | 元音游程 DP 题族（consecutive-vowel count · String Patterns `calcul | OA | 5 | 2026-06 | 5.00 | 11% |
| 3 | KV store（分布式：versioning / time-travel snapshot / Raft / rang | SD 电面+onsite | 5 | 2026-09 | 5.00 | 16% |
| 4 | In-Memory File System（LC 588 + rm/chunk/线程安全/WAL 追问） | 电面 PS | 4 | 2026-08 | 4.00 | 20% |
| 5 | Cron / Job Scheduler（含 "SQL engine running many queries as c | SD 电面+onsite | 4 | 2026-07 | 4.00 | 25% |
| 6 | 树高压缩题族（Minimum Height 换根 · Minimum N-ary Deletions · Prune M | OA+电面 PS | 3 | 2026-08 | 3.00 | 28% |
| 7 | Recent Event Stream Queries（最近 m 条事件：count 去重 / top 最频 key）+ | 电面 PS | 3 | 2026-08 | 3.00 | 31% |
| 8 | Distributed Tree Counting 状态机（消息传递 fan-out/fan-in） | 电面 PS | 3 | 2026-07 | 3.00 | 34% |
| 9 | SQL Notebook / 查询结果分发（submit→poll→fetch，大结果集流式） | SD 电面 | 3 | 2026-08 | 3.00 | 37% |
| 10 | Audit / Query-Event Log Service（"pg_stat for Snowflake"，多租户、 | SD 电面+onsite | 3 | 2026-06 | 3.00 | 41% |
| 11 | Task Scheduling — paid vs free server（0/1 背包式调度） | OA | 3 | 2026-03 | 2.40 | 43% |
| 12 | Task Scheduler `addTask(id,priority,ts)` / `executeTask()`（+ | onsite | 3 | 2026-08 | 2.40 | 46% |
| 13 | Quota System（多上游服务共用，强一致 vs 本地缓存） | SD | 3 | 2026-06 | 2.40 | 48% |
| 14 | Distributed Rate Limiter（per-second，防 hot-spot / thundering  | SD | 3 | 2026-09 | 2.40 | 51% |
| 15 | Closest Bathroom / Desk on a Grid（多源 BFS） | 电面 PS | 2 | 2026-09 | 2.00 | 53% |
| 16 | Web Crawler Shortest Path Reconstruction | 电面 PS | 2 | 2026-09 | 2.00 | 55% |
| 17 | Rate Limiter（onsite 滑窗单规则 + 电面多规则排队线程安全） | onsite+电面 | 2 | 2026-08 | 2.00 | 57% |
| 18 | Cron Scheduler 类：schedule / pause / resume / tick（多实例不重复触发） | 技术筛 | 2 | 2026-06 | 2.00 | 59% |
| 19 | Concurrent Web Crawler（BFS + 去重 + 扩展） | SD/编码 | 3 | 2026-03 | 1.92 | 61% |
| 20 | Maximum Order Volume / phone calls（加权区间调度，LC 1235 型） | OA | 3 | 2025-03 | 1.80 | 63% |
| 21 | Queue 类（类 deque）→ 扩展为云端 queue service（故障语义） | onsite | 2 | 2026-08 | 1.60 | 65% |
| 22 | Distributed Queue Service（enqueue/dequeue 故障行为、at-least-once | SD onsite | 2 | 2026-08 | 1.60 | 67% |
| 23 | Automated Jira-Ticket-to-PR System（异步任务、队列架构；一手印证） | SD onsite | 2 | 2026-06 | 1.60 | 69% |
| 24 | Paint the Ceiling（递推生成边长，计数 area ≤ a 的对） | OA | 2 | 2026-03 | 1.60 | 70% |
| 25 | DAG Cache for Query Views / Materialized Views（≈ Dynamic Tab | SD | 2 | 2026-03 | 1.28 | 72% |
| 26 | Object Store with Deduplication（Blob 去重） | SD | 2 | 2025-12 | 1.28 | 73% |
| 27 | LRU Cache（warehouse SSD cache 框架 + TTL 追问） | onsite | 3 | 2026 | 1.20 | 74% |
| 28 | Minimum Clicks Between Wiki Pages（图 BFS；OA 与电面池都有） | OA+电面 | 1 | 2026-09 | 1.00 | 75% |
| 29 | LC 1751 Maximum Number of Events That Can Be Attended II 变体  | 电面 PS | 1 | 2026-06 | 1.00 | 76% |
| 30 | Happy Number：O(n) → O(1)（Floyd 判环）；前 20 min 讲项目 | 电面/onsite | 1 | 2026-07 | 1.00 | 77% |
| 31 | Transactional in-memory KV store（嵌套事务 begin/commit/rollback  | 技术筛 | 1 | 2026-08 | 1.00 | 79% |
| 32 | User Password Storage 系统设计 | SD 电面/onsite | 1 | 2026-07 | 1.00 | 80% |
| 33 | Generating Login Codes（New Grad OA，仅标题+标签） | OA | 1 | 2026-09 | 1.00 | 81% |
| 34 | Character Frequencies（跨字符串 / 嵌套列表） | 电面 PS | 1 | 2026-06 | 1.00 | 82% |
| 35 | Top Two Users by Total Purchase Amount | 电面 PS | 1 | 2026-06 | 1.00 | 83% |
| 36 | Patching Array（LC 484 原题；2019 电面也考） | OA+电面 | 2 | 2023-02 | 0.80 | 84% |
| 37 | Binary Tree Inorder Traversal（LC 94 + Morris 追问） | OA+电面 | 2 | 2023-02 | 0.80 | 85% |
| 38 | Course Schedule II（LC 210 原题；电面拓扑排序同族） | OA+电面 | 2 | 2023-02 | 0.80 | 85% |
| 39 | Server Selection（m 服务器 × n 任务 2D DP，目标 O(m·n)） | OA | 2 | 2023-02 | 0.80 | 86% |
| 40 | Parallel Courses III（LC 2050 原题） | onsite | 1 | 2026-08 | 0.80 | 87% |
| 41 | Geolocation Search Service | SD | 1 | 2026-07 | 0.80 | 88% |
| 42 | Service Startup / Dependency Ordering（Kahn） | 电面 PS | 1 | 2026-03 | 0.80 | 89% |
| 43 | Parentheses Matching（栈） | 电面 PS | 1 | 2026-03 | 0.80 | 90% |
| 44 | ACL Authorization Checking Service | SD | 1 | 2026-01 | 0.64 | 90% |
| 45 | Distributed Metadata Catalog / Schema Registry | SD | 1 | 2025-09 | 0.64 | 91% |
| 46 | Multi-Tenant Interactive Analytics Platform（摄取+查询端到端） | SD | 1 | 2025-09 | 0.64 | 92% |
| 47 | Resilient Auth with Flaky Third-Party Tokens | SD | 1 | 2025-09 | 0.64 | 92% |
| 48 | REST API Abstraction Layer / Internal Service-Client SDK | SD | 1 | 2026-04 | 0.64 | 93% |
| 49 | Remove Stones to Minimize the Total（LC 1962 原题） | OA | 1 | 2024-12 | 0.60 | 94% |
| 50 | Throne Inheritance without initial king（LC 1600 变体） | 电面 PS | 1 | 2026 | 0.50 | 94% |
| 51 | Min-Height-Trees 图变体（LC 310 + twist） | OA | 1 | 2026 | 0.50 | 95% |
| 52 | Reverse Alphanumeric Segments（1p3a 标题） | 电面 PS | 1 | 2026 | 0.50 | 95% |
| 53 | Word Search II（LC 212）+ 审计日志设计（senior 电面二合一） | 电面 PS | 1 | 2024-02 | 0.40 | 96% |
| 54 | Array-diff removal + Inorder（Morris）+ Patching Array（2019 两轮 | 电面 PS | 1 | 2019-11 | 0.40 | 96% |
| 55 | Query Audit Log 类（record_access / accessed_in_range / unacce | 电面 PS | 1 | 2024-02 | 0.40 | 97% |
| 56 | Event Subscription System（1M/s 通知） | SD | 1 | 2026 | 0.40 | 97% |
| 57 | Dynamic Blacklist Filter System（仅 1p3a 标题） | SD | 1 | 2026 | 0.40 | 97% |
| 58 | Merge Intervals（LC 56 原题） | OA | 1 | 2023-02 | 0.40 | 98% |
| 59 | Minimum Interval to Include Each Query（LC 1851 原题） | OA | 1 | 2023-02 | 0.40 | 98% |
| 60 | Palindromic Subsequences（LC 2002 原题） | OA | 1 | 2023-02 | 0.40 | 99% |
| 61 | Graph Valid Tree（LC 261 原题） | OA | 1 | 2023-02 | 0.40 | 99% |
| 62 | String Formation via dictionary（LC 1639 原题） | OA | 1 | 2023-02 | 0.40 | 100% |
| 63 | Meeting Rooms II（LC 253 型，2026 实习 VO） | onsite | 1 | 2026 | 0.40 | 100% |

**63 行 · 累计 80% 出现在第 33 行（前 52%）** —— cut line 以内的题先建题库。
