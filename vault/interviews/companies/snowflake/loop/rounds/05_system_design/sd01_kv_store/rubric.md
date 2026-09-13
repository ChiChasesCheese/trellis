# 评分 rubric（五维，1–4 分/维，满分 20）

> 依据 `loop/LOOP_GUIDE.md` §6 与 `catalog/raw/system_design.md` §1.1。这是 Snowflake SD 题库里出现频率最高、版本最多的一族——面试官很可能会在你选定一个版本后，主动把你推向"分布式版"（time travel + Raft + 跨分区事务），所以基础版答完就该主动升级，不要等对方问。

## 1. Problem framing（需求抽取）

- **1 分**：一上来就画"Client → 分片 → 节点"框图，没有先确认这是单机 KV 还是分布式 KV、没有问清楚 point-in-time 查询的粒度（任意时间戳？还是固定间隔快照？）；被问"这个系统最重要的保证是什么"答成"高可用"这种空话。
- **4 分**：先用两句话复述题目——"这是一个多团队共用的分布式元数据 KV，需要在网络分区和机器宕机下保证单 key 强一致，同时支持按任意历史时间戳读取过去的值"；显式说出关键不变量——**已提交的写入不能读不到**（read-your-writes / 线性一致）、**同一 key 的并发写必须有确定的胜者**（不能"谁的写后到就静默覆盖谁"）、**历史快照只增不能无限增长**（需要 compaction/GC 策略）；主动确认规模（QPS、key 数量、value 大小、range scan 的典型跨度）与 time travel 的保留窗口（类比 Snowflake 默认 1 天最长 90 天）。

## 2. API & data model（权重最高）

- **1 分**：只写了 `put/get/delete`，`getRange` 和 point-in-time 查询没有具体签名；没有区分"key 的最新值"和"key 的版本历史"两种存储；把 versioning 讲成"每次写自增一个整数"就结束，没说这个整数在分布式环境下怎么保证全局单调。
- **4 分**：给出完整接口 `PUT(key, value) -> version`、`GET(key, [as_of=ts]) -> (value, version)`、`DELETE(key)`（墓碑，不是物理删除）、`GETRANGE(minKey, maxKey, [as_of=ts])`；数据模型区分**当前值索引**（key → 最新 version 指针，供快速点查）与**版本历史存储**（(key, version) → value，LSM 结构，天然按 version 有序，range scan 和历史读都在这一层做）；version 用**分区内单调递增序列 + 分区号**组成全局可比较的复合版本号（而不是挂钟时间戳，避免时钟漂移导致的顺序错乱）；point-in-time 查询实现为"找到 ≤ as_of 的最大 version"，这是让候选人证明理解 LSM/MVCC 的关键点。

## 3. Failure modes & scale（本题权重也很高）

- **1 分**：一致性协议只说"用 Raft 就行"，说不出 leader 选举、日志复制、commit 的具体流程；point-in-time 快照说"就一直存着"，没意识到历史数据会无限增长拖垮存储；被追问"跨分区原子更新"答不出为什么单纯 Raft 不够、需要 2PC/事务协调。
- **4 分**：讲清 Raft 内部——leader 处理写请求、日志复制到多数派后 commit、leader 挂了走选举、follower 只读走 leader 或有界 staleness 的 read index；讲清**单 key 强一致**的落地——同一 key 固定路由到同一个分区的 Raft group，写只能过 leader，读默认也过 leader（或用 read index/lease read 保证不读到脏数据）；讲清**跨分区事务**——单个 Raft group 内的多 key 更新可以用组内的一次 Raft 日志原子完成，但跨多个分区（多个 Raft group）就需要 **2PC**：一个协调者先给所有参与分区发 prepare、各分区各自在自己的 Raft 日志里记一条"prepared"再回 ack，协调者收齐后发 commit，任一分区 timeout/失败就发 abort；能主动指出 2PC 的代价——协调者是新的单点（可以让协调者本身也是一个 Raft group）、prepared 状态期间该 key 被锁住会影响可用性；**compaction**——历史版本按保留窗口定期合并/裁剪，超过窗口的老版本物理删除并留一条"已裁剪"标记防止误判为不存在。

## 4. Separation of concerns

- **1 分**：把路由、一致性协议、存储引擎、time travel 全部糅在一个"KV 节点"框里；client 怎么找到某个 key 在哪个分区没有设计。
- **4 分**：分层清楚——**路由层**（客户端或独立的路由服务维护 key range → Raft group 的映射，支持分区分裂/合并时的重路由）；**一致性层**（每个分区一个 Raft group，只负责日志复制和 leader 选举，不关心存储格式）；**存储引擎层**（LSM-tree，membtable + SSTable，独立负责单机的读写路径与 compaction）；**事务协调层**（2PC 协调者，独立于单分区的 Raft，只在跨分区更新时才被调用，单分区更新走快路径不经过协调者）。

## 5. Delivery beyond the diagram（rollout / 测试 / 监控）

- **1 分**：画完架构图就结束，不谈怎么验证正确性、怎么上线。
- **4 分**：讲到关键监控指标（每分区的 Raft leader 稳定性/选举频率、写入延迟 p99、compaction 积压、历史版本存储增长率）；讲到用 Jepsen 类型的分区注入测试验证线性一致性；讲到分片扩容（分区分裂）时如何不停服——先在新分区上做日志复制追平，再原子切流量；讲到 2PC 协调者本身的容灾（协调者状态持久化，崩溃后能从日志恢复未完成的事务，不会永久悬挂锁住的 key）。
