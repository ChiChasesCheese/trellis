# 题 5：托管数据库的多租户控制面（RDS / Aurora 风格：开通、备份、故障切换）

> 题库里最近的是 [design-job-scheduler](../../../../../domains/system-design/drills/problems/design-job-scheduler.md)（调度与 fencing）、[design-lock-service](../../../../../domains/system-design/drills/problems/design-lock-service.md)（租约与选主）、[design-key-value-store](../../../../../domains/system-design/drills/problems/design-key-value-store.md)（副本与分区），但没有"为百万个数据库实例做控制面"的题。
> 本题几乎是 AWS Data Services 岗位的原型问题：**"build and operate cloud-native distributed systems"**。先读 `../00_ddia_refresh.md` §2、§5，以及 `../00_how_to_run_the_round.md` §5、§7。
> 复习：[distributed-failover-mechanics](../../../../../domains/system-design/cards/distributed/distributed-failover-mechanics.md)、[distributed-fencing-tokens](../../../../../domains/system-design/cards/distributed/distributed-fencing-tokens.md)、[distributed-failure-detection](../../../../../domains/system-design/cards/distributed/distributed-failure-detection.md)、[distributed-new-follower-setup](../../../../../domains/system-design/cards/distributed/distributed-new-follower-setup.md)、
> [reliability-rpo-vs-rto](../../../../../domains/system-design/cards/reliability/reliability-rpo-vs-rto.md)、[reliability-untested-failover](../../../../../domains/system-design/cards/reliability/reliability-untested-failover.md)、[reliability-gray-failure](../../../../../domains/system-design/cards/reliability/reliability-gray-failure.md)、[correctness-saga-orchestrator-recovery](../../../../../domains/system-design/cards/correctness/correctness-saga-orchestrator-recovery.md)、[infra-k8s-primitives](../../../../../domains/system-design/cards/infra/infra-k8s-primitives.md)（reconcile 循环思想）。
> 研究依据（2026-10-15 抓取）：RDS Multi-AZ 概述 https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html ；
> RDS 故障切换 https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html ；RDS 时间点恢复 https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html ；
> Aurora SIGMOD'17、DynamoDB ATC'22（autoadmin、备份、故障检测）；Builders' Library（Fairness、Static stability、Automating safe deployments）；Well-Architected cell-based architecture。

## 1. 题面

> "设计一个**托管关系型数据库服务的控制面**。客户通过 API 创建数据库实例、修改规格、开启自动备份和多可用区高可用、从备份还原到某个时间点。
> 服务同时管理**百万级**数据库实例，跨多个区域。重点说明：开通（provisioning）、备份与还原、故障切换（failover），以及如何在多租户下保证可靠、安全、可运维。"

## 2. 需求

**控制面 API（低频、强一致、需审计）**
`CreateDBInstance(client_token, engine, class, storage, multi_az, …)`、`ModifyDBInstance`、`DeleteDBInstance`、`RestoreDBInstanceToPointInTime`、`CreateSnapshot`、`RebootDBInstance(force_failover)`、`DescribeDBInstances`（分页）。

**数据面（不属于本题，但控制面要管）**：真正运行数据库引擎的主机；客户的应用通过**端点（endpoint）**连接。

**非功能**
- **开通成功率**与时延（创建几分钟内可用，p99 受容量/依赖影响）。
- **故障切换（Multi-AZ）**：文档数字——典型 **60–120 秒**（取决于数据库活动，大事务或长恢复会延长）；RPO ≈ 0（同步复制到另一个 AZ 的 standby）。
- **备份**：自动备份 + 事务日志持续上传（RDS 文档：**每 5 分钟**上传事务日志到 S3，点时间恢复用"快照 + 重放日志"）；备份不能影响线上性能与可用性。
- **隔离**：一个客户的 API 风暴 / 一个坏实例 / 一个坏发布不能影响其他客户；**爆炸半径可量化**。
- **安全**：每实例独立的加密密钥（KMS）、网络隔离（VPC）、最小权限；控制面不能读客户数据。
- **可运维**：每个操作可审计、可重入、可观测；on-call 能一键定位"卡在哪一步"。

**非目标**：数据库引擎内部实现；查询优化；跨引擎迁移。

## 3. 估算（脚本）

假设 **100 万**个数据库实例，平均 100 GB。

| 量 | 计算 | 结果 |
|---|---|---|
| 心跳/健康上报 | 每实例每 10 s | **10 万次/s**（控制面 + 监控的写入）|
| 总存储 | 10^6 × 100 GB | **100 PB** |
| 每日变更量 | 5% | **5 PB/天 ≈ 58 GB/s** 的 WAL/增量备份上传 |
| 日志对象数 | 每实例每 5 分钟 1 个 | 每天 **2.88 亿**个对象 → S3 前缀分散与 PUT 速率（≥3,500 写/s/前缀）要设计 |
| 创建/修改速率 | 每天 2% 的实例有创建或重要变更 | 约 **0.23 次/s** —— 控制面写**很少**；高频的是心跳和读 |
| 一个 AZ 故障 | 1/3 实例需切换 | **33 万实例**；要在 2 分钟内完成 ≈ **2,800 次切换决策/s** |
| 99.99% 可用性 | 一年 | 52.6 分钟不可用预算 → 一次 60–120 秒的切换就吃掉 2–4% 的年预算 |

**这些数字改变的设计**：(1) 控制面的"写"很少但"读"和心跳极多 → 状态机/元数据写走强一致小库，心跳走**独立的、可丢的、聚合型的路径**；
(2) **AZ 级故障时，切换决策会瞬间放大 3 个数量级**（从偶发到 2,800/s）→ 切换逻辑必须是**数据面本地、自治**的，不能依赖那时最拥挤的中心控制面（静态稳定）；
(3) 日志上传 2.88 亿对象/天 → 必须有分片/前缀设计与批量化。

## 4. 标准答案

### 4.1 控制面 vs 数据面：先画边界（本题的"题眼"）

```
                     控制面 (Control plane)                                       数据面 (Data plane)
客户 ─▶ API 前端 ─▶ 工作流引擎 ─▶ 期望状态库 ──(下发/拉取)──▶  主机 agent ─▶ 数据库引擎进程 (主/备)  ◀── 客户应用(经 endpoint)
        │幂等/配额/鉴权  │状态机,可重入   │ 强一致,带版本      │ 本地缓存"期望配置"         │ ▲ 同步复制/共享存储
        ▼              ▼              ▲                    │ 上报 实际状态+心跳 ───────▶  监控/健康系统 (独立, 可丢)
   审计日志        放置服务(选主机/AZ)  │ reconcile 循环      ▼
                                       └── 观察者对比 期望 vs 实际 → 触发修复
```
**铁律**：数据面在控制面完全不可用时**仍然继续服务**（客户的数据库不能因为我们的 API 挂了就停）。控制面可以降级成"不能创建/修改"，但不能让已有实例不可用。
这是 Builders' Library《Static stability using Availability Zones》的原则（控制面是"做变更的机器"，数据面是"每次请求用的机器"）。

### 4.2 数据模型（期望状态 + 实际状态）

```
DBInstance (instance_id PK, account_id, desired{engine, class, storage, multi_az, backup_retention…}, desired_version,
            observed{status, host_id, az, endpoint, last_heartbeat}, workflow_id, owner_lease, fencing_token, created_at)
Placement  (host_id PK, az, free_capacity{cpu, mem, iops, slots}, state ∈ {active, draining, retired})
Backup     (instance_id, backup_id, type ∈ {snapshot, log}, start_lsn, end_lsn, s3_uri, checksum, created_at, retained_until)
Workflow   (workflow_id PK, instance_id, type, step, status, attempt, last_error)    ← 每步幂等,可从 step 继续
```
- 存储：强一致 KV（DynamoDB 风格：条件写、事务），分区键 `account_id` 或 `instance_id`（见 §4.7 的 cell 化）。
- **期望版本 `desired_version` + 乐观并发控制**：`ModifyDBInstance` 用 `UPDATE … WHERE desired_version = ?`，并发修改的第二个调用得到冲突错误，而不是静默覆盖。
- **`client_token`** 使 `CreateDBInstance` 重试幂等：同一 token + 相同参数返回同一个实例；相同 token 不同参数 → 报错（卡 [correctness-idempotency-payload-hash](../../../../../domains/system-design/cards/correctness/correctness-idempotency-payload-hash.md)）。

### 4.3 开通（Provisioning）：用 Saga 把"创建"拆成可重入的步骤（第一个深挖）

```
CreateDBInstance 请求
  1. 校验 + 配额检查(账号实例数/总存储)       ← 失败立刻返回 4xx, 不进入工作流
  2. 写 DBInstance(状态=creating) + 创建 Workflow  (一个事务/条件写, 带 client_token 去重)
  3. 放置: 选 AZ 与主机 (见 §4.4)         ── 预留容量(带 TTL 的预留,避免泄漏)
  4. 创建存储卷 / 分配加密密钥(KMS)        ── 每步记录 "已完成+产物 id"
  5. 在主机上启动引擎(agent 拉取期望状态)
  6. 配置网络: ENI、安全组、DNS 端点
  7. 健康检查通过 → 状态=available;若 multi_az: 同时创建 standby 并等待同步完成
  失败: 逐步补偿(释放预留→删卷→删密钥)，状态=failed + 原因; 补偿本身也必须幂等、可重试
```
要点：
- **每一步幂等**，工作流引擎崩溃后从 `Workflow.step` 继续（卡 [correctness-saga-orchestrator-recovery](../../../../../domains/system-design/cards/correctness/correctness-saga-orchestrator-recovery.md)、[correctness-saga-compensation-limits](../../../../../domains/system-design/cards/correctness/correctness-saga-compensation-limits.md)）。
- **步骤的外部副作用用确定性 id**：如用 `instance_id` 作为卷的幂等 token（`CreateVolume(client_token=instance_id)`），重放不产生第二个卷。这是 Builders' Library《Timeouts, retries, backoff》里对 `RunInstances` 的 client token 做法。
- **泄漏防护**：预留带 TTL；定期**对账（reconciliation）**：云账单/资源清单里"有资源但数据库无记录"的孤儿由 GC 回收（[correctness-reconciliation](../../../../../domains/system-design/cards/correctness/correctness-reconciliation.md)）。
- **超时与预算**：整个创建有总超时；每步重试带抖动退避，并有"最大尝试次数→失败并告警"，避免无限卡死。
- **进度可观测**：`DescribeDBInstances` 返回 `status` 与当前 `step`；on-call 看工作流表就知道卡在哪。

### 4.4 放置（Placement）：多租户装箱 + AZ 分散
- 目标：把实例放到有容量的主机上，**同一客户的主/备在不同 AZ**，同一主机不过度超配；尽量降低"噪声邻居"。
- 容量是**多维**的（CPU、内存、IOPS、网络、存储槽位）→ 装箱问题（Builders' Library《Fairness in multi-tenant systems》把它类比为 bin-packing，并指出高级公平系统会预测哪些工作负载可以友好共存）。
- 放置服务是**热点依赖**：创建风暴时所有请求争抢同一份"空闲容量"视图 → 做成**分片 + 乐观预留**（按 AZ/主机池分片；预留用 CAS；冲突就换下一个候选），避免全局锁。
- DynamoDB 的经验可借鉴：存储节点自己监控吞吐/容量，超过阈值就向 autoadmin 上报"建议迁走的副本"，由中心找新位置（[DDB22] §4.3）——**由数据面上报、控制面决策**。

### 4.5 备份与还原（第二个深挖）

**三层保护**（类比 DynamoDB 的 WAL 归档 + 快照 + 持续校验，[DDB22] §5）：
1. **持续日志归档**：引擎 WAL/binlog 持续上传到 S3（RDS 文档：每 5 分钟上传事务日志），文件带 **manifest（实例、起止 LSN）与校验和**；归档前验证"无序号空洞"（DynamoDB 论文：归档代理检查序号无空洞、校验和、属于正确分区后才上传）。
2. **周期快照**：增量快照（块级变更）；快照周期可由"累积日志量"触发，而不只按时间（DynamoDB 做法：按累积的 WAL 量决定快照频率）。
3. **还原 = 最近快照 + 重放日志到目标时间点**（点时间恢复 PITR）。恢复到**新实例**（不覆盖原实例），避免误操作二次伤害。

**关键性质**
- 备份**不影响线上**：从 standby 或存储层快照取，不在主库上做重 I/O（Aurora 中备份是存储层的连续、增量行为，[AUR17]；Multi-AZ 文档也写到同步 standby 能"minimize latency spikes during system backups"）。
- **最新可还原时间（LatestRestorableTime）** 是一个对客户可见的、可观测的承诺；日志上传停滞时它会停止前进 → 要告警。
- **验证**：备份没验证过就等于没有备份。定期**自动还原抽样实例到隔离环境**，校验引擎可启动、校验和一致（DynamoDB 的 scrub 思想）。
- **保留与删除**：保留期过后删除；客户删除实例时可选保留最终快照。合规删除要考虑备份中的残留。
- **加密与访问**：备份用实例密钥加密；控制面工作流只拿到"还原权限"而非明文数据；跨区域复制备份是 DR 能力（RPO 取决于复制延迟）。
- **规模**：58 GB/s 的上传，需要在 S3 上按 `(instance_hash, 日期)` 分散前缀；PUT 批量化（把多个小日志合并为一个对象）。

### 4.6 故障切换（Failover，第三个深挖：最容易挖深）

**架构（Multi-AZ 实例）**：主库在 AZ-A，**同步复制**到 AZ-B 的 standby（RDS 文档：synchronous standby in a different AZ；写提交需要 standby 确认 → 提交延迟略增）。客户通过**端点（DNS 名）**连接；切换后端点指向新主库（文档里关于 JVM DNS TTL 的提示说明这一点）。

```
健康检查 (多个独立观察者) ──▶ 判定主库不可用 ──▶ 隔离旧主(fencing) ──▶ 提升 standby ──▶ 更新端点 ──▶ 新建新 standby(后台)
```

**1. 如何判定"主库挂了"（避免误切）**
- 单一观察者会因自己网络问题误判；用**多个独立观察者投票**（不同 AZ 的监控节点 + 主机 agent 自报 + 存储层信号），多数同意才切。
- DynamoDB 同样的经验：follower 发起选举前先问其他副本"你能连上 leader 吗？"，有人说能就放弃，**显著减少误选举**（[DDB22] §6.2）。
- **灰色故障（gray failure）**：主库进程在、心跳正常，但查询极慢或磁盘卡死 → 需要**深度健康检查**（真实的读写探针、慢查询比例），而不仅是 TCP/心跳。切换条件要包含"客户视角的失败率"。
- **抖动保护**：设置冷却时间和最大切换频率，避免来回切换（flapping）。

**2. 防脑裂：旧主必须被 fencing（最重要）**
- 触发切换后，旧主可能只是网络不通（仍在接收部分客户写入）。必须保证它**不再接受写**：
  - 存储层 fencing：给卷发 **fencing token / epoch**，存储拒绝携带旧 epoch 的写（卡 [distributed-fencing-tokens](../../../../../domains/system-design/cards/distributed/distributed-fencing-tokens.md)；Aurora 的做法是用 epoch 编号给恢复过程的截断范围版本化，[AUR17] §4.3）；
  - 同步复制天然限制：旧主要提交需 standby 确认，standby 已提升并拒绝旧主 → 旧主的新提交无法完成；
  - 兜底：强制关闭旧主所在主机/实例（STONITH）。
- **租约**：主库持有"我是主库"的租约，租约到期且未续期则自行降级只读；新主必须等旧主租约过期后才对外服务（DynamoDB：新 leader 等旧 leader 租约过期；部署时 leader 主动让位可省去等待，[DDB22] §6.2、§6.4）。

**3. 提升 standby**
- 同步复制 → standby 数据不落后（RPO≈0）；异步（跨区域只读副本）→ 选**日志位置最新**的副本，并告知客户可能丢失的窗口。
- 引擎做崩溃恢复（重放未应用的日志）——这就是文档说"大事务或长恢复会延长故障切换时间"的原因。

**4. 切换端点**
- DNS 切换受 **TTL 与客户端缓存**影响（长连接池、JVM DNS 缓存）；缓解：低 TTL、驱动程序重新解析、或使用**代理层/端点代理**把客户连接与实际主机解耦（代价：多一跳延迟与新的故障点）。
- 切换期间客户看到连接断开；应用需要**重试 + 幂等**（卡 [reliability-retryable-errors](../../../../../domains/system-design/cards/reliability/reliability-retryable-errors.md)）。

**5. 谁来执行切换？——静态稳定的关键**
- **不要让切换依赖控制面 API/工作流引擎在 AZ 故障的拥堵时刻可用。** 设计成两级：
  - **数据面本地自治**：每个复制组有本地的"仲裁者/监控器"（跨 AZ 部署，持有租约与缓存的元数据），在控制面不可达时也能依据规则完成切换；
  - 控制面事后**对账**：观察到端点/角色变化后更新元数据、补建新 standby。
- 大面积故障（整个 AZ）时切换风暴：限速 + 优先级（付费 SLA 高者优先）+ 分批，防止新主机的容量/存储 API 被冲垮（对应 §3 的 2,800 次/s）。

**6. 切换后**
- 在新 AZ 重建 standby（可能要几十分钟~几小时的数据拷贝），期间处于"无冗余"状态 → 需要**告警与指标**，并优先修复。
- 记录**切换事件**（原因、耗时、数据丢失窗口）供客户和内部复盘。

**7. 演练**
- 未经演练的故障切换等于没有（[reliability-untested-failover](../../../../../domains/system-design/cards/reliability/reliability-untested-failover.md)）。定期对随机实例做**强制故障切换**（`RebootDBInstance(force_failover)`），把结果当作 SLO 指标。

### 4.7 多租户、爆炸半径与运维

**API 层公平**（Builders' Library《Fairness in multi-tenant systems》）：
- 控制面 API 与数据面 API 分别限流；控制面按**账号**配额（令牌桶），超限 `ThrottlingException` + `Retry-After`。
- 昂贵 API（`DescribeDBInstances` 全量列表）有分页 + 缓存 + 批量导出替代，避免"轮询风暴"。

**Cell 化**（Well-Architected：cell-based architecture）
- 按 `account_id` 把控制面切成 **cell**：每个 cell 拥有自己的元数据库、工作流引擎、放置服务与主机池，**不共享状态**；前面一层极薄的 **cell router** 按账号路由。
- 文档算术：10 个 cell → 一个 cell 故障时 90% 请求不受影响。坏发布、毒丸请求（某账号的畸形参数触发工作流死循环）被限制在一个 cell。
- 代价：容量碎片化；跨 cell 操作（跨账号共享快照）要专门设计；cell 路由表本身要极稳。

**Shuffle sharding 在 cell 内**：工作流 worker、放置服务实例对账号做 shuffle shard，坏账号只影响与它共享全部 worker 的极少数账号（8 选 2 → 28 种组合；Route 53 用 2048 选 4 → 约 7300 亿种）。

**发布安全**（Builders' Library《Automating safe, hands-off deployments》）
- 控制面与 agent 软件：one-box（≤10% 流量）→ 逐 cell/AZ 波次 → bake time → 自动回滚（监控聚合告警）；整体 4–5 个工作日铺到所有区域。
- **agent 与控制面之间的协议演进用"先读后写"**（DynamoDB read-write deployment，[DDB22] §6.4），回滚安全。
- **引擎补丁/维护窗口**是最频繁的客户可感知事件：用 Multi-AZ 切换实现"几乎零停机"补丁（先给 standby 打补丁→切换→再给旧主打补丁），并安排在客户设定的维护窗口。

**可观测**
- 控制面指标：API 成功率与延迟（按分位）、工作流各步耗时、卡住的工作流数量、孤儿资源数、放置冲突率。
- 数据面指标：每实例健康、复制延迟、`LatestRestorableTime`、切换次数/耗时。
- **canary**：每个 cell、每个 AZ 持续创建/删除一个"金丝雀"数据库，端到端验证开通/备份/还原/切换（DynamoDB 用从每个 AZ 访问每个公共端点的 canary 发现灰色故障，[DDB22] §6.3）。
- 客户面告警（CFA）：以**客户感知的失败率**为准。

**安全**
- 控制面使用**角色/临时凭证**操作客户账号内的资源（跨账号 assume role），最小权限；所有操作写不可变审计日志。
- 数据库管理员凭证由客户持有；控制面不存明文。
- 加密密钥：每实例数据密钥由 KMS 主密钥加密（信封加密）；KMS 不可用时，已运行实例应继续运行（缓存解密后的数据密钥——静态稳定；DynamoDB 对 IAM/KMS 的做法见 [DDB22] §6.5）。

## 5. 追问与答案

**Q1. 工作流引擎在"创建卷"之后崩溃了，重启会创建第二个卷吗？**
A：不会。`CreateVolume` 带 `client_token = instance_id + step`，卷服务按 token 去重；工作流在每步结束时记录产物 id，重启后读取 `Workflow.step` 继续，并先查询"该 token 是否已有产物"。同时有对账任务回收孤儿。

**Q2. 如何避免故障切换时的脑裂？**
A：§4.6：多观察者判定 + 存储层 epoch fencing + 租约 + 同步复制提交需 standby 确认 + 兜底 STONITH。核心不变量：**任一时刻只有一个主库可以提交写**；提升 standby 之前必须先让旧主不能写，或证明其租约已过期。

**Q3. 整个 AZ 挂了，33 万个实例同时切换，会发生什么？**
A：切换风暴会冲击放置服务、存储 API、DNS 更新与新 standby 的重建。对策：(1) 切换由数据面本地仲裁者执行，不经过中心控制面；(2) 提前留好容量（静态稳定：新主在存活 AZ 里的主机上已存在 standby，不需要现场开通）；(3) 重建新 standby 的工作限速并排队（优先级）；(4) 对 DNS 更新做批量与退避。

**Q4. 怎么知道备份真的能用？**
A：自动还原演练：每天抽样还原到隔离环境，校验引擎能启动、行数/校验和一致，并记录还原耗时作为 RTO 指标；监控 `LatestRestorableTime` 的滞后；归档前校验日志序号无空洞。

**Q5. 客户把数据库删了，30 秒后后悔了。**
A：删除默认**软删除/保留最终快照**（可配置）。工作流把 `status=deleting`，并保留元数据与最后快照 N 天；真正的资源回收由延迟任务执行。若客户选择"不保留"，则只有备份保留期内的自动备份能救（语义需要明确告知）。

**Q6. 同一个账号并发 `ModifyDBInstance` 两次（一次改规格，一次改存储）怎么办？**
A：每个实例同一时间只允许一个"改变资源形态"的工作流（用租约+`workflow_id` 抢占）；第二次请求要么排队、要么返回 `InvalidDBInstanceState`。通过 `desired_version` CAS 防止覆盖。要的是**可预期的语义**，而不是静默合并。

**Q7. 控制面本身要怎么升级而不影响已有数据库？**
A：数据面不依赖控制面进程；控制面按 cell 灰度；agent 协议先读后写；元数据 schema 变更走 expand/contract（[architecture-expand-contract](../../../../../domains/system-design/cards/architecture/architecture-expand-contract.md)）；每次发布前跑升级/降级测试。

**Q8. 你怎么证明故障切换在 120 秒内？**
A：把切换分段计时（检测、fencing、提升、引擎恢复、端点更新），各段都有指标；每个 cell 持续金丝雀强制切换；在压测中注入"大事务正在进行"。承诺值用分位（p99），而不是平均。

**Q9. 成本压力：怎样把更多实例塞在同一台主机？**
A：基于真实使用率的**超配（over-subscription）**+ 预测共存性 + 主机级隔离（cgroup/微虚拟机）+ 压力超阈值自动迁移（DynamoDB：节点超过阈值就上报候选副本移走）。风险：噪声邻居 → 必须有公平机制与迁移能力。

**Q10. 为什么不用一个全局的大控制面？**
A：爆炸半径是 100%；规模上限由单个元数据库决定；发布风险无法分段。Cell 化把任何故障限制在 1/N，且易于灰度与回滚。代价是复杂度与碎片化，但对于"所有客户都依赖它"的服务这是必须付出的。

## 6. 评分表

| 维度 | Strong | OK | Weak |
|---|---|---|---|
| 边界 | 明确控制面/数据面，强调数据面静态稳定；期望状态+reconcile | 分层但无原则 | 一个"数据库服务"黑盒 |
| 开通 | Saga/工作流、每步幂等、client token、预留 TTL、对账回收 | 队列+worker | 同步调用链，失败留半成品 |
| 备份 | 日志归档+快照+PITR；manifest/校验和/无空洞；还原演练；LatestRestorableTime | 说"每天快照" | 只有快照，或者从主库做重备份 |
| 故障切换 | 多观察者、灰色故障、fencing/epoch/租约、同步复制 RPO≈0、端点切换与 DNS 缓存、切换本地自治 | 心跳+提升 standby | 忽略脑裂 |
| 多租户 | 配额/限流、cell、shuffle sharding、放置装箱 | 提到限流 | 无隔离 |
| 运维 | one-box/波次/bake/回滚、金丝雀、CFA、切换演练、协议先读后写 | 监控报警 | 无 |
| 数字意识 | 用心跳 10 万/s、58 GB/s、AZ 故障 2,800 次/s 驱动设计 | 有估算 | 没有 |

**Senior 常见失分点**：把切换放在需要中心控制面的路径上；忘了 fencing；备份只有快照没有日志；没有对账；用单个全局元数据库。

## 7. 与题库的关系
- [design-job-scheduler](../../../../../domains/system-design/drills/problems/design-job-scheduler.md)（工作流/租约）、[design-lock-service](../../../../../domains/system-design/drills/problems/design-lock-service.md)（fencing）、[design-key-value-store](../../../../../domains/system-design/drills/problems/design-key-value-store.md)（副本）、[design-object-storage](../../../../../domains/system-design/drills/problems/design-object-storage.md)（备份落地）、[design-metrics-monitoring](../../../../../domains/system-design/drills/problems/design-metrics-monitoring.md)（健康信号）。
- 阅读：[aws-static-stability](../../../../../domains/system-design/readings/aws-static-stability.md)、[aws-shuffle-sharding](../../../../../domains/system-design/readings/aws-shuffle-sharding.md)、[aws-leader-election](../../../../../domains/system-design/readings/aws-leader-election.md)、[postgres-high-availability](../../../../../domains/system-design/readings/postgres-high-availability.md)。
