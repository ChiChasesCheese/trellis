# Distributed KV Store（含 time travel / Raft）

我们内部很多团队都在用一个共享的键值存储做元数据管理——有的团队拿它存表的 schema 版本，有的拿它做分布式锁的租约记录，还有的拿它当配置中心。现在这个东西已经从"某个团队自己攒的一个内存 hashmap 加个持久化文件"，长成了一个所有基础设施团队都依赖的公共服务，我们想把它重新设计成一个正经的分布式系统。基本接口很朴素：`PUT(key, value)`、`GET(key)`、`DELETE(key)`、以及一个 `getRange(minKey, maxKey)` 做范围扫描。但几个团队都提了同一个需求：他们希望能拿到某个 key 在"过去某个时间点"的值——不是简单的软删除或者版本号自增，而是类似"给我看这个 key 在 5 分钟前长什么样"这种可以按时间戳查询的能力，因为他们经常要排查"这个配置到底是什么时候被改坏的"这类问题。数据量和访问量都在快速增长，单机内存和单机磁盘都装不下也扛不住了，所以这必须是一个多机的、能水平扩展的系统；与此同时，可靠性要求也上来了——机器会宕、网络会分区，但业务方不能接受"我刚写进去的东西读不出来"或者"两个人同时改同一个 key，最后数据变得不知道是谁的"。有团队还问，如果他们要做一个跨多个 key（甚至跨分区）的原子更新——比如"同时改 A 和 B 两个 key，要么都成功要么都不生效"——这套系统能不能支持。请设计这个系统。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟（多份报告落在两种口径都有；电面阶段常与一轮 coding 搭配，构成"两轮 back-to-back 各 60 min"里的一轮）。白板工具未证实——不同于 Stripe 明确用 Whimsical，没有任何一手报告点名 Snowflake 用哪个白板产品，coding 轮确认用 CoderPad 但 SD 轮是否共用未知，实际操作中按"口头 + 简单画框图"准备即可。面试官风格两极分化：多数报告"人很好，会给 hint"，但至少一条 IC1/IC2 SD 报告明确"面试官全程沉默"，需要候选人自己主动推进设计、自己提出假设和边界条件，不能指望被追问式引导。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.1）：
- 基础版："PUT/GET/DELETE，需要持久化 + `getRange(minKey, maxKey)` + point-in-time snapshot" —— 1point3acres 问题库页面摘要（**中**，无法核实具体面经贴 ID）。
- "signature" 分布式版（多个聚合站复述细节高度一致）："Design a distributed KV store，PUT/GET/DELETE 接口，要求 global versioning、time travel 式 point-in-time snapshot、strong consistency on a single key within a partition、Raft-based replication、service discovery；follow-up 延伸到跨分区更新多个 key 的分布式事务协议，需 serializability，涉及两阶段提交" —— staffengprep.com（**中**，聚合站转述，但与 Snowflake 自身"FDB 存元数据 + 分区版本"的架构高度吻合，可信度上调）。
- 磁盘/并发版："Design a Disk-Backed KV Store Under Contention"，考 durable on-disk storage、indexing 与并发 —— PracHub（**低**，AI 题库聚合站，仅作题型参考）。
- 复用材料：`../../raw/process_research.md` §3.2 #7 记录 2025-12 两轮 back-to-back 电面中出现"KV store 系统设计"，1p3a thread-1158595 搜索摘要（**中**）。
- 该题族是 Snowflake 面试库里**出现频率最高的 infra 题**，5 条独立来源，整体置信度 **HIGH-MED**。
