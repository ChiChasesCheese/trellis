# 论坛里出现、但题库和本 kit 的 5 道新题都没有完整覆盖的 HLD：6 个答题骨架

> 来源：`../catalog/raw/forums.md` §3.3 / §4.4（2025-01..2026-10 的候选人报告）。**这是骨架（sketch），不是完整题解**：每个只给需求关键点、数据模型、4–5 个关键决策、
> 常见追问。题面原文引自 forums.md；设计内容是我基于 `00_ddia_refresh.md` 和 AWS 公开实践的推断（标 `推断`）。完整题解的深度参考 `problems/` 下的 5 道。
> 用法：每个骨架限时 25 分钟口述，然后对照检查是否覆盖了 `00_how_to_run_the_round.md` §8 的评分维度。

---

## S1. Artifact Repository（JFrog 式：上传一个制品、取回一个制品）

- 题面：LC8464434（AWS Dublin SDE2，2026-08）"Design Artifact Repository (like JFrog, adding an artifact and fetching an artifact)"，追问 **可扩展性、指标监控、可靠性、可扩展的功能（恶意制品）**。
- 需求要点：发布不可变的版本化制品（大二进制 + 元数据）；按坐标 `(组, 名称, 版本)` 取回；读远多于写（CI 每次构建都拉依赖）。
- 数据模型 `推断`：
  - 元数据：`Artifact(group, name, version) → {sha256, size, publisher, created_at, state}`，强一致 KV（DynamoDB 风格，分区键 `(group,name)`，排序键 `version`）。
  - 内容：**内容寻址**存对象存储，键 = `sha256`；同内容多版本/多仓库天然去重（见 [design-file-sync](../../../../domains/system-design/drills/problems/design-file-sync.md) 的块级内容寻址）。
- 关键决策：
  1. **发布是两阶段**：先上传 blob（分段并发、可恢复）→ 校验 sha256 → 再用**条件写**提交元数据（`attribute_not_exists(version)` 保证版本不可变）。读者只通过元数据找 blob，所以元数据提交前 blob 对外不可见（半成品不可见）。
  2. **下载**走 CDN / 区域缓存（读多）；热门制品命中率高；缓存键含 sha256，天然不可变，永不失效。
  3. **恶意制品**：发布后状态为 `quarantined`，异步扫描管线（病毒/许可证/已知漏洞）通过后才变 `available`；签名校验；依赖混淆攻击（内部包名被公共仓库同名包覆盖）用"命名空间优先级"防御。
  4. **垃圾回收**：blob 被多个版本引用 → 引用计数或 mark-and-sweep；删除版本只删元数据，blob 在无引用且过保留期后回收；GC 与发布并发要避免误删（引用先于 blob 存在的窗口）。
  5. **可观测**：发布成功率、下载 p99、缓存命中率、扫描积压；canary 定时发布/下载一个探针制品。
- 追问：多区域复制（元数据全局表 + blob 跨区域复制，读就近）；一致性（发布后立即可读 vs 缓存）；超大文件（分段、断点续传）；配额与多租户公平（见 [aws-shuffle-sharding](../../../../domains/system-design/readings/aws-shuffle-sharding.md)）。
- 题库近邻：[design-object-storage](../../../../domains/system-design/drills/problems/design-object-storage.md)、[design-file-sync](../../../../domains/system-design/drills/problems/design-file-sync.md)、[design-cdn](../../../../domains/system-design/drills/problems/design-cdn.md)。

## S2. Kindle / 电子书阅读器多设备同步

- 题面：JC-860888（L5 **Bar Raiser** 设计轮，2026-07，1point3acres 转述）与 KV1lzmtlt："Design Kindle reader"（离线、多设备阅读进度、**幂等 API、冲突解决**）。当事人失败原因：**"过于关注底层实现细节，而没有持续从 Customer Experience / 高层设计 / 取舍角度展开"**（forums.md §3.4）。
- 需求要点：离线阅读；多设备同步阅读进度、书签、批注；书库购买/下载；设备 ID；弱网。
- 数据模型 `推断`：按用户分区的变更日志 `Change(user_id, seq, device_id, op_id, type, payload, client_ts)`；阅读进度是"每本书一条当前值"，批注是"追加 + 软删除"。
- 关键决策：
  1. **客户端操作带 `op_id`**（幂等）；服务端按 `(user_id, op_id)` 去重；同步 API 是"上传本地待发送变更 + 拉取 `seq > cursor` 的远端变更"，游标单调（见 [networking-cursor-vs-offset-pagination](../../../../domains/system-design/cards/networking/networking-cursor-vs-offset-pagination.md)）。
  2. **冲突策略按数据类型区分**（这是 BR 想听到的"客户体验取舍"）：阅读进度——取"最远页"还是"最后阅读的设备"？这是产品选择，两种都合理，可以把选择权交给用户（提示"跳到最远页吗？"）；批注——合并（集合并，删除用墓碑）；用 LWW 时说明设备时钟不可信，改用服务端接收序或版本向量（[distributed-lww-danger](../../../../domains/system-design/cards/distributed/distributed-lww-danger.md)、[distributed-offline-client-writes](../../../../domains/system-design/cards/distributed/distributed-offline-client-writes.md)）。
  3. **推送**：一个设备改了进度，通过推送通知其他设备"有新变更"，设备再用游标拉取；推送丢了也不影响正确性（下次打开必拉）。
  4. **内容分发**：书文件走 CDN + 预签名 URL + DRM 许可证；元数据小、内容大，分开存储与扩缩。
  5. 冷启动/重装：全量快照 + 增量游标。
- 追问：一个用户 10 台设备同时在线；服务端收到的变更时间戳倒退；GDPR 删除；弱网下的分块上传；热点用户（无，按用户分区自然均匀）。
- 题库近邻：[design-file-sync](../../../../domains/system-design/drills/problems/design-file-sync.md)（游标日志 vs Merkle）、[design-google-docs](../../../../domains/system-design/drills/problems/design-google-docs.md)（OT/CRDT）、[design-notification-system](../../../../domains/system-design/drills/problems/design-notification-system.md)。

## S3. 日志存储 / 日志与监控系统

- 题面：LC6801242（AWS Dublin SDE2，2025-06）"design a log storage"；LC6397223（AWS L5）"design a logging and monitoring system"。
- 需求要点：海量日志写入（至少一次、允许少量重复）；按时间范围 + 服务 + 关键字/trace id 查询；保留期与成本；多租户。
- 数据流 `推断`：应用 agent（本地磁盘缓冲，断网不丢）→ 区域收集器（批量、压缩）→ 分区日志（Kinesis 类）→ 写入器按 `(租户, 服务, 小时)` 聚成 128 MB+ 的压缩块落对象存储 → 索引层。
- 关键决策：
  1. **索引取舍**：全文倒排索引贵（写放大、内存）；常见做法是**稀疏索引**——按 `(服务, 时间窗)` 记块位置 + 每块的布隆过滤器/字段统计，查询先剪枝块再扫描；热数据（最近几小时）才建倒排索引。成本是"扫描量"，与 Athena 同理（见 `problems/serverless_query_over_s3.md`）。
  2. **去重**：`(source_id, seq)` 为幂等键；下游容忍重复或在写块时去重。
  3. **背压与丢弃策略**：agent 缓冲满了先丢低优先级（debug）；收集器过载 → 限流返回 429，agent 带抖动退避（[aws-timeouts-retries-jitter](../../../../domains/system-design/readings/aws-timeouts-retries-jitter.md)）。
  4. **保留分层**：热（SSD/索引）→ 温（对象存储标准）→ 冷（归档），生命周期策略；合规保留与删除。
  5. **多租户**：每租户摄取配额；查询并发与扫描预算；shuffle sharding 到写入器（[aws-shuffle-sharding](../../../../domains/system-design/readings/aws-shuffle-sharding.md)）。
- 追问：日志里的敏感信息；跨区域查询；时钟偏差下的排序（事件时间 vs 接收时间）。
- 题库近邻：[design-metrics-monitoring](../../../../domains/system-design/drills/problems/design-metrics-monitoring.md)、[design-message-queue](../../../../domains/system-design/drills/problems/design-message-queue.md)；新题 `problems/metrics_timeseries_store.md`、`problems/data_lake_ingestion_catalog.md`。

## S4. 员工目录（DynamoDB 分区键选择）

- 题面：LC8528370（电话面，2026-09）"Design an Employee Directory for Amazon … ~1M employees … Read-heavy"，并要求给出 **DynamoDB schema 的分区键**。
- 先算数（估算接回设计）：1M 员工 × 约 2 KB ≈ 2 GB——**一台机器就装得下**。所以选 DynamoDB 的理由是运维和可用性而不是容量；说出这一点是 senior 信号。
- 访问模式（先列出来再设计键）`推断`：按 `employee_id` 查；按姓名前缀搜索；列某经理的直接下属；列整个部门；向上追溯管理链（org chart）。
- 设计：
  - 主表：分区键 `employee_id`（高基数、均匀）。**不要**用 `department` 当分区键：部门大小悬殊，热分区（[distributed-data-skew-vs-access-skew](../../../../domains/system-design/cards/distributed/distributed-data-skew-vs-access-skew.md)；DynamoDB 论文 §4 的热分区故事）。
  - GSI：`manager_id → employee_id`（直接下属）；`department → employee_id`（按需，分区键加盐或限制大小）。GSI 异步更新，**写后读索引可能陈旧**，要在需求里说明（[distributed-global-index-staleness](../../../../domains/system-design/cards/distributed/distributed-global-index-staleness.md)）。
  - 管理链：向上追溯用迭代 `GetItem` 沿 `manager_id` 走（深度很浅，≤20）；整棵子树用**物化路径**（`/ceo/vp/dir/mgr`）字段 + 前缀查询，或预计算闭包表（写放大换读快）。
  - 姓名搜索：不适合直接放 DynamoDB → 旁挂搜索服务（OpenSearch）通过 **CDC/Streams** 同步（呼应 `problems/cdc_replication_pipeline.md`）。
  - 读多：DAX/ElastiCache；员工变更少，TTL + 变更事件失效。
- 追问：谁能看到谁（权限，按字段过滤）；组织重组时批量更新经理字段（批处理幂等）；多区域读。
- 题库近邻：[design-key-value-store](../../../../domains/system-design/drills/problems/design-key-value-store.md)、[storage-wide-column-modeling](../../../../domains/system-design/cards/storage/storage-wide-column-modeling.md)、[debrie-single-table-design](../../../../domains/system-design/readings/debrie-single-table-design.md)。

## S5. 设备管理 / 配置同步 / OTA（"管理成千上万台设备"）

- 题面：JC-amz445（AWS HM，2026-07）"a system to manage thousands of devices"；LC7910016 / LC8519174："config sync / backup（full、diff、log 三种备份）"。
- 需求要点：设备注册与身份（证书）、在线状态、下发配置/命令、批量升级（OTA）、遥测上报。
- 设计骨架 `推断`：
  1. **期望状态 vs 报告状态（device shadow）**：控制面存"期望配置 + 版本号"，设备上报"实际配置 + 版本号"；设备上线后对比版本、自行拉取差异——**水平触发（level-triggered）而不是边沿触发**，掉线期间错过的命令不丢（对应 `problems/managed_db_control_plane.md` §4.1 的 reconcile）。
  2. **命令至少一次 + ack + 幂等**；命令带过期时间。
  3. **心跳与在线状态**：设备数 × 心跳频率决定写入量（100 万设备 × 每 60 s ≈ 1.7 万次/s），用 TTL 键或聚合写入，不要每次心跳都落强一致库；**重连风暴**：大面积断线后同时重连 → 设备端指数退避 + 抖动，服务端接入层限流。
  4. **分波次升级（OTA）**：1% → 5% → 25% → 100%，每波有 bake time 和自动回滚阈值——直接套用 Builders' Library《Automating safe, hands-off deployments》的 one-box / waves / bake（见 `00_how_to_run_the_round.md` §7.1）。
  5. **备份三种类型**：full（整体）、diff（相对上一次 full 的差异）、log（持续的变更日志）；恢复 = 最近 full + 对应 diff + 重放 log（与 `problems/managed_db_control_plane.md` §4.5 的 PITR 同构）。
- 追问：证书轮换；设备时钟不可信；弱网下的大文件分块断点续传；多租户（每客户设备配额）。
- 题库近邻：[design-job-scheduler](../../../../domains/system-design/drills/problems/design-job-scheduler.md)、[design-notification-system](../../../../domains/system-design/drills/problems/design-notification-system.md)。

## S6. 评论与评分（Reviews & Ratings）

- 题面：LC6394206 / LC6735161（Bluescape 白板 HLD：电商商品页的评论与评分部分，按 功能/非功能需求 → 实体 → API → 深挖 的结构）。
- 要点 `推断`：
  1. **写入**：每用户每商品一条评论（唯一键 `(product_id, user_id)` + 条件写，编辑 = 覆盖并保留历史）；幂等 `client_token`。
  2. **聚合（平均分、数量、星级直方图）**：不要每次读都扫所有评论。写入时发事件，**流式增量更新**聚合（分片计数器防热点商品：一个爆款的计数器拆成 N 个分片，读时求和），最终一致；展示端容忍秒级到分钟级延迟。
  3. **列表**：按"最有帮助 / 最新"排序，游标分页；"有帮助"投票是高频小写入 → 分片计数 + 批量落库。
  4. **反作弊/审核**：异步管线（垃圾、刷单），审核前状态 `pending`，只对作者可见。
  5. **读路径**：商品页读聚合（缓存/预计算），评论正文分页懒加载；读写比极高。
- 追问：删除/编辑如何修正聚合（发负事件，幂等）；国际化；"已验证购买"标识（跨服务 join 用事件冗余，避免同步调用）。
- 题库近邻：[design-e-commerce](../../../../domains/system-design/drills/problems/design-e-commerce.md)、[design-leaderboard](../../../../domains/system-design/drills/problems/design-leaderboard.md)（计数与排序）、[design-news-feed](../../../../domains/system-design/drills/problems/design-news-feed.md)。
