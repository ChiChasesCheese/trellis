# 05 · SD 45 分钟结构 + 8 个共用构件 ↔ Snowflake 原语

> 45 分钟的分钟表、五维 rubric、三句 Snowflake 味加分句已经在 `../20-cards/sd_checklist.md` 里写完，**这里不重复**，只做一件事：把 `../../catalog/CATALOG.md` Table C 的 12 道 SD 题拆开，找出反复出现的 8 个构件，说清每个构件在哪几题出现、对应 Snowflake 哪个原语。背下这张表，任何一道没见过的 SD 题，先问"这 8 个里哪几个用得上"，比从零画框图快得多。

---

## 0. 怎么用这份文件

`sd_checklist.md` 已经告诉你 45 分钟怎么分配、五维怎么打分。这份文件解决的是**"具体设计决策该说什么"**——SD 面试挂点最常见的不是流程不对，是"加缓存、加队列、加机器"这种空话（`sd_checklist.md` 反例第一条）。8 个构件就是把空话变成具体机制的词汇表：**先在 API/数据模型阶段（8–15 min）就点名要用哪几个构件，再在失败模式阶段（25–35 min）说清它们各自怎么失败。**

---

## 1. 八个构件 ↔ 出现的题 ↔ Snowflake 原语

| 构件 | 一句定义 | 出现在哪些 SD 题 | 对应 Snowflake 原语 | 面试里怎么说一句 |
|---|---|---|---|---|
| **幂等键** | 同一个逻辑操作重试多次，效果等于执行一次 | `sd02`（job 失败重试）· `sd05`（消息重投）· `sd11`（Jira→PR 失败重试）· `sd22`（CDC 断点续传重放） | Streams：offset 只在消费它的 DML 事务**内部**推进，崩溃后重放该批次幂等；Snowpipe Streaming 的 offset token | "Each job run is keyed by (job_id, scheduled_time); replaying the same key is a no-op, the same way a Snowflake Stream only advances its offset inside the consuming transaction." |
| **租约（lease）** | 在有效期内独占一份工作，到期自动释放，别人可以抢 | `sd02`（调度器多副本不重复触发）· `sd08`（DAG 刷新单写者）· `sd05`（消费者可见性超时） | **Execution Anchor**：每个查询绑定恰好一个 GS 实例，绑定信息存 FDB，心跳嵌入事务；~99% 查询不转移 | "I'd bind each job to exactly one worker via a lease in the metadata store — that's what your Execution Anchor does for queries, down to the 'crash triggers involuntary transfer' detail." |
| **唯一约束 + CAS** | 用存储层的原子"若不存在则插入/若版本匹配则更新"代替应用层加锁 | `sd01`（分布式 KV 单 key 强一致）· `sd02`（调度器 claim）· `sd04`（quota 扣减）· `sd07`（限流令牌桶） | Hybrid Tables 强制 PK + 行锁做毫秒点查；Execution Anchor 的 in-process guard 在每次 FDB 事务前校验绑定 | "The claim itself is a conditional write — insert-if-absent on (job_id, tick) — not a distributed lock held across the whole operation." |
| **outbox** | 把"改数据"和"发通知/触发下游"绑进同一个事务，避免"改了但没通知"或"通知了但没改" | `sd03`（查询结果异步 submit→poll→fetch）· `sd06`（写业务表的同时写审计记录）· `sd11`（DB 写入后触发 PR 创建） | Streams + MERGE：消费 stream 净变化和写下游是同一个事务，天然是 outbox 的一种实现 | "I don't fire the downstream event separately — the write and the event marker commit atomically, the way a Stream's offset only advances alongside the consuming write." |
| **背压** | 下游处理不过来时，让上游主动减速而不是让队列无限堆积 | `sd04`（quota 限流）· `sd07`（分布式限流器）· `sd03`（仓库排队）· `sd10`（爬虫礼貌性限速） | Warehouse 排队 + 60 s 计费粒度；Cloud Services 每日免费额度 = 仓库消耗 10%（超了自然限速） | "When the queue depth crosses a threshold, producers get a 429/backoff signal instead of the queue growing unbounded — same shape as warehouse query queueing under load." |
| **分片** | 按某个 key 把数据/负载切开，各分片独立扩展、独立失败 | `sd01`（KV 分区）· `sd06`（多租户审计日志按租户分片）· `sd10`（爬虫按域名分片）· `sd22`（PB 级同步分批回填） | 存算分离：micro-partition 是存储的天然分片单位；virtual warehouse 是计算的独立扩展单位 | "I'd shard by tenant so one noisy tenant's audit volume can't starve another's queries — the same isolation virtual warehouses give you on the compute side." |
| **快照 + 增量** | 定期打一个完整基线，之间只传变化量；判定"什么时候增量不够、要重新打基线" | `sd01`（point-in-time snapshot）· `sd08`（DAG 缓存增量 vs 全量刷新）· `sd22`（CDC vs 全量回填） | **Time Travel / zero-copy clone**（快照是元数据指针，几乎免费）；**Dynamic Tables** 的 `TARGET_LAG` + 2026-07 **Adaptive Refresh**（上游大变动自动重初始化）| "The refresh is incremental when the upstream delta is small; when it isn't, I reinitialize from a full snapshot — that's exactly the Adaptive Refresh decision Dynamic Tables makes." |
| **不可变日志** | 只追加、不改写的记录序列；查询是在这个序列上做范围扫描，不是就地更新 | `sd06`（审计日志防篡改）· `sd01`（KV 版本历史）· `sd08`（依赖图变更序列）· `od06`（同族 OOD 题） | 底层数据本身是不可变列式 micro-partition；**Streams** 就是"表版本"这条不可变序列上的 offset 书签 | "Audit records are append-only; 'undo' means writing a compensating record, never rewriting history — the same discipline that makes Time Travel possible." |

---

## 2. 用法：8 个构件如何组合出一道题的答案骨架

拿到一道没准备过的 SD 题，先扫一遍这张表，圈出用得上的 2–4 个构件，再按 `sd_checklist.md` 的分钟表填内容。例子：

**`sd02`（Cron/Job Scheduler）**：幂等键（job_id + scheduled_time）+ 租约（哪个 worker 拥有这次执行）+ 唯一约束/CAS（claim 的原子性）+ 背压（1e6 job/分钟峰值时怎么不炸）。**四个构件覆盖了这道题 rubric 里 Failure modes 维度几乎全部的内容**——"幂等重试、失败隔离、多副本 lease"三个面试官会压的点，正好是幂等键 + 租约两个构件的组合。

**`sd22`（两个 PB 级数据库间同步，不允许需求澄清）**：幂等键（断点续传怎么不重不丏）+ 分片（回填按什么粒度分批）+ 快照+增量（CDC 首次全量、之后增量）。这道题一手报告说"面试官不给澄清，自己声明假设再推进"——**先把这三个构件的假设说出口**（"I'll assume idempotent replay keyed by (table, watermark), sharded backfill by partition key, CDC after an initial snapshot"），比空手画框图更快建立结构。

**`sd05`（Distributed Queue Service）**：幂等键（消费者必须能处理重投）+ 租约（可见性超时本质是租约）+ 背压（生产者写入速率 vs 消费者处理速率）。**这题和 OOD 的 `od09` 是同一个语义模型**，SD 版本只是把"一个类"换成"一个服务"，五步答法完全复用 `04-class-design-and-concurrency.md` §8。

---

## 3. 和 `sd_checklist.md` 三句加分句的关系

`sd_checklist.md` 已经给了三句可以直接背的"Snowflake 味加分句"（单写者/Execution Anchor、增量 vs 全量/Dynamic Tables、offset 只在事务内推进/Streams）——对照上表就会发现，**这三句分别对应"租约"、"快照+增量"、"outbox"三个构件**。这不是巧合：这三个构件恰好是 Snowflake 自己产品化程度最高、最容易讲清楚的部分，所以 `sd_checklist.md` 选了它们做"三句加分句"。剩下的"幂等键、唯一约束+CAS、背压、分片、不可变日志"五个构件同样能对应 Snowflake 原语（见上表），只是需要多说一句才能落地，不适合压缩成一句模板——**遇到题目需要时展开说，不用强行现场编一句"加分句"**。

---

## 4. 反问：从构件反推到 Snowflake 内部（40–45 min 环节）

`../20-cards/snowflake_internals.md` 里每条原语都配了"面试里怎么用"，8 个构件表已经把对应关系摆平；到反问环节，直接从**自己刚设计的构件**跳到 Snowflake 的对应机制并追问细节，比泛泛地问"你们技术栈是什么"更有信号：

- 用了**租约**构件 → "Execution Anchor 的心跳嵌入事务这件事，是所有事务类型都走这条路径，还是只对长查询？"
- 用了**快照+增量** → "Adaptive Refresh 判断'要不要重新初始化'的信号具体是什么阈值？"
- 用了**分片** → "micro-partition 的默认大小是怎么在写入时决定的，会不会因为写入模式产生'热分片'？"

这三句反问的素材都在 `../00-prereq/04-snowflake-primitives.md`（本 kit 已有文件，不在本文件重复）——45 分钟结构里最后一步是把这份文件和第 1 节的映射表在脑子里连起来，不是临场现编。
