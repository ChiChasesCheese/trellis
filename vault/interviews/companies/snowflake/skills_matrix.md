# Skills matrix — Snowflake 考什么 · 哪道题练它 · 对应 JD 哪一行

技能 id：**S** = 编码/OOD 测试目标（来自 `catalog/raw/coding_*.md`、`ood.md` 的题面与追问），**D** = 系统设计目标（`raw/system_design.md`），**B** = 行为/项目目标（`raw/bq_hm_recruiter.md`）。JD 列 = 6 份 Snowflake SWE JD（`raw/process_and_jd.md` §6.3）里出现次数。题 ID 见 `catalog/CATALOG.md`。

| id | 技能 / 测试目标 | 为什么 Snowflake 考它 | 练它的题 | JD 行 |
|---|---|---|---|---|
| S01 | DAG 上的继承与覆盖（多父、deny-wins、反向索引） | Snowflake 产品本身是 ROLE/grant 图；#1 题族 | pc01 | 数据库内部 5/6 |
| S02 | 计数 DP：状态 = (位置, 游程/剩余时间)，取模 | 元音游程、paid/free server 反复出现 2022→2026 | q02 q01 | 算法与数据结构 5/6 |
| S03 | 加权区间调度 / 排序 + 二分 + DP | Maximum Order Volume；LC 1235 型 | q04 | 同上 |
| S04 | 树：深度计算、删叶子/剪子树、换根 | 树高压缩题族横跨 OA 与电面 | q03 | 同上 |
| S05 | 图：多源 BFS、路径重建、拓扑排序、valid tree | 网格最近设施、Wiki 点击、Course Schedule、Service startup | pc02 pc04 q10 q08 pc13 | 同上 |
| S06 | 滑窗与事件流（deque + 计数哈希 + 最频 key） | Recent Event Stream；与 Stripe ps01/cd06 同族 | pc03 | 大规模系统 4/6 |
| S07 | 消息传递模拟 / 异步聚合协议 | Distributed Tree Counting；Snowflake 元数据服务 fan-out/fan-in | pc10 | 分布式系统 5/6 |
| S08 | LC 原题 + 复杂度再压一档（Morris、Floyd、O(m·n)） | Inorder→Morris、Happy Number→O(1)、Server Selection O(m·n) | q07 pc06 q09 q06 | 算法 5/6 |
| S09 | 类设计先定 API 契约，再讲状态与不变量 | 所有 OOD 题；task scheduler 挂经就是契约没定清 | od01 od02 od03 od07 | "design/build services" |
| S10 | 并发正确性：锁粒度、原子 claim/lease、每线程事务栈 | 5/10 OOD 题有明确并发追问 | od03 od04 od05 od01 | 并发 1/6 明确 + 分布式 5/6 |
| S11 | 持久化与恢复：WAL/快照、崩溃不丢触发 | 文件系统追问、cron scheduler (f) | od02 od05 | 数据库内部 5/6 |
| S12 | 缓存与淘汰（LRU/TTL/多级） | warehouse SSD cache 框架 | od08 | 大规模系统 |
| S13 | 队列语义（at-least-once、落盘确认、背压） | Queue 类→服务（onsite 挂经） | od09 sd05 | 分布式 5/6 |
| D01 | 先说不变量再画图；显式说"不做什么" | SD 面试官压 failure modes；沉默面试官下自己带节奏 | sd01–sd11 | — |
| D02 | 一致性协议与版本：Raft、2PC、MVCC/快照、compaction | KV store 题族（#refs 最高的 SD） | sd01 | 数据库内部 5/6 |
| D03 | 调度器：幂等、lease、失败隔离、cron 粒度 | "SQL engine as cron"（一手）、Reliable Job Scheduler | sd02 od05 | 分布式 5/6 |
| D04 | 异步结果投递：submit/poll/fetch、流式分片、排队 | SQL notebook（两条一手） | sd03 | SQL 5/6 |
| D05 | 配额/限流：强一致 vs 本地缓存 + 同步，hot-key | Quota、Distributed Rate Limiter | sd04 sd07 | 大规模系统 |
| D06 | 审计/治理：不可变、时间窗、多租户、保留 | Audit log（含 senior 电面逐字） | sd06 od06 | 数据治理 1/6 |
| D07 | 依赖图刷新：增量 vs 全量、一致快照、失效传播 | DAG cache ≈ Dynamic Tables | sd08 | 查询优化/执行 2/6 |
| D08 | 用 Snowflake 原语作参照：Execution Anchor、FDB、Tasks、Streams offset、Dynamic Tables | 差异化加分；`../01-company-brief.md` §1 | 所有 SD | 数据库内部 5/6 |
| B01 | 项目深挖三层：why → 备选 → 可用性/容错/重做 | expertise 轮一手追问模式 | exp（S1、S5） | 大规模生产系统 4/6 |
| B02 | 8 条价值观逐条有故事（Own It / Get It Done / Integrity Always 优先） | HM 轮逐题记笔记 | hm（S1–S9） | — |
| B03 | 具体化 why Snowflake + level 不报数字 + 问 headcount | recruiter / team matching 一手风险 | rc tm | — |
| B04 | transcript 证据型回答（Chakra） | AI 轮打分只读 transcript | `../loop/rounds/00_ai_screen/questions.md`（79 题）· `stories.md` | — |

**决定过/挂的点（一手）**：S09（task scheduler 契约）· S13（queue 故障语义）· D01（沉默面试官）· B01（expertise 讲不出 why）· B03（headcount 搁置）。
