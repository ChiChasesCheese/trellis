# 前置课 03 · 分布式系统词汇表

> 目标：JD "分布式系统 5/6"，且 SD 轮 12 道题几乎每道都要用到下面这些词——面试评的不是"你能不能背定义"，是**"你能不能在设计里正确使用这个词，并说清它在这道题的代价"**。每个词：**一句定义 → 一句面试里怎么说 → 本 kit 哪题用到**。配合 `../00-essentials/05-sd-framework-snowflake-primitives.md` 的 8 构件表一起读——那张表是"构件"，这份词汇表是"构件之间怎么协作的语言"。

---

## 1. 一致性模型（Consistency Model）

**定义**：规定"多副本/多节点场景下，一次读操作最多能看到多旧的数据、多快能看到最新的写"的一组规则——从强到弱大致是线性一致（linearizable，像只有一份数据一样）→ 顺序一致 → 因果一致 → 最终一致（eventual，迟早收敛，不保证多迟）。

**面试里怎么说**："I'd give single-key operations linearizable consistency, but cross-partition reads are only eventually consistent unless the client opts into a distributed transaction — mixing the two into one blanket guarantee is usually over-promising."

**本 kit**：`sd01`（KV Store，追问"单 key 强一致、跨分区事务用 2PC"，即典型的"分层一致性"设计——不是整个系统统一一个一致性级别）。

---

## 2. Raft（共识算法）

**定义**：一种通过"选出一个 leader、所有写先到 leader、leader 把日志复制到多数派节点确认后才算提交"来让多个副本对"日志顺序"达成一致的算法；核心保证是**多数派确认过的日志不会丢**。

**面试里怎么说**："For the replicated log behind the KV store, I'd reach for a Raft-style leader election plus majority-quorum log replication rather than inventing my own consensus protocol."

**本 kit**：`sd01`（分布式 KV store 的追问方向之一），**不需要手写 Raft**——面试里说清"leader 写、多数派确认、leader 挂了重新选举"三句话，比试图现场推导算法细节更有效。Snowflake 自己的类比：**Execution Anchor** 不是 Raft（它是单查询绑定单实例的租约机制，不是多副本日志复制），面试里不要把两者混为一谈，见 `../20-cards/snowflake_internals.md`。

---

## 3. 2PC（Two-Phase Commit，两阶段提交）

**定义**：跨多个参与者做一次原子提交的协议——阶段一（prepare）问所有参与者"你能不能提交"，全部说能才进入阶段二（commit）真正提交；只要有一个说不能，全体回滚。**代价是阶段一到阶段二之间，参与者必须锁住资源等待协调者的决定**（协调者故障会导致参与者一直悬挂）。

**面试里怎么说**："A cross-partition transaction needs 2PC or an equivalent; I'd flag that the coordinator becoming a single point of blocking is the real cost, not just 'it's slower'."

**本 kit**：`sd01`（跨分区事务）、`sd22`（PB 级数据库间同步，追问一致性校验时可以提到"强一致场景下才需要 2PC，大多数同步场景其实用 CDC + 对账更划算"，见下文"CDC"词条）。

---

## 4. At-least-once（至少一次）

**定义**：一条消息/一次操作在异常情况下（重试、故障恢复）**可能被处理多次，但保证至少被处理一次，不会被静默丢弃**。代价是消费者必须自己处理重复（通常靠"幂等"，见下一条）。

**面试里怎么说**："I'll design for at-least-once delivery — that means every consumer must be idempotent, because a crash or a timeout can redeliver the same message."

**本 kit**：`od09`（队列，可见性超时到期后消息重新排队，可能被两个消费者先后拿到）、`sd05`（分布式队列服务，落盘确认前不算成功）。

---

## 5. Exactly-once（恰好一次）

**定义**：一条消息/一次操作保证**恰好被处理一次**——工程上几乎总是"at-least-once 传递 + 幂等消费"组合模拟出来的效果，而不是传输层真的做到物理上只发一次。**在面试里承诺"端到端 exactly-once"且说不清具体机制是明确的减分项**（`../20-cards/sd_checklist.md` 反例第二条）。

**面试里怎么说**："I won't promise end-to-end exactly-once at the transport layer — I'll get the equivalent behavior via at-least-once delivery plus an idempotency key on the consumer side."

**本 kit**：Snowpipe Streaming 用 offset token 做到"行级 exactly-once"是 Snowflake 自己少数敢明确承诺 exactly-once 的地方（`../20-cards/snowflake_internals.md`）——反问环节可以问"这个保证具体靠什么机制，是不是就是幂等 token"，展示你知道这句承诺背后必须有机制支撑，不是隔空喊话。

---

## 6. 幂等（Idempotency）

**定义**：同一个操作（带着同一个"幂等键"）执行一次和执行多次，效果完全一样。是"at-least-once 传递"能被安全使用的**前提条件**，不是可选优化。

**面试里怎么说**："I'll key each retry by (job_id, scheduled_time) so replaying the same key is a no-op — that's what makes at-least-once safe to use here."

**本 kit**：`od01`（重复 `add` 同一个未执行的 task_id 只是更新，不是重复调度）、`sd02`（job 失败重试）、`sd11`（Jira→PR 失败重试不重复建 PR）、Snowflake 的 **Streams**（offset 只在消费事务内推进，重放同一批次是幂等的）。

---

## 7. 租约（Lease）

**定义**：在**有限时间**内独占一份资源/一份工作的授权，到期自动失效（不需要持有者主动释放）——比永久锁更能容忍持有者故障（持有者挂了，锁不会永远锁死，等租约到期就能被别人抢到）。

**面试里怎么说**："Instead of a lock that could be held forever if the owner crashes, I'd use a time-bounded lease — if the holder dies, the lease expires and another instance picks up the work."

**本 kit**：`od05`（Cron Scheduler，`LeaseStore.try_claim`）、`sd02`（调度器多副本不重复触发）、`sd08`（DAG 缓存刷新单写者）。Snowflake 的 **Execution Anchor** 是这个概念的产品级实现：每个查询绑定恰好一个 GS 实例，绑定信息存 FDB，心跳嵌入事务证明"我还活着"，租约到期或心跳中断触发"非自愿转移"。

---

## 8. Fencing Token（防护令牌）

**定义**：租约机制的一个已知漏洞是——持有者 A 的租约"逻辑上"已经过期（比如它自己因为 GC 暂停/网络分区没意识到），但它仍然认为自己持有租约、继续对下游系统写入；防护令牌是给每次租约签发一个**单调递增的编号**，下游存储只接受"编号比它见过的最大编号更大"的写入，从而拒绝掉过期租约持有者的"迟到"写入。

**面试里怎么说**："A lease alone doesn't stop a paused-then-resumed holder from writing after it should have expired; I'd have the storage layer reject writes tagged with a fencing token older than the latest one it has accepted."

**本 kit**：`od05`/`sd02` 的租约设计如果被追问"如果拿到租约的 worker 因为 GC 暂停很久，租约过期后又醒过来继续写怎么办"——**这就是在问 fencing token**，本 kit 现有的 `LeaseStore.try_claim` 没有实现这一层，面试里可以主动说"当前实现假设持有者会诚实地在租约过期后停止写入；更严格的版本需要给下游存储加单调递增的 fencing token 校验"，这是加分的坦诚，不是暴露缺陷的减分。

---

## 9. 背压（Backpressure）

**定义**：当下游处理速度跟不上上游产生速度时，让**上游主动减速或拒绝**，而不是让中间的队列/缓冲区无限增长直到内存耗尽或延迟失控。

**面试里怎么说**："When the queue depth or worker latency crosses a threshold, I'd have producers see a slow-down signal — a 429, a smaller batch size, or admission control — rather than letting the buffer grow unbounded."

**本 kit**：`od04`/`sd07`（限流器本身就是背压的一种实现）、`sd04`（quota 系统）、`sd10`（爬虫的"礼貌性限速"）。Snowflake 的对应机制：warehouse 排队（查询提交速度超过仓库处理能力时排队而不是拒绝）、Cloud Services 每日免费额度耗尽后开始计费（经济层面的背压）。

---

## 10. CDC（Change Data Capture，变更数据捕获）

**定义**：不是定期把整张表重新导出对比，而是**捕获数据库自身的变更事件流**（insert/update/delete），下游按事件顺序重放来保持同步——比"全量快照 diff"更实时、更省资源，但需要处理"事件顺序保证""断点续传""schema 变化"等额外复杂度。

**面试里怎么说**："I'd use CDC to stream row-level changes rather than diffing full snapshots on a schedule — the trade-off is I now need to handle ordering, replay from a checkpoint, and schema drift explicitly."

**本 kit**：`sd22`（两个 PB 级数据库间同步，明确的追问点是"CDC vs 快照+增量、断点续传、schema 演进"）。Snowflake 自己的 CDC 原语是 **Streams**（对表版本的 offset 书签，查询得到净变化），`Datastream`（2026 预览，Kafka wire-compatible 原生流服务）——这是"用自己在 Snowflake 上的经验反过来讲 CDC"的现成桥，见 `04-snowflake-primitives.md` §1 第一行。

---

## 11. 自测

- [ ] 不看这篇，用一句话分别定义 at-least-once 和 exactly-once，并说出它们的关系（不是对立的两个选项，是组合关系）
- [ ] 解释 fencing token 解决的问题为什么"仅有租约"解决不了
- [ ] 挑 `sd01`/`sd02`/`sd22` 其中一题，说出它用到了这 10 个词里的哪几个，分别扮演什么角色
- [ ] 说出 Streams 和 CDC 的关系（Streams 是 Snowflake 对 CDC 这个通用概念的具体实现）
