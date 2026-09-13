# 模型答案：设计分布式 KV Store（含 time travel / Raft）

> 取材：staffengprep.com "signature" 分布式版题面；1point3acres 问题库基础版；`../../raw/process_research.md` §3.2 #7；`catalog/raw/system_design.md` §1.1。按 `LOOP_GUIDE.md` §6 主线组织。

## 0. 两句话复述 + 不变量

**复述**：这是一个多基础设施团队共用的分布式键值存储，对外是简单的 PUT/GET/DELETE/getRange，但内部需要在机器宕机、网络分区的前提下保证单 key 强一致，并支持按任意历史时间戳查询某个 key 过去的值（point-in-time / time travel）。

**核心不变量**：

1. **单 key 线性一致**：一旦一个 PUT 返回成功，后续任何 GET（不管打到哪个副本）都必须看到这次写入或更晚的写入，不能读到更旧的值。
2. **写入有确定的全局顺序**：同一 key 的并发写必须有一个所有节点认可的先后顺序，不能出现"两个副本各自认为自己是最后写入者"。
3. **历史可查但不可变**：一旦某个 version 被提交，它的内容永久不变；time travel 只是"读某个更早的 version"，不是"回滚"。
4. **快照存储有界**：历史版本必须有 compaction/GC，不能无限增长。

明确"不做什么"：不追求跨分区的强一致（那是可选的 2PC 扩展，代价明显）；不保证任意长时间的历史保留（有固定的时间窗口，类比 Snowflake time travel 默认 1 天、最长 90 天）。

## 1. API 契约

```
PUT(key, value)              -> {version}
GET(key, as_of?: timestamp)  -> {value, version} | NotFound
DELETE(key)                  -> {version}          # 写墓碑，不物理删除
GETRANGE(minKey, maxKey, as_of?: timestamp, limit, cursor?)
                              -> {items: [(key, value, version)], next_cursor?}
```

- `version` 是复合值 `(partition_id, sequence)`，`sequence` 在分区内单调递增（由该分区的 Raft group 保证），不用挂钟时间戳做排序依据——避免多机时钟漂移导致的顺序错乱。挂钟时间仍然记录（`committed_at`），仅用于 `as_of` 查询做时间戳到 version 的映射，不参与一致性判断。
- `as_of` 语义：返回"在该时间戳时刻，该 key 已提交的最新版本"，等价于"找到 `committed_at <= as_of` 的最大 version"。
- `DELETE` 产生一个墓碑 version，`GET` 在墓碑之后（且没指定历史 `as_of`）返回 NotFound；`GET(key, as_of=<墓碑之前>)` 仍能读到删除前的值。
- `GETRANGE` 用 cursor 分页（不是 offset），因为底层是 LSM range scan，深分页用 offset 会退化成线性扫描。

## 2. 数据模型

```
分区路由表（独立的元数据服务，或客户端缓存 + 版本号做失效）:
  key_range(start, end) -> raft_group_id -> [replica_endpoints]

每个分区内部（一个 Raft group 管一段 key range）:
  当前值索引: key -> latest_version           # 点查快路径，内存 + 持久化的 index
  版本历史（LSM-tree，天然按 (key, version) 有序）:
    memtable(内存，最近写入) + 一系列不可变 SSTable(磁盘)
    每条记录: (key, version, value | TOMBSTONE, committed_at)

  Raft 日志: 每条日志项 = 一次 PUT/DELETE 的 (key, value, sequence)
             日志本身就是"版本历史"的权威来源，SSTable 是它的物化视图
```

**为什么用 LSM 而不是 B-tree**：写多读少、需要按 version 做 range scan 和历史读，LSM 的顺序写和天然分层结构（memtable → L0 → L1…）正好对上；compaction 顺带做 GC——超过保留窗口的老 version 在 compaction 时被丢弃。

## 3. 核心流程

**写路径（单分区）**：client 按 key 路由到对应 Raft group 的 leader → leader 分配下一个 sequence、把 `(key, value, sequence)` 写入 Raft 日志 → 复制到多数派并 commit → leader 应用到本地 memtable、更新当前值索引 → 返回 `version` 给 client。

**读路径**：
- 最新值：路由到 leader（或用 lease read / read index 允许 follower 在确认自己不落后的前提下也能读，减轻 leader 压力）→ 查当前值索引 → 命中直接返回，未命中查 memtable→SSTable 由新到旧找。
- `as_of` 历史值：直接跳过当前值索引，走版本历史层，在 memtable 和各 SSTable 里做"≤ as_of 对应的最大 version"的合并查找（多路归并，取最新一条未过期的记录）。

**跨分区原子更新（follow-up 会问到）**：如果一次更新只涉及一个 Raft group 内的多个 key，可以把这几个 key 的变更打包成**一条 Raft 日志项**原子提交，不需要额外协议。但如果 A、B 两个 key 分属不同分区，需要 **2PC**：
1. 协调者（可以是发起请求的客户端边车服务，也可以是独立的、自身也用 Raft 做容灾的协调者集群）生成一个全局事务 id，向 A、B 所在分区分别发 `PREPARE(txn_id, mutation)`。
2. 每个分区把"prepared but not committed"的 mutation 写入自己的 Raft 日志（这一步保证即使分区 leader 换人，prepared 状态也不丢），并锁住相关 key（拒绝其他事务修改）后 ack。
3. 协调者收齐两个 ack 后，写自己的"txn committed"决定（同样是持久化、可 Raft 复制的），再向两个分区发 `COMMIT`；分区各自把 mutation 应用到实际的版本历史里、解锁 key。
4. 若任一分区 prepare 超时或拒绝，协调者发 `ABORT`，各分区回滚 prepared 状态、解锁。

## 4. 失败模式与规模

**Raft 内部机制**：每个分区一个 Raft group（通常 3 或 5 副本）；leader 处理所有写，日志复制到多数派才 commit；leader 崩溃后 follower 检测心跳超时发起选举，新 leader 必须包含所有已提交的日志（Raft 选举限制保证这一点）；网络分区时少数派一侧无法凑够多数派，直接拒绝写入（保证一致性优先于可用性，CP 系统）。

**读一致性的细节**：如果允许 follower 读，需要 **read index**（follower 向 leader 确认自己已应用的日志 index 不落后于 leader 当前的 commit index）或**租约读**（leader 持有一个时间窗口的租约，租约内确信自己仍是 leader 就可以直接读本地状态），否则 follower 可能返回过期数据，违反线性一致这条不变量。

**Compaction 与快照增长**：历史版本按保留窗口（如 90 天）做 compaction 时物理裁剪；裁剪掉的 version 如果被 `as_of` 查询命中，返回"该时间点数据已超出保留窗口"而不是静默返回错误结果；compaction 是**存储层内部**的操作，不影响 Raft 日志的正确性（Raft 日志本身也有独立的日志截断/快照机制，防止日志无限增长——通过定期给状态机做快照后截断已经快照过的日志段）。

**跨分区事务的代价**：2PC 期间被锁住的 key 对其他事务不可用，如果协调者本身挂了会导致 key 长期悬挂——对策是协调者的决定（committed/aborted）必须先持久化再通知参与者，协调者重启后能靠持久化的日志把未完成事务推进完；进一步可以给 prepared 状态加超时，超时后参与者主动向协调者查询状态（而不是无限等待）。

**规模估算**：假设 100 个分区、每分区一个 3 副本 Raft group，整体可以水平扩展到分区数量线性增长的写吞吐；单分区写吞吐受 Raft 日志复制的网络往返延迟限制（典型几千到一万 QPS/分区），跨机房部署时要考虑把同一分区的多数派放在同城以控制复制延迟，牺牲的是跨机房容灾能力——这是需要主动提出讨论的 trade-off。

## 5. 分层与组件

- **路由/元数据层**：独立服务维护 key range → Raft group 映射，本身也需要高可用（可以用同一套 Raft 机制自举，或依赖更底层的强一致存储）；客户端缓存路由表，收到"分区已迁移"错误时刷新。
- **一致性层**（每个分区一个 Raft group）：只负责日志复制、leader 选举、commit 语义，不感知存储格式。
- **存储引擎层**（LSM-tree）：负责单机读写路径、compaction、快照裁剪，独立于一致性协议演进（未来换存储引擎不影响 Raft 层）。
- **事务协调层**（2PC，仅跨分区更新时介入）：单分区更新完全不经过这一层，保证快路径的延迟不被拖累。

## 6. rollout/测试/监控

- **测试**：用类 Jepsen 的故障注入（网络分区、leader 强制重启、时钟漂移）验证线性一致性没有被破坏；对 compaction 逻辑做"边界时间戳"的单元测试（保留窗口边缘的 `as_of` 查询）。
- **监控**：每分区 leader 稳定性/选举频率（频繁选举说明网络或负载有问题）；写入 p99 延迟；compaction 积压与历史存储增长率；2PC 事务的平均 prepared 时长与超时率。
- **rollout**：新分区上线先做"影子路由"（新请求同时发一份到新分区但不采信结果）验证正确性，再切真实流量；分区分裂时先在子分区上追平父分区的日志，再原子切换路由表，避免服务中断。

## 7. 用 Snowflake 自己的原语作参照

Snowflake 自己的**元数据全部集中存在 FoundationDB**（`01-company-brief.md` §1「三层架构」），这正是一个大规模生产级的分布式事务性 KV——FDB 本身就是"强一致 KV + 严格可序列化事务"的样板，Snowflake 的 zero-copy clone 和 time travel 能做到"只复制指针、按版本回看"，靠的正是 FDB 里保存了表的版本历史而不是每次物理拷贝数据；这与本题"版本历史存储 + point-in-time 查询"的设计思路完全同构。另外，Snowflake 的 **Execution Anchor**（`01-company-brief.md` §1）机制——每个查询绑定恰好一个 GS 实例、绑定信息存在 FDB 里、~99% 查询不转移、崩溃时走两阶段的非自愿转移——是"单资源恰好一个权威写者，崩溃后如何安全交接"这个问题的真实工程实践，跟本题"同一 key 固定路由到一个 Raft leader，leader 崩溃后走选举"是同一个模式在不同层面的体现。面试时可以直接说："这类似 Snowflake 内部给每个查询绑定单一权威执行者（Execution Anchor）的思路，只是这里的资源粒度是 key 而不是 query。"

## 8. 45 分钟口述时间表

- **0–5 min**：复述题目 + 说不变量（单 key 线性一致、有序写、历史不可变、快照有界），确认规模与 time travel 保留窗口。
- **5–12 min**：API 契约（PUT/GET/DELETE/GETRANGE + as_of 参数），数据模型（当前值索引 + LSM 版本历史）。
- **12–22 min**：核心流程——写路径过 Raft leader、读路径的 lease read/read index、point-in-time 查询怎么在 LSM 上实现。
- **22–35 min**：失败模式——Raft 选举、网络分区下的 CP 取舍、compaction 与快照增长、跨分区 2PC 的具体步骤与代价（这一段通常是面试官追问最密集的地方，主动往这个方向讲）。
- **35–42 min**：分层图 + rollout（新分区影子路由、分裂不停服）+ 监控指标。
- **42–45 min**：一句话总结不变量与最大的 trade-off（CP 优先于 AP、跨分区事务牺牲延迟换正确性），反问面试官。
