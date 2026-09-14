# PARETO — 28 法则排序输出（2026-09-14，RANK 并入 GitHub 蒸馏后重跑）

> 命令：`python3 tools/pareto.py catalog/RANK.md --table "总表" --focus "OA,电面,PS,技术筛" --title-col 题`
> 规则：score = #refs × 时效（≤3 月 1.0 / ≤12 月 0.8 / ≤24 月 0.6 / 更早 0.4）× 轮次权重（要面的轮次 1.0 / 其它技术轮 0.8 / 非编码轮 0.6）；cut line = 累计 80%。

| # | 题 | 轮次 | #refs | 最近 | score | 累计 |
|---|---|---|---:|---|---:|---:|
| 1 | RBAC / DAG 权限继承题族（Effective Access Control · Role Privileges | 电面 PS | 6 | 2026-09 | 6.00 | 4% |
| 2 | 元音游程 DP 题族（consecutive-vowel count · String Patterns `calcul | OA | 5 | 2026-06 | 5.00 | 8% |
| 3 | KV store（分布式：versioning / time-travel snapshot / Raft / rang | SD 电面+onsite | 5 | 2026-09 | 5.00 | 11% |
| 4 | In-Memory File System（LC 588 + rm/chunk/线程安全/WAL 追问） | 电面 PS | 5 | 2026-08 | 5.00 | 15% |
| 5 | Cron / Job Scheduler（含 "SQL engine running many queries as c | SD 电面+onsite | 5 | 2026-07 | 5.00 | 18% |
| 6 | 树高压缩题族（Minimum Height 换根 · Minimum N-ary Deletions · Prune M | OA+电面 PS | 4 | 2026-08 | 4.00 | 21% |
| 7 | Recent Event Stream Queries（最近 m 条事件：count 去重 / top 最频 key）+ | 电面 PS | 4 | 2026-08 | 4.00 | 24% |
| 8 | Distributed Tree Counting 状态机（消息传递 fan-out/fan-in） | 电面 PS | 4 | 2026-07 | 4.00 | 26% |
| 9 | Audit / Query-Event Log Service（"pg_stat for Snowflake"，多租户、 | SD 电面+onsite | 4 | 2026-06 | 4.00 | 29% |
| 10 | Quota System（多上游服务共用，强一致 vs 本地缓存） | SD | 4 | 2026-06 | 3.20 | 31% |
| 11 | Distributed Rate Limiter（per-second，防 hot-spot / thundering  | SD | 4 | 2026-09 | 3.20 | 34% |
| 12 | Maximum Order Volume / phone calls（加权区间调度，LC 1235 型） | OA | 4 | 2026-01 | 3.20 | 36% |
| 13 | SQL Notebook / 查询结果分发（submit→poll→fetch，大结果集流式） | SD 电面 | 3 | 2026-08 | 3.00 | 38% |
| 14 | Closest Bathroom / Desk on a Grid（多源 BFS） | 电面 PS | 3 | 2026-09 | 3.00 | 40% |
| 15 | Web Crawler Shortest Path Reconstruction | 电面 PS | 3 | 2026-09 | 3.00 | 42% |
| 16 | Rate Limiter（onsite 滑窗单规则 + 电面多规则排队线程安全） | onsite+电面 | 3 | 2026-08 | 3.00 | 44% |
| 17 | Concurrent Web Crawler（BFS + 去重 + 扩展） | SD/编码 | 4 | 2026-03 | 2.56 | 46% |
| 18 | Task Scheduling — paid vs free server（0/1 背包式调度） | OA | 3 | 2026-03 | 2.40 | 48% |
| 19 | Task Scheduler `addTask(id,priority,ts)` / `executeTask()`（+ | onsite | 3 | 2026-08 | 2.40 | 49% |
| 20 | Automated Jira-Ticket-to-PR System（异步任务、队列架构；一手印证） | SD onsite | 3 | 2026-06 | 2.40 | 51% |
| 21 | Course Schedule II（LC 210 原题；电面拓扑排序同族） | OA+电面 | 3 | 2026-03 | 2.40 | 53% |
| 22 | Cron Scheduler 类：schedule / pause / resume / tick（多实例不重复触发） | 技术筛 | 2 | 2026-06 | 2.00 | 54% |
| 23 | LC 1751 Maximum Number of Events That Can Be Attended II 变体  | 电面 PS | 2 | 2026-06 | 2.00 | 55% |
| 24 | Happy Number：O(n) → O(1)（Floyd 判环）；前 20 min 讲项目 | 电面/onsite | 2 | 2026-07 | 2.00 | 57% |
| 25 | Transactional in-memory KV store（嵌套事务 begin/commit/rollback  | 技术筛 | 2 | 2026-08 | 2.00 | 58% |
| 26 | Dynamic Blacklist Filter System（两条并发流：黑名单增删 / 输入值；原 sd20，Tru | 电面 PS | 2 | 2026-06 | 2.00 | 60% |
| 27 | Object Store with Deduplication（Blob 去重） | SD | 3 | 2025-12 | 1.92 | 61% |
| 28 | Queue 类（类 deque）→ 扩展为云端 queue service（故障语义） | onsite | 2 | 2026-08 | 1.60 | 62% |
| 29 | Distributed Queue Service（enqueue/dequeue 故障行为、at-least-once | SD onsite | 2 | 2026-08 | 1.60 | 63% |
| 30 | Paint the Ceiling（递推生成边长，计数 area ≤ a 的对） | OA | 2 | 2026-03 | 1.60 | 64% |
| 31 | Word Search II（LC 212）+ 审计日志设计（senior 电面二合一） | 电面 PS | 2 | 2026-02 | 1.60 | 65% |
| 32 | Parallel Courses III（LC 2050 原题） | onsite | 2 | 2026-08 | 1.60 | 66% |
| 33 | Merge Intervals（LC 56 原题） | OA | 2 | 2026-02 | 1.60 | 68% |
| 34 | Parentheses Matching（栈） | 电面 PS | 2 | 2026-03 | 1.60 | 69% |
| 35 | Maximize OR-Sum（AIML 实习 OA 一手） | OA | 2 | 2026-05 | 1.60 | 70% |
| 36 | Student / Result OOP（OA 内嵌） | OA | 2 | 2026-05 | 1.60 | 71% |
| 37 | DAG Cache for Query Views / Materialized Views（≈ Dynamic Tab | SD | 2 | 2026-03 | 1.28 | 72% |
| 38 | ACL Authorization Checking Service | SD | 2 | 2026-02 | 1.28 | 73% |
| 39 | REST API Abstraction Layer / Internal Service-Client SDK | SD | 2 | 2026-05 | 1.28 | 74% |
| 40 | LRU Cache（warehouse SSD cache 框架 + TTL 追问） | onsite | 3 | 2026 | 1.20 | 74% |
| 41 | Throne Inheritance without initial king（LC 1600 变体） | 电面 PS | 2 | 2026 | 1.00 | 75% |
| 42 | Reverse Alphanumeric Segments（1p3a 标题） | 电面 PS | 2 | 2026 | 1.00 | 76% |
| 43 | Minimum Clicks Between Wiki Pages（图 BFS；OA 与电面池都有） | OA+电面 | 1 | 2026-09 | 1.00 | 76% |
| 44 | User Password Storage 系统设计 | SD 电面/onsite | 1 | 2026-07 | 1.00 | 77% |
| 45 | Generating Login Codes（New Grad OA，仅标题+标签） | OA | 1 | 2026-09 | 1.00 | 78% |
| 46 | Character Frequencies（跨字符串 / 嵌套列表） | 电面 PS | 1 | 2026-06 | 1.00 | 79% |
| 47 | Top Two Users by Total Purchase Amount | 电面 PS | 1 | 2026-06 | 1.00 | 79% |
| 48 | Forest Parent Array Delete Node（parent 数组删点 + 下标压缩） | 电面 PS | 1 | 2026-06 | 1.00 | 80% |
| 49 | Number Transformation Path（+2 / −2 / ⌊÷2⌋ 路径） | 电面 PS | 1 | 2026-06 | 1.00 | 81% |
| 50 | Rewrite Tree With Subtree Sums（同形完全二叉树写子树和） | 电面 PS | 1 | 2026-06 | 1.00 | 81% |
| 51 | Four-in-a-row `canPlayWin` + Design Connect Four | 电面 PS | 1 | 2026-06 | 1.00 | 82% |
| 52 | Patching Array（LC 484 原题；2019 电面也考） | OA+电面 | 2 | 2023-02 | 0.80 | 83% |
| 53 | Binary Tree Inorder Traversal（LC 94 + Morris 追问） | OA+电面 | 2 | 2023-02 | 0.80 | 83% |
| 54 | Server Selection（m 服务器 × n 任务 2D DP，目标 O(m·n)） | OA | 2 | 2023-02 | 0.80 | 84% |
| 55 | Meeting Rooms II（LC 253 型，2026 实习 VO） | onsite | 2 | 2026 | 0.80 | 84% |
| 56 | Geolocation Search Service | SD | 1 | 2026-07 | 0.80 | 85% |
| 57 | Service Startup / Dependency Ordering（Kahn） | 电面 PS | 1 | 2026-03 | 0.80 | 85% |
| 58 | PB 级数据库间同步（IC2 一手，不许澄清需求） | SD 电面+onsite | 1 | 2026-03 | 0.80 | 86% |
| 59 | SnowCal 小语言 / String-Command Calculator（累加器解释器） | 电面 PS | 1 | 2026-05 | 0.80 | 86% |
| 60 | Document Predicate Search Engine（倒排 + 布尔查询，3 Part） | 电面 PS | 1 | 2026-04 | 0.80 | 87% |
| 61 | Min Coins to Pay with Change Allowed | 电面 PS | 1 | 2026-02 | 0.80 | 88% |
| 62 | Service Failure Forensics（二分最早错误 → 级联失败 → 最长传播链） | 电面 PS | 1 | 2026-02 | 0.80 | 88% |
| 63 | Grep With Context Lines | 电面 PS | 1 | 2026-02 | 0.80 | 89% |
| 64 | Top K Hash Tags（去重用户数） | 电面 PS | 1 | 2026-02 | 0.80 | 89% |
| 65 | Recipe Sequence Matcher（连续子序列 + O(1) 空间追问） | 电面 PS | 1 | 2026-01 | 0.80 | 90% |
| 66 | Preorder Traversal Without Invalid Nodes | 电面 PS | 1 | 2025-12 | 0.80 | 90% |
| 67 | Valid Tic-Tac-Toe State（N×N、K 连） | 电面 PS | 1 | 2025-11 | 0.80 | 91% |
| 68 | Top K Book Sales `bestSellers` | 电面 PS | 1 | 2026-02 | 0.80 | 91% |
| 69 | Serialize / Deserialize Dictionary Trie | 电面 PS | 1 | 2025-12 | 0.80 | 92% |
| 70 | Durable KV Store Serialization（自定义编码 + 1 KB 分块） | 电面 PS | 1 | 2025-11 | 0.80 | 93% |
| 71 | Maximum Profit Query Selection | OA | 1 | 2026-01 | 0.80 | 93% |
| 72 | Dropped Requests（多窗口限流拒绝） | OA | 1 | 2025-11 | 0.80 | 94% |
| 73 | Distributed Metadata Catalog / Schema Registry | SD | 1 | 2025-09 | 0.64 | 94% |
| 74 | Multi-Tenant Interactive Analytics Platform（摄取+查询端到端） | SD | 1 | 2025-09 | 0.64 | 95% |
| 75 | Resilient Auth with Flaky Third-Party Tokens | SD | 1 | 2025-09 | 0.64 | 95% |
| 76 | Cross-Platform Logging Library | SD | 1 | 2026-03 | 0.64 | 95% |
| 77 | Remove Stones to Minimize the Total（LC 1962 原题） | OA | 1 | 2024-12 | 0.60 | 96% |
| 78 | Work Schedule（`?` 填充枚举） | OA | 1 | 2025-07 | 0.60 | 96% |
| 79 | Min-Height-Trees 图变体（LC 310 + twist） | OA | 1 | 2026 | 0.50 | 97% |
| 80 | JSON Parser（最小化输出 / INVALID） | 电面 PS | 1 | 未知 | 0.50 | 97% |
| 81 | Sequential String（前缀凑排列，JoeBao22 OA 2024） | OA | 1 | 2024 | 0.50 | 97% |
| 82 | Maximum Throughput（二分答案 + 升级预算） | OA | 1 | 未知 | 0.50 | 98% |
| 83 | Distance from Each 1 to the Nearest 2 | OA | 1 | 未知 | 0.50 | 98% |
| 84 | Array-diff removal + Inorder（Morris）+ Patching Array（2019 两轮 | 电面 PS | 1 | 2019-11 | 0.40 | 98% |
| 85 | Query Audit Log 类（record_access / accessed_in_range / unacce | 电面 PS | 1 | 2024-02 | 0.40 | 99% |
| 86 | Event Subscription System（1M/s 通知） | SD | 1 | 2026 | 0.40 | 99% |
| 87 | Minimum Interval to Include Each Query（LC 1851 原题） | OA | 1 | 2023-02 | 0.40 | 99% |
| 88 | Palindromic Subsequences（LC 2002 原题） | OA | 1 | 2023-02 | 0.40 | 99% |
| 89 | Graph Valid Tree（LC 261 原题） | OA | 1 | 2023-02 | 0.40 | 100% |
| 90 | String Formation via dictionary（LC 1639 原题） | OA | 1 | 2023-02 | 0.40 | 100% |

**90 行 · 累计 80% 出现在第 49 行（前 54%）** —— cut line 以内的题先建题库。
