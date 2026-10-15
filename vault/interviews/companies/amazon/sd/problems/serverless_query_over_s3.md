# 题 4：S3 之上的无服务器 SQL 查询（Athena 风格）

> 题库里没有这道题（分析型查询引擎不在 47 题内；相关概念散落在 `analytics.*` 卡里）。
> 先读 `../00_ddia_refresh.md` §7，复习：[analytics-row-vs-column-layout](../../../../../domains/system-design/cards/analytics/analytics-row-vs-column-layout.md)、[analytics-columnar-compression](../../../../../domains/system-design/cards/analytics/analytics-columnar-compression.md)、[analytics-vectorized-execution](../../../../../domains/system-design/cards/analytics/analytics-vectorized-execution.md)、
> [analytics-join-strategies](../../../../../domains/system-design/cards/analytics/analytics-join-strategies.md)、[analytics-shuffle-mechanics](../../../../../domains/system-design/cards/analytics/analytics-shuffle-mechanics.md)、[analytics-skew-stragglers](../../../../../domains/system-design/cards/analytics/analytics-skew-stragglers.md)、[storage-multipart-ranged-io](../../../../../domains/system-design/cards/storage/storage-multipart-ranged-io.md)。
> 研究依据（2026-10-15 抓取）：Athena 列存格式 https://docs.aws.amazon.com/athena/latest/ug/columnar-storage.html ；Athena 数据优化（分区、投影、小文件）https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html ；
> Athena 分区 https://docs.aws.amazon.com/athena/latest/ug/partitions.html ；Parquet 格式 https://parquet.apache.org/docs/file-format/ ；S3 请求速率 https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html ；ClickHouse VLDB 论文剪藏 [clickhouse-vldb-paper](../../../../../domains/system-design/readings/clickhouse-vldb-paper.md)（列存执行参照）。

## 1. 题面

> "设计一个**无服务器交互式查询服务**：用户把数据放在 S3 上（Parquet、ORC、CSV、JSON），在目录里登记表，然后直接提交 SQL。
> 没有集群需要用户创建或管理，按**扫描的数据量**付费。目标：扫描 1 TB 的查询在几十秒内返回，同时服务成千上万个并发的用户。"

## 2. 需求

**功能**：提交 SQL（SELECT / 聚合 / JOIN / 窗口函数）；查看状态、取消、取结果（结果落地到 S3 并可分页读取）；读取目录中的表和分区；`CREATE TABLE AS SELECT`（把数据转成列存）。

**非功能**
- **延迟**：交互式（秒到几十秒），支持长查询（分钟到小时）；**p50 与 p99 的比值要可控**（尾部由 straggler 和 S3 抖动决定）。
- **弹性**：零查询时成本为零；一个用户的 1 万 vCPU 瞬时突发不应要求其预置。
- **多租户隔离**：一个用户的重查询不能饿死别人；对每个账号有并发上限与配额。
- **正确性**：读到的是一致的快照（表格式提交原子；没有"一半新一半旧"）。
- **计费可预测**：按扫描字节计费 → 引擎要**精确统计扫描量**，并且提供降低扫描量的手段（列存、分区、统计）。

**非目标**：低于 100 ms 的点查；写入事务（除 CTAS/INSERT）；跨查询的常驻缓存集群（可作为优化）。

## 3. 估算（脚本）

场景：一个扫描 **10 TB** 原始数据的查询，目标 **60 秒**内完成。

| 量 | 计算 | 结果 |
|---|---|---|
| 所需聚合读吞吐 | 10 TB ÷ 60 s | **167 GB/s** |
| worker 数 | 每个 worker 从 S3 的有效读速率假设 125 MB/s（`推断`：单实例可达更高，这里保守，含解码）| ≈ **1,334 个并行 worker** |
| S3 GET 数 | 每次 8 MB 范围读 → 10 TB ÷ 8 MB | **125 万次 GET**，≈ **2.1 万 GET/s** |
| 需要的前缀数 | S3 每前缀 ≥5,500 读/s（[S3PERF]）| 至少 **4 个前缀** → 数据布局/分区直接影响能否打满吞吐；否则出现 503 Slow Down |
| 剪枝后 | 分区裁剪 + 列裁剪 + 行组统计，砍掉 99% | 只扫 **100 GB** → 约 1 秒级读取（同样 1,334 worker）|
| 列裁剪收益 | 表 100 列、查 3 列、Parquet 压缩约 4 倍（`推断`）| 读取量约原始的 **0.75%** |

**这些数字改变的设计**：(1) 瓶颈是 **S3 吞吐与 GET 请求速率**，不是 CPU；(2) 查询时间 ∝ 扫描量 ÷ 并行度，所以**剪枝（少读）比加机器更划算**；
(3) 1,300 个 worker 要在一两秒内"凭空"出现 → 需要**预热的共享 worker 池**，而不是每个查询冷启动一堆容器。

## 4. 标准答案

### 4.1 总体架构

```
客户 SQL ─▶ API 前端(鉴权/配额/排队)
              │
              ▼
         ┌──────────────┐  元数据   ┌────────────┐
         │  协调器       │◀────────▶│ 目录 (表/分区/统计) │   *规划阶段*: 解析 → 绑定 → 优化 → 分区裁剪 → 文件级裁剪
         │ (每查询一个)  │          └────────────┘
         └──────┬───────┘
                │ 生成分布式执行计划 = 若干 *阶段(stage)*, 每阶段若干 *任务(task)*
                ▼
   ┌────────────────────────────────────────────────────────┐
   │ 共享 worker 池 (预热的微虚拟机/容器, 多租户, 按需扩缩)   │
   │   Stage 3: Final agg  ◀── shuffle ──  Stage 2: Partial agg  ◀── Stage 1: Scan splits (S3 range GET) │
   └────────────────────────────────────────────────────────┘
                │  结果写 S3 (客户的结果前缀)  +  元数据(扫描字节, 耗时)
                ▼
            结果/计费记录
```

### 4.2 规划阶段：在读到第一个字节之前就把 99% 的数据排除（第一个深挖）

1. **分区裁剪（partition pruning）**：WHERE 命中分区键 → 只列出匹配分区。Athena 文档："If you query a partitioned table and specify the partition in the WHERE clause, Athena scans the data only from that partition"。
   目录里可能有**数百万个分区** → 分区查找本身成为瓶颈：
   - 目录分区索引（Glue partition index：没有索引时加载全部分区再过滤）；
   - **分区投影（partition projection）**：分区信息不存目录，而存成"规则"（如日期范围、整数范围），规划时在**内存里计算**要读的分区，不去查目录。文档同时警告：稀疏表会产生大量对空前缀的 S3 `LIST`，而缺少某个分区键的谓词会使用整个范围（比如 100 万个取值就是 100 万次 LIST）。
2. **分区粒度的取舍**（文档原则）："optimize for the most common queries and avoid optimizing for rare queries"：天级查询不要按小时分区；**按时间戳排序**的列存文件对短时间窗几乎和小时分区一样高效；过多分区键导致碎片化小文件。
3. **文件级/行组级裁剪**：Parquet 文件 = 若干行组 → 每列一个列块；**footer 存 schema 与每列块的 min/max 统计**。规划/执行时读 footer（对象末尾的一次小范围 GET），用谓词跳过整个行组。Athena 文档称之为 predicate pushdown。
   表格式（Iceberg）更进一步：manifest 里就有**文件级**统计，规划阶段不必打开文件即可跳过（见题 2）。
4. **列裁剪（projection）**：只读被引用的列块 → 这是列存最大的收益（§3：0.75%）。
5. **统计信息与基数估计**：目录/表格式里的行数、NDV、min/max → 决定 **join 顺序与策略**（广播 vs 分区哈希）。统计过期 → 计划变差，但不影响正确性。
6. **小文件与 `LIST` 成本**：规划要列文件；百万个小文件使规划本身要几十秒（文档："Avoid having too many files"）。服务端要有**文件清单缓存**，并鼓励（或自动）合并。

### 4.3 执行：split → task → stage

- **split（分片）**：一个 split = 一个文件的一段（通常对齐到 Parquet 行组或 64–128 MB）。协调器把 split 分配给 worker，**拉取式调度**（worker 做完再要下一个）→ 天然负载均衡，抵抗 straggler。
- **扫描任务**：对每个 split 并发发 `Range GET` 读取需要的列块（几个列块合并成一次较大的读以减少请求数）；解码为**列批（vectorized batch）**；应用谓词；输出到下一阶段。
- **阶段间数据交换（exchange / shuffle）**：
  - **聚合**：每个扫描任务先做 **partial aggregation**（本地预聚合），再按 group key 哈希重分区到 final aggregation（减少 shuffle 数据量）。
  - **JOIN**：小表 → **广播**（broadcast）到所有 probe worker；两个大表 → 双方按 join key 哈希分区（**shuffle hash join**）。选择依据是统计信息。
  - **倾斜**：热门 key 使某个 task 远慢于其他（[analytics-skew-stragglers](../../../../../domains/system-design/cards/analytics/analytics-skew-stragglers.md)）→ 对热 key 单独拆分/加盐，或做自适应重分区。
- **shuffle 的存储**：交换数据先放内存和本地盘；容量不足时**溢写到 S3**（慢但可容错）。把 shuffle 数据放在 S3 还有一个好处：它是**可持久的中间结果**，下游任务失败可只重做下游（"阶段级重试"），不必从头执行。

### 4.4 容错与长尾（第二个深挖）

| 问题 | 机制 |
|---|---|
| worker 崩溃/被回收 | 任务**幂等**：输入 split 不可变（对象不可变 / 快照固定）→ 重新调度到另一 worker 即可；输出以 `(query, stage, task, attempt)` 命名，只有成功 attempt 的输出被采用 |
| straggler（慢任务）| **推测执行**：任务耗时超过同阶段中位数的 k 倍时，在另一台 worker 启动副本，先完成者胜；败者取消。代价：多 5–10% 计算 |
| S3 503 Slow Down / 抖动 | 带**抖动的指数退避**重试 GET；限制每个查询的 GET 并发；跨多个前缀分散；对热点对象做请求合并 |
| 协调器崩溃 | 查询状态（计划、已完成阶段）定期写入持久存储；新协调器可接管；否则查询失败重提（对交互式短查询可接受）|
| 内存不足 | spill 到本地盘/S3；超限则只失败该查询（**爆炸半径 = 一个查询**），而不是 worker |
| 数据在查询中途被覆盖 | 表格式快照固定读版本；对无事务的 Hive 风格目录，**提交前后读到混合数据**是已知风险，需要在文档中明确 |

### 4.5 多租户与"无服务器"的资源模型（第三个深挖）

**核心矛盾**：无服务器 = 用户不预置资源；但 1,300 个 worker 不可能在 1 秒内冷启动。
- **预热共享池**：持续保持一池热 worker（微虚拟机，隔离性强、启动快；Builders' Library《Fairness in multi-tenant systems》写明 AWS Lambda 在亚秒级粒度共享计算资源，并用 Firecracker 轻量虚拟化做隔离；本地阅读 [aws-shuffle-sharding](../../../../../domains/system-design/readings/aws-shuffle-sharding.md) 同系列）。
  池大小按**历史需求预测 + 余量**，自动扩缩，目标利用率 50–70%（余量留给突发，利用率-排队延迟曲线，[foundations-utilization-latency-knee](../../../../../domains/system-design/cards/foundations/foundations-utilization-latency-knee.md)）。
- **配额与公平**：每账号**并发查询数**、**每查询最大 worker 数**、**每账号每秒 DML/DDL**；超限排队（有上限）或拒绝；队列按账号公平调度（加权轮询），避免大账号独占。
- **隔离**：worker 内部按查询**沙箱隔离**；每查询的 S3 凭证是**限定到其有权前缀的临时凭证**（见题 2 的凭证发放），绝不让 worker 持有全桶权限。
- **容量预留**（可选产品）：愿意付费的客户获得专属 worker 配额，隔离"吵闹邻居"（DynamoDB 的预留/隔离思想，[DDB22] §4）。
- **爆炸半径**：协调器与 worker 池按 **cell**（账号哈希）划分；发布走 one-box → cell 逐个 → bake。

### 4.6 成本与计费模型：按扫描量计费意味着什么

> 来源说明：Athena 官方文档称 "serverless … you pay only for the queries you run"（https://docs.aws.amazon.com/athena/latest/ug/what-is.html ，2026-10-15 抓取）；SQL 查询按扫描数据量计费（定价页另有 Provisioned Capacity 按计算计费的选项）；定价页示例按 $5/TB 计算（3 TB 未压缩文本 = $15；GZIP 后 1 TB = $5；Parquet+压缩只读一列 0.25 TB = $1.25，说明计费的是实际读取的压缩/列裁剪后字节），实际单价按区域而异，面试里不要报具体单价（来源：https://aws.amazon.com/athena/pricing/ ，经 r.jina.ai 镜像读取，2026-10-15 核对）。

- 计费字节 = **实际从 S3 读取的字节**（压缩后的列块字节，而非解压后），所以：列存、压缩、列裁剪、分区裁剪、行组跳过**直接降低客户账单**，也是产品的核心卖点。
- 引擎必须**精确且可审计**地统计每查询的扫描量；失败/取消的查询要有明确计费规则（例如失败的不收费，取消的按已扫描收费）。
- 服务端的成本是：worker 计算 + S3 请求数 + 数据传输。**S3 GET 请求数**随范围读的粒度增大而下降：8 MB 比 1 MB 少 8 倍请求（请求费与速率限制都受益），但裁剪粒度变粗。要在两者间取舍。
- 防滥用：`SELECT *` 对 100 列表是 0.75%→100% 的差别；提供"预估扫描量"与账号级预算上限。

### 4.7 结果与交互
- 结果写入客户 S3 前缀（分段并发写，最后合并成 manifest），API 返回结果位置与分页 token；小结果可直接内联返回。
- **结果复用缓存**：相同 SQL + 相同表快照版本 + 相同参数 → 返回缓存结果（安全，因为快照不可变）；失效键 = 表元数据版本。命中即**零扫描**。
- 查询取消：协调器通知所有 task 终止；已发出的 S3 请求无法收回，但结果丢弃。

## 5. 追问与答案

**Q1. 表有 500 万个分区，规划就要 30 秒，怎么办？**
A：(1) 目录分区索引；(2) 分区投影——规则计算，不查目录（注意稀疏表产生空 LIST）；(3) 换表格式，让 manifest 承担裁剪；(4) 降低分区粒度（天级而非小时级）并按时间戳排序；(5) 合并小分区。

**Q2. 查询只用 3 列，为什么 Parquet 的 `SELECT *` 仍然很慢？**
A：`SELECT *` 要读全部 100 个列块，扫描量是列裁剪后的约 130 倍（§3 的 0.75% 对比 100%）。列存只在你只取需要的列时才有优势；这也是计费上的直接损失。

**Q3. 一个 join 的两侧都是 5 TB，怎么执行？**
A：shuffle hash join：双方按 join key 哈希到 N 个分区，每个分区在一个 task 内建哈希表（小的一侧）并探测。要点：(1) 先各自做过滤和列裁剪，减少 shuffle 量；(2) N 取大一些，避免单分区超内存；(3) 倾斜 key 拆分；(4) 若一侧经过滤后变小 → 改为广播（自适应执行，在运行时根据实际大小切换）。

**Q4. 怎么解决 straggler？**
A：拉取式小 split + 推测执行 + 在阶段末尾"拆小任务"。还要排查根因：热分区（倾斜）、慢 S3 对象（重试/换前缀）、慢 worker（灰色故障 → 摘除）。

**Q5. S3 的 503 Slow Down 怎么避免？**
A：(1) 数据布局分散到多个前缀；(2) 范围读粒度足够大（8 MB 而非 64 KB）；(3) 退避重试；(4) 查询级并发限速；(5) 对重复读取的热对象在 worker 池本地缓存。S3 官方说明自动扩容是渐进的，期间会出现 503（[S3PERF]）。

**Q6. 如何保证用户读到一致的数据？**
A：对表格式表，查询开始时固定一个**快照 id**，整个查询只读该快照引用的文件。对 Hive 风格目录没有这个保证，文件可能在查询途中被替换 → 在产品上用"写入先写临时前缀再原子改目录指针"的惯例，并告知用户。

**Q7. 并发 1 万个查询，worker 池怎么扩缩？**
A：协调器按需向调度器申请"槽位"，调度器把需求（排队长度 × 每查询所需并行度）作为扩容信号；缩容保守（避免抖动）；容量预测使用历史+日历特征；突发超出池容量时先排队（有上限），超过排队上限则限流并返回明确错误（load shedding，而非让所有查询一起变慢）。

**Q8. 为什么交互式查询不直接用 DynamoDB/OLTP 数据库？**
A：访问模式是大范围扫描+聚合，OLTP 的行存/B-tree 会读取全部列、随机 I/O，也无法按"扫描量"弹性扩展；而 S3 + 列存 + 无状态计算把存储与计算分离，各自独立扩缩（卡 [storage-compute-separation](../../../../../domains/system-design/cards/storage/storage-compute-separation.md)）。

**Q9. 怎样支持"最近 5 分钟的新数据也能查到"？**
A：依赖摄取层（题 2）把新文件原子提交进表元数据；查询规划时读取最新快照。小文件多 → 读放大，所以最新的数据以小文件形式存在，旧数据已合并。不要让查询引擎自己维护写路径。

**Q10. 如何证明引擎没有读错数据？**
A：黄金查询集（对固定快照的查询，结果哈希固定）、新旧版本并行"影子执行"比对、对 shuffle 的校验和；这与 DynamoDB 持续校验思想一致（[DDB22] §5.3）。

## 6. 评分表

| 维度 | Strong | OK | Weak |
|---|---|---|---|
| 瓶颈判断 | 用 167 GB/s、2.1 万 GET/s 推出瓶颈在 S3 与扫描量；强调"少读"优先于"加机器" | 知道列存快 | 认为靠加 CPU |
| 规划 | 分区裁剪+投影、行组统计、列裁剪、统计信息；知道分区粒度的取舍和 LIST 成本 | 说"分区" | 无规划阶段概念 |
| 执行 | split 拉取调度、partial agg、broadcast vs shuffle join、倾斜处理 | MapReduce 式描述 | 单机执行 |
| 容错 | 幂等 task、推测执行、阶段级重试、S3 退避 | 重试 | 失败则整查询重跑且不提 |
| 无服务器与多租户 | 预热池、公平调度、沙箱、临时凭证、cell | 提到容器 | 每查询冷启动一堆 VM |
| 成本模型 | 按扫描字节计费的含义，用格式/分区降本 | 提到成本 | 无 |
| 取舍 | 请求粒度 vs 裁剪粒度；预热余量 vs 成本；推测执行额外开销 | 被动 | 无 |

**Senior 常见失分点**：忽略 S3 请求速率限制；忘了倾斜；没有 worker 池预热就谈"无服务器"；分区越细越好。

## 7. 与题库的关系
- 先做 [design-object-storage](../../../../../domains/system-design/drills/problems/design-object-storage.md)（S3 如何分区与扩展）；[design-top-k](../../../../../domains/system-design/drills/problems/design-top-k.md)（近似聚合）；[design-ad-click-aggregation](../../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)（批流结合）。
- 阅读：[clickhouse-vldb-paper](../../../../../domains/system-design/readings/clickhouse-vldb-paper.md)、[spark-rdd-paper](../../../../../domains/system-design/readings/spark-rdd-paper.md)、[iceberg-table-format](../../../../../domains/system-design/readings/iceberg-table-format.md)。
