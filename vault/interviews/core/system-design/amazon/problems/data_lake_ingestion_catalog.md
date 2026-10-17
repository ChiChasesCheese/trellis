# 题 2：数据湖摄取 + 数据目录（Glue / Lake Formation 风格）

> 题库里没有这道题（最近的是 [design-file-sync](../../../../../domains/system-design/drills/problems/design-file-sync.md) 的内容寻址分块和 [design-object-storage](../../../../../domains/system-design/drills/problems/design-object-storage.md) 的元数据分片，但没有"表级元数据 + 治理"）。
> 先读 `../00_ddia_refresh.md` §7（批/流、列存、分区裁剪、表格式），复习卡 [analytics-lake-vs-warehouse-vs-lakehouse](../../../../../domains/system-design/cards/analytics/analytics-lake-vs-warehouse-vs-lakehouse.md)、[analytics-table-formats](../../../../../domains/system-design/cards/analytics/analytics-table-formats.md)、[analytics-lakehouse-compaction](../../../../../domains/system-design/cards/analytics/analytics-lakehouse-compaction.md)、[analytics-lakehouse-snapshot-isolation](../../../../../domains/system-design/cards/analytics/analytics-lakehouse-snapshot-isolation.md)。
> 研究依据（2026-10-15 抓取）：Glue 概念 https://docs.aws.amazon.com/glue/latest/dg/components-key-concepts.html ；Glue 分区索引 https://docs.aws.amazon.com/glue/latest/dg/partition-indexes.html ；
> Lake Formation https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html ；Athena 分区 https://docs.aws.amazon.com/athena/latest/ug/partitions.html ；S3 性能 https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html 。

## 1. 题面

> "设计一个**托管数据湖服务**：客户把来自应用日志、数据库 CDC、批量文件上传、流（Kinesis/Kafka）的数据持续写进对象存储；
> 服务负责把原始数据变成**可查询的、有 schema 的、有权限控制的表**，并提供一个**中心化目录（catalog）**让各种查询引擎（Athena、EMR、Redshift Spectrum）都能发现这些表。"

## 2. 需求

**功能**
1. **摄取**：流式微批 + 批文件两种入口，落到 S3 "原始区（raw/bronze）"，再整理为"规整区（curated/silver）"的列存表（Parquet）。
2. **目录**：数据库 → 表 → 分区 → schema 版本；支持 schema 发现（爬取文件推断，Glue crawler 的角色）与显式注册。
3. **事务性表**：并发写入与读取互不影响；失败的摄取不会让读者看到半成品；支持 upsert/delete（合规删除）。
4. **治理**：库/表/列/行级权限；跨账号共享；审计日志。（Lake Formation 文档：权限在 Athena、Redshift Spectrum、EMR、Glue 等引擎上以列、行、单元格粒度强制。）
5. **维护**：小文件合并、过期快照清理、孤儿文件回收、统计信息。

**非功能**
- 摄取**至少一次**，对外表现为**恰好一次**（重复摄取同一文件不产生重复行）。
- 新数据对查询可见的延迟：流 1–5 分钟，批文件 <1 分钟（数字是我设的目标，面试时与面试官确认）。
- 目录读 QPS 高、写 QPS 低；目录必须**强一致读**（引擎规划查询时要看到刚提交的分区）。
- 规模：数千张表、数 PB/天、多账号多租户。

**非目标**：实时 OLAP 毫秒级查询（那是 ClickHouse/Druid 类）；数据血缘的完整产品化；跨区域复制（追问）。

## 3. 估算（脚本算出）

| 量 | 计算 | 结果 |
|---|---|---|
| 总摄取量 | 200 TB/天 | **2.3 GB/s** |
| 目标文件大小 | 256 MB（Athena 文档建议 Parquet 行组 128 MB 量级；文件目标 `推断`：128 MB–1 GB）| 78 万文件/天 |
| **小文件问题** | 5,000 张低流量表，每分钟 flush 一次 | 5,000 × 1,440 = **720 万个小文件/天**，一年 **26 亿** |
| 分区数 | 2,000 张表 × 每小时一个分区 × 3 年 | **5,256 万**分区；若再加 10 个 region 分区 → **5.3 亿** |
| 查询规划 | 每次查询要拿分区列表 | 无索引就是全量加载分区，再在客户端过滤（Glue 文档原话）|

**这些数字改变的设计**：(1) 小文件必然出现 → **必须有自动合并**；(2) 分区数达亿级 → 目录要有**分区索引/元数据下推**，或者改用"表格式把文件清单放在对象存储里的元数据文件"以绕开目录瓶颈；
(3) S3 请求速率（每前缀 3,500 写/5,500 读每秒，[S3PERF]）→ 目录布局和读并行度要和前缀对应。

## 4. 标准答案

### 4.1 分层与数据流

```
 来源                      摄取层                         存储 (S3)                       目录/治理               查询
┌────────┐    ┌──────────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────┐  ┌──────────┐
│ 日志   │──▶ │ 流缓冲(Kinesis/Kafka)     │   │ raw/   原样落盘, 按到达时间   │   │ Catalog 服务      │  │ Athena   │
│ CDC    │──▶ │ 微批写入器(每 N 分钟/MB)  │──▶│ curated/ Parquet, 分区 + 排序 │◀──│ 库/表/分区/schema │◀─│ EMR      │
│ 批文件 │──▶ │ 批摄取工作流(文件清单)    │   │ _metadata/ 表格式元数据(快照) │   │ 权限(列/行/单元格)│  │ Redshift │
└────────┘    └──────────────────────────┘   └──────────────────────────────┘   │ 凭证发放(vending) │  └──────────┘
                      │ 提交 = 原子切换元数据指针                                  └──────────────────┘
                      ▼
               后台维护: 合并小文件 / 过期快照 / 孤儿文件回收 / 统计信息
```

### 4.2 摄取：幂等 + 原子提交（本题第一个深挖）

**目标**：同一个批次被执行两次，表里只出现一份数据；失败的批次对读者不可见。

1. **文件级账本（ingestion ledger）**：每个源文件（或流的 offset 区间）在摄取前登记 `(source_id, file_key, etag/offset_range)`；
   用**条件写**（`attribute_not_exists`）抢占登记，已登记过的批次直接跳过。（对应卡 [correctness-idempotency-key-design](../../../../../domains/system-design/cards/correctness/correctness-idempotency-key-design.md)、[analytics-idempotent-reruns](../../../../../domains/system-design/cards/analytics/analytics-idempotent-reruns.md)。）
2. **先写数据文件，后提交元数据**：写入器把 Parquet 文件写到 S3 的**确定性路径**（含批次 id），**不会被读者看到**——因为读者只通过元数据找文件。
3. **提交 = 原子地把表的"当前元数据指针"从 v 改为 v+1**（乐观并发控制，CAS）：
   - 做法 1：目录服务里存"表当前元数据文件位置"，提交是目录里一次条件更新。
   - 做法 2：纯 S3 做法，用 S3 条件写（`If-None-Match` 创建 `v+1.metadata.json`，已存在则失败）实现 CAS，见卡 [storage-s3-conditional-writes](../../../../../domains/system-design/cards/storage/storage-s3-conditional-writes.md)。
   - 冲突时（另一个写入器先提交）：重新读最新元数据，**检查自己写的文件与新提交是否冲突**（同一分区的覆盖才冲突；追加互不冲突），无冲突就基于 v+1 重试提交。
4. **失败的批次留下孤儿文件**（数据文件写了但没提交）→ 后台**孤儿文件回收**：扫描前缀下"不被任何快照引用且超过 N 天"的文件删除。N 要大于最长摄取任务时间，否则会误删进行中的批次。
5. **延迟数据与分区**：按**事件时间**分区而非到达时间，则迟到事件会落到旧分区，改变旧分区 → 每次提交会触发"重写分区"或追加小文件。折中：写入按到达时间追加，由合并任务按事件时间重新聚簇。

### 4.3 表格式：为什么需要（Iceberg / Delta 风格，卡 [analytics-table-formats](../../../../../domains/system-design/cards/analytics/analytics-table-formats.md)）

没有表格式，S3 上的"目录 + Parquet 文件"有三个问题：(1) `LIST` 慢且最终一致历史包袱；(2) 一次摄取写多个文件不是原子的；(3) 改 schema、改分区要重写数据。
表格式的核心结构：
```
catalog 指针 ──▶ metadata.json (表 schema + 分区规格 + 快照列表)
                    └─▶ snapshot N ──▶ manifest list ──▶ manifest 文件(每个列出若干数据文件 + 每文件的列统计 min/max/null 数)
                                                                  └─▶ data 文件 (Parquet)
```
- **查询规划不再 LIST 目录**：读 manifest（几十 MB 的元数据），利用**文件级 min/max 统计**直接跳过不相关文件，这比分区裁剪更细。
- **快照 = 时间旅行 + 快照隔离**：读者固定读一个快照，写入器并发提交新快照，互不影响（[analytics-lakehouse-snapshot-isolation](../../../../../domains/system-design/cards/analytics/analytics-lakehouse-snapshot-isolation.md)）。
- **隐藏分区**：分区规格是元数据，查询写 `WHERE ts > …` 即可裁剪，用户不必知道目录结构；改分区规格不需要重写旧数据。
- **行级删除**（合规）：写"删除文件"（位置删除/相等删除），读时合并（merge-on-read），之后合并任务再物化（copy-on-write）。

### 4.4 目录服务（Catalog）本身怎么设计（第二个深挖）

**数据模型**
```
Database(account_id, db_name)                 Table(db_id, table_name, current_metadata_pointer, owner, params…)
Partition(table_id, partition_values[], location, stats, schema_version)    SchemaVersion(table_id, version, columns[])
PermissionGrant(principal, resource(db|table|column|row filter), privileges[])
```
- **存储**：强一致 KV（DynamoDB 风格）。分区键 `table_id`，排序键 `partition_values` 的有序编码 → 分区列表是**范围扫描**；这样"按前缀裁剪"（如 `year=2026/month=10`）是一次范围查询。
- **分区过滤下推**：引擎调用 `GetPartitions(expression)`；Glue 文档说明：没有分区索引时，Glue 会加载表的**全部分区**再用表达式过滤，分区数增长时越来越慢；有索引时只取子集。
  → 目录要为"分区键前缀的任意组合"提供**可配置的二级索引**（每个索引 = 一组有序键），代价是写放大（每个分区每个索引多一条记录）。
- **规模应对**：5,256 万分区（见 §3）。若全部按 `table_id` 分区，单张大表的分区会成为**热分区**（DynamoDB 的"热分区/吞吐稀释"教训，[DDB22] §4）。
  解法：对超大表按 `(table_id, hash(partition_prefix) mod K)` 加盐分片；或把大表的分区信息**下沉到表格式的 manifest**，目录只存一个指针 —— 目录负载与分区数脱钩。这是现代数据湖转向表格式的主要动机之一。
- **缓存**：引擎侧缓存表元数据，用 `metadata_pointer` 的版本号校验（ETag 式条件读）。
- **可用性**：目录是所有查询的前置依赖 → 数据面（读取数据）不应依赖目录的**写**路径；目录读路径多 AZ，客户端缓存+重试带抖动；目录宕机时，已缓存元数据的引擎继续工作（静态稳定）。

### 4.5 Schema 发现与演进

- **爬取（crawler）**：采样文件推断 schema，写入目录。Glue 文档：爬虫"连接数据源、推断 schema、在 Data Catalog 创建表定义"。
  成本与风险：爬取全前缀代价高 → 只爬**新增前缀**（增量爬取，记录已见分区）；推断可能把偶发的脏数据当 schema → 需要**人工确认 / 兼容性检查**才发布新版本。
- **兼容性规则**（[architecture-schema-compat-rules](../../../../../domains/system-design/cards/architecture/architecture-schema-compat-rules.md)）：加可空列 = 向后兼容；删列/改类型 = 破坏性 → 新 schema 版本需要通过**兼容性检查**才能提交；
  表格式用**列 ID** 而非列名定位列，所以重命名不需要重写数据（[analytics-table-formats](../../../../../domains/system-design/cards/analytics/analytics-table-formats.md)）。
- **Parquet 内部结构**（Apache Parquet 文档，2026-10-15 抓取）：文件 = 行组（row group）→ 每列一个列块（column chunk）→ 页（page）；**文件尾部有 footer 含 schema 与每个列块的统计**，所以查询先读 footer（一次小范围读），再按需读相关列块。

### 4.6 治理与访问控制（Lake Formation 的角色）

```
引擎(Athena) ──请求读表──▶ Catalog/权限服务: 校验 principal 对 table/column/row 的权限
                                │ 通过: 返回 *临时凭证* (只能访问该表对应 S3 前缀) + 行/列过滤规则
                                ▼
                           引擎用临时凭证读 S3，并按规则过滤列/行
```
- 核心思想：**授权在目录，数据留在 S3**，引擎永远拿不到"全桶权限"，只拿到**限定前缀、限时的凭证**（credential vending）。
- 行级/列级过滤要**由受信任的执行环境强制**（否则引擎里的用户代码可以直接读 S3 绕过）。这是 Lake Formation 文档强调"augments IAM"的原因。
- 跨账号共享：授权记录指向 owner 账号的资源；审计日志记录每次凭证发放（谁、何时、哪张表）。
- 合规删除（GDPR）：按用户 id 删除 → 表格式 delete file + 异步重写；对**备份/快照**也要有保留期，使被删数据在 N 天内彻底消失。

### 4.7 后台维护（决定长期成本的"非功能"）

| 任务 | 做什么 | 触发 | 风险与对策 |
|---|---|---|---|
| 合并小文件 | 把同分区的小文件重写成 256 MB 左右、按常用过滤列排序/聚簇 | 小文件数/占比超阈值 | 与摄取并发 → 用同样的乐观提交；冲突则放弃重试（摄取优先）|
| 快照过期 | 删除超过保留期的旧快照元数据 | 定时 | 保留期要大于最长查询时间；时间旅行需求决定下限 |
| 孤儿文件回收 | 删除不被任何快照引用的数据文件 | 定时 | 必须有"年龄"保护，避免误删进行中的写 |
| 统计信息 | 更新文件/列统计、分区统计 | 提交后异步 | 过期统计只影响计划质量，不影响正确性 |

维护任务本身要做成**常量工作**风格：按固定节奏、固定预算运行，而不是"数据多了就多干"，防止它在摄取高峰时与摄取抢资源（Builders' Library《Reliability, constant work》）。

### 4.8 多租户与爆炸半径
- 目录按 `account_id` 分 **cell**（router 按账号路由），一个 cell 的坏发布只影响该 cell 的账号。
- 摄取与维护 worker 池按账号 **shuffle sharding**；配额：每账号并发作业数、每秒目录写、每表分区数上限。
- 限流策略区分：目录**读**（数据面，弹性）与**写/DDL**（控制面，严格配额）。

## 5. 追问与答案

**Q1. 两个写入器同时往同一张表提交，会发生什么？**
A：各自写完数据文件后争着把元数据指针从 v 改为 v+1，只有一个 CAS 成功。输家读取新元数据，检查自己的文件与 v+1 的变更是否冲突：纯追加到不同文件不冲突，直接基于 v+1 重新提交；若两者都**覆盖同一分区**则冲突，输家失败并按策略重试整个批次（因批次幂等所以安全）。

**Q2. 查询执行到一半，另一个任务合并了小文件并删除了旧文件，查询会失败吗？**
A：不会，只要**物理删除晚于快照过期**。合并只产生新快照；旧文件仍被旧快照引用。只有在快照过期（保留期过后）且无活跃查询使用它之后，孤儿回收才会删除。保留期必须大于最长查询时长。

**Q3. 分区数涨到 5 亿，目录扛不住，怎么办？**
A：(1) 先加分区索引，把"全量加载再过滤"变成范围查询；(2) 对超大表盐化分片避免热分区；(3) 根本办法：用表格式，分区文件清单放进 manifest（按需读取、带文件级统计），目录只存指针；(4) 限制分区粒度（别按分钟分区），用隐藏分区+聚簇代替超细分区。

**Q4. 流式摄取 1 分钟一次 flush，会不会制造海量小文件？**
A：会（720 万/天，§3）。办法：(1) 低流量表**拉长 flush 间隔**或按"字节数或时间，先到者"触发；(2) 摄取层按 `(表, 分区)` **先聚合再写**；(3) 写入时接受小文件，由后台合并器在分区"冷却"后合并成大文件；(4) 查询侧依赖文件级统计跳过，小文件的代价主要是 LIST/GET 次数与元数据。

**Q5. 如何保证"新数据 5 分钟内可查"同时不制造小文件？**
A：这是延迟 vs 文件大小的权衡。两层存储：热层（最近 5 分钟的小文件，查询时与大文件一起读；元数据里有标签）+ 冷层（合并后的大文件）。查询在两层都读，合并后原子替换。代价：读放大，维护复杂。

**Q6. 目录里一张表被误删，怎么恢复？**
A：目录元数据变更**也是日志**：对每次变更写不可变的审计日志（谁、何时、旧值/新值），软删除（标记删除，保留 N 天），定期快照目录并归档到 S3；恢复 = 取消软删除或回放日志。数据文件在 S3 并未删除（删表只删元数据，除非 purge）。

**Q7. 权限变更（撤销某用户的访问）多久生效？**
A：凭证是限时发放的，生效延迟 ≤ 凭证有效期（如 15 分钟）+ 引擎缓存。要更快就缩短有效期，代价是目录请求量上升；严重事件提供"立刻吊销"通道（撤销令牌表，引擎每次规划时检查）。

**Q8. 怎么做数据质量？**
A：摄取管线中的**隔离区**：解析失败/违反约束的记录写到 `quarantine/` 并计数，达到阈值则暂停提交；不要让坏数据悄悄进入 curated 表。质量规则（非空、范围、唯一性）作为提交前检查，结果入表级指标。

**Q9. 成本从哪来，怎么降？**
A：S3 存储（分层到冷存储、生命周期）、请求数（小文件、LIST）、查询扫描量（列存+分区+排序聚簇）、爬取与维护计算。最高杠杆的三项：列存+压缩、合并小文件、按常用过滤列聚簇。Amazon 的 Frugality。

## 6. 评分表

| 维度 | Strong | OK | Weak |
|---|---|---|---|
| 摄取正确性 | 文件账本 + 确定性路径 + CAS 提交 + 孤儿回收；解释幂等 | 说"去重" | 直接写目标目录，失败留半成品 |
| 表元数据 | 能画 metadata→manifest→data，讲文件级统计与快照隔离 | 知道 Iceberg 名字 | 只有"按日期分目录" |
| 目录设计 | 分区索引/盐化/下沉到 manifest；强一致读；缓存校验；cell 化 | 一张表存分区 | 忽略分区规模 |
| 小文件 | 给出数量级（720 万/天）并有触发+合并+并发提交方案 | 知道要合并 | 没意识到 |
| 治理 | 目录授权 + 凭证发放；列/行强制在可信环境；撤销延迟权衡 | 提到 IAM | 把权限只放在 S3 bucket policy |
| 多租户与运维 | shuffle sharding、配额、数据面/控制面分开、维护任务常量工作 | 提到配额 | 无 |
| 取舍 | 延迟 vs 文件大小、分区粒度 vs 元数据量、爬取成本 | 单一方案 | 无 |

**Senior 常见失分点**：说"把文件写进 S3 就完了"；把目录当成数据库的一张表而不谈分区规模；没有幂等；忘了删除/合规。

## 7. 与题库的关系
- [design-object-storage](../../../../../domains/system-design/drills/problems/design-object-storage.md)（S3 本体怎么做）、[design-file-sync](../../../../../domains/system-design/drills/problems/design-file-sync.md)（内容寻址与去重）、[design-ad-click-aggregation](../../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)（对账与迟到数据）。
- 更进一步：[iceberg-table-format](../../../../../domains/system-design/readings/iceberg-table-format.md)、[map:analytics.warehouse](../../../../../domains/system-design/map/analytics.warehouse.md)。
