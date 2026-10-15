# 题 3：托管时序 / 指标存储 + 降采样（CloudWatch Metrics 风格）

> 与题库的关系：[design-metrics-monitoring](../../../../../domains/system-design/drills/problems/design-metrics-monitoring.md)（题解 [solution-metrics-monitoring](../../../../../domains/system-design/readings/problems/solution-metrics-monitoring.md)）是**自建监控系统**（采集、告警、仪表盘）。
> 本题是它的"云厂商版"：**多租户托管服务**，重点是 **保留分层 + 降采样**、**统计量可聚合性（百分位怎么办）**、**基数（cardinality）治理**、**租户隔离**。
> 先把题库那道做完再来。复习卡：[problems-metrics-monitoring-downsampling-keep-min-max](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-downsampling-keep-min-max.md)、[problems-metrics-monitoring-cardinality-not-sample-rate](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-cardinality-not-sample-rate.md)、
> [problems-metrics-monitoring-cardinality-admission-quota](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-cardinality-admission-quota.md)、[problems-metrics-monitoring-noisy-tenant-isolation](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-noisy-tenant-isolation.md)、[reliability-metric-cardinality](../../../../../domains/system-design/cards/reliability/reliability-metric-cardinality.md)、[reliability-percentile-aggregation](../../../../../domains/system-design/cards/reliability/reliability-percentile-aggregation.md)。
> 研究依据（2026-10-15 抓取）：CloudWatch 概念与保留 https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html ；
> PutMetricData https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html ；Gorilla（VLDB 2015）https://www.vldb.org/pvldb/vol8/p1816-teller.pdf 。

## 1. 题面

> "设计一个**托管的指标服务**。客户（成千上万个账号）通过 API 上报带维度的时间序列数据点；
> 服务保存它们，按时间范围和统计量（平均、最大、求和、百分位）查询，并在数据变老时自动降低分辨率；还要支持基于指标的告警。"

## 2. 需求

**功能**
1. `PutMetricData(namespace, metric_name, dimensions{k:v}, timestamp, value | statistic_set | (values, counts))`。
2. `GetMetricData(queries, start, end, period, stat)`：按维度过滤、按 `period` 聚合；支持百分位（p50/p99/p99.9）。
3. **保留分层与自动降采样**（CloudWatch 的真实做法，文档逐字）：
   - 周期 <60 秒的数据点保留 **3 小时**；60 秒周期保留 **15 天**；300 秒保留 **63 天**；3600 秒保留 **455 天（15 个月）**。
   - 初始以较短周期发布的数据会被聚合用于长期存储：15 天后 1 分钟数据只能以 5 分钟分辨率取回，63 天后只能以 1 小时分辨率取回。
4. 告警：对一个指标的统计量在窗口上设阈值，状态机 OK / ALARM / INSUFFICIENT_DATA。
5. 列表 API：`ListMetrics`（按命名空间、维度前缀）。

**非功能**
- 写：高吞吐、**尾延迟低**、可丢极少量但不可悄悄丢（要有可观测的丢弃计数）。
- 读：最近数据 p99 < 数百毫秒；长跨度查询（几个月）可以慢，但要有上限。
- **多租户**：一个账号的基数爆炸或查询风暴不得拖垮他人。
- 可用性：写路径的可用性高于读路径；**告警评估路径独立于查询路径**（见 §4.8）。
- 持久性：已确认写入的数据点不丢（至少 3 副本 / 跨 AZ）。

**非目标**：日志与 trace 存储；任意 SQL；毫秒级实时流处理。

## 3. 估算（脚本）

假设（要和面试官确认）：**10 万租户**，总计 **2,000 万点/秒**，**5 亿活跃序列**（活跃 = 近期有写入）。

| 量 | 计算 | 结果 |
|---|---|---|
| 写入点速率 | 假设 | **2,000 万点/s** |
| 副本写入 | RF=3 | **6,000 万点写/s** 的内部流量 |
| ingester 数 | 每台处理 20 万点/s（假设）| ≈ **100 台**（实际要 ×2 做利用率余量）|
| 未压缩原始量 | 2×10^7 × 16 B × 86,400 | **27.6 TB/天** |
| Gorilla 压缩后 | 1.37 B/点（论文：平均每点 1.37 字节，12 倍）| **2.4 TB/天** |
| 活跃序列的内存（head）| 5×10^8 × 1.5–3 KB/序列（`推断`：Prometheus 类 TSDB 经验值）| **750–1,500 GB** → 必须分片，且**序列数（基数）是第一约束** |
| 分层后每序列点数 | 1 分钟×15 天 + 5 分钟×63 天 + 1 小时×455 天 = 21,600 + 18,144 + 10,920 | **50,664 点**，而全程 1 分钟保留 455 天需要 655,200 点 → **12.9 倍**节省 |
| PutMetricData 限制 | 单请求 ≤1 MB（可 gzip）、≤1000 个不同指标、`Values/Counts` 每指标 ≤150 个值 | 客户端必须批量 |

**这些数字改变的设计**：(1) 压缩让存储不是瓶颈，**内存里的活跃序列数才是**（基数治理 = 成本治理）；(2) 分层降采样省 ~13 倍，且降采样后"点数"不再随时间线性增长；
(3) 写路径 6,000 万点/s 的内部放大要求**批量化、顺序写**。

## 4. 标准答案

### 4.1 总体架构

```
 写路径                                                                   读路径
客户 ─▶ 前端(鉴权/配额/校验/限流) ─▶ 分发器 ──(按 序列ID 一致性哈希 + 租户 shuffle shard)──▶ ingester×N   ◀── 查询前端(拆分/缓存)
                                                         │ 每序列: 内存 head 块 + WAL(顺序追加)            │
                                                         │ 每 2 小时: head → 不可变 *块* (列式+Gorilla 压缩)  ▼
                                                         ▼                                      查询器: 近期数据问 ingester;
                                                  对象存储 (S3 类): 块 + 块级索引                  历史数据读块(带本地缓存)
                                                         │
                                       后台 compactor: 合并块 → 生成降采样块(1m→5m→1h) → 按保留期删除
```
这与 Cortex/Mimir/Thanos 的结构同类（`推断` 说明：这些开源系统公开了类似架构；本次没有抓取其文档，仅作为结构参照）。

### 4.2 写路径

1. **前端**：认证租户、校验时间戳（拒绝太旧或太远的未来；CloudWatch 文档提示时间戳偏离当前 UTC 会导致告警 Insufficient Data）、**限流**（每租户每秒点数、每秒新序列数）。
2. **序列标识**：`series_id = hash(tenant, namespace, metric_name, sorted(dimensions))`。维度是**身份的一部分**——CloudWatch 文档："Because dimensions are part of the unique identifier for a metric"，一个指标最多 **30 个维度**。
   → 任何一个新的维度取值组合都会创建**新序列**，这就是基数爆炸的来源。
3. **分发**：按 `series_id` 一致性哈希到 ingester；**租户 shuffle sharding**：每个租户只用 ingester 集合中的 k 台，坏租户（基数暴增）只影响与它共享全部 k 台的极少数租户（[aws-shuffle-sharding](../../../../../domains/system-design/readings/aws-shuffle-sharding.md)）。
4. **复制**：RF=3 写 3 台，W=2 确认即成功（跨 AZ）；这是**写可用性**优先的无主设计（卡 [distributed-quorum-math](../../../../../domains/system-design/cards/distributed/distributed-quorum-math.md)），副本间由查询时合并去重。
5. **ingester 内**：内存 `head`（按序列 append）+ **WAL 顺序追加**（崩溃恢复）；Gorilla 式压缩（时间戳 delta-of-delta、浮点 XOR）。
6. **乱序/迟到**：接受窗口（如 1 小时内的迟到点写入 head 的乱序缓冲）；更晚的丢弃并计数 `rejected_too_old`。
7. **批量/幂等**：PutMetricData 重试同一点 → 序列内 `(timestamp)` 作为天然幂等键，重复写覆盖同值（不同值如何处理见 Q3）。

### 4.3 存储布局与块

- **块（block）** = 一个时间窗（如 2 小时）内的所有序列：`[索引][每序列的压缩 chunk][元数据]`。不可变 → 可缓存、可并行读、容易做校验。
- **倒排索引**：`(tenant, label_name, label_value) → [series_id…]`（postings list）。过滤 `dimension=value` 即取 postings 求交集。**索引大小随基数线性增长**，是成本重点。
- **时间分区**：块按时间窗切分，保留期删除 = 删文件，O(1)，不需要逐点删除（对比 LSM 的墓碑代价，[storage-tombstone-deletes](../../../../../domains/system-design/cards/storage/storage-tombstone-deletes.md)）。
- **热点**：同一个租户的某个超大维度被一条序列占满不是问题；问题是同一**租户**的写入集中到少数 ingester → 用 shuffle shard 的 k 控制。

### 4.4 降采样（本题第一个深挖）

**目标**：旧数据降低分辨率以节省存储和查询成本，同时**让统计量仍然正确**。

**为什么只存平均不行**（对应卡 [problems-metrics-monitoring-downsampling-keep-min-max](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-downsampling-keep-min-max.md)）：`avg(avg(x))` 在各窗口样本数不同时是错的；`max` 被平均抹平 → 峰值事故看不见。
**每个降采样窗口至少存 `count, sum, min, max`**（CloudWatch 的 statistic set 就是 Min、Max、Sum、SampleCount，文档逐字）。由它们能无损推出平均 = sum/count，并可继续向上一层聚合：
```
rollup(窗口集合 W) = { count: Σcount, sum: Σsum, min: min(min), max: max(max) }       ← 满足结合律,可分层/可并行/可重算
```
**百分位怎么降采样？** 百分位**不能**由 avg/min/max 推出，也**不能**把各窗口的 p99 再平均（卡 [reliability-percentile-aggregation](../../../../../domains/system-design/cards/reliability/reliability-percentile-aggregation.md)）。三条路：
1. **保存值分布的草图（sketch）**：每窗口存 t-digest / DDSketch / 直方图桶；草图**可合并**，合并后查询百分位，误差有界（DDSketch 的相对误差保证是它的卖点，`推断`，面试前核对）。
2. **原始 `Values/Counts` 压缩**：CloudWatch 允许上报"值 + 出现次数"数组（每指标最多 150 个值）并支持从中取百分位——相当于客户端预聚合的直方图。
3. **只在高分辨率层保留百分位**：长期层只提供 count/sum/min/max；这是 CloudWatch 类产品常见的限制（产品取舍，需要明确告诉客户）。

**降采样流水线**（后台 compactor，**常量工作**风格）：
```
原始 1s/10s 块 ──(3 小时)──▶ 1 分钟块 ──(15 天)──▶ 5 分钟块 ──(63 天)──▶ 1 小时块 ──(455 天)──▶ 删除
每一层: 读上一层块 → 按窗口对齐聚合 → 写新块(确定性命名,幂等) → 校验计数 → 原子替换元数据 → 删旧块
```
- **幂等重跑**：输出块名由 `(tenant, 层级, 起止时间)` 确定；compactor 崩溃后重做得到同名同内容的块，覆盖无副作用（[analytics-idempotent-reruns](../../../../../domains/system-design/cards/analytics/analytics-idempotent-reruns.md)）。
- **对齐**：窗口按 UTC 对齐，保证不同序列、不同 compactor 实例得到相同的窗口边界。
- **迟到数据**：窗口已降采样后到达的点 → 要么丢弃并计数，要么触发**重写该窗口**（昂贵）。产品选择：设定"最大迟到时间 = 本层级窗口长度"，之后拒绝。
- **查询选择分辨率**：`GetMetricData(period=P)` → 选择能覆盖请求范围的、最粗但 ≤P 的层；请求的 period 小于该时间点可用的最细分辨率时，返回该层分辨率（文档语义：只能取回聚合后的分辨率）。

### 4.5 读路径

- **查询前端**：把长时间范围**按时间拆成多段**并行查，每段结果可缓存（不可变块 → 缓存命中率高，仅"最近一段"不可缓存或短 TTL）。
- **最近数据**：扇出到持有该租户序列的 ingester（只有 k 台，不是全体 → 扇出受 shuffle shard 约束）；对 RF=3 的副本结果**合并去重**。
- **历史数据**：读块的索引（先读块级布隆/索引头），再读命中序列的 chunk；本地 SSD 缓存热块。
- **查询保护**：每租户并发查询数、最大返回点数（CloudWatch 类服务限制单次返回点数，需翻页）、最大扫描序列数；超限快速失败（load shedding，不排队，[traffic-rate-limiting-vs-load-shedding](../../../../../domains/system-design/cards/traffic/traffic-rate-limiting-vs-load-shedding.md)）。
- **公平**：昂贵查询走独立队列+公平调度，避免一个大查询堵住所有小查询。

### 4.6 基数治理（成本与稳定性的第一杠杆）

- 每租户**活跃序列数上限**（软限制告警、硬限制拒绝**新**序列但继续接受**已有**序列的点）。关键：拒绝新序列而不是拒绝所有写，否则基数爆炸会"误伤"正常指标。
- 检测：前端维护每租户的新序列速率（滑动窗口）；对超速租户返回明确错误码并给出 top 维度（哪个标签在爆炸）。
- **告警评估/查询不得因基数爆炸而变慢**：给每租户单独的预算。
- 对应卡：[problems-metrics-monitoring-cardinality-admission-quota](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-cardinality-admission-quota.md)。

### 4.7 多租户隔离

| 层 | 机制 |
|---|---|
| 写入 | 前端每租户令牌桶（点/s、新序列/s）；ingester shuffle shard；超限 429 + `Retry-After` |
| 存储 | 块按租户前缀；每租户序列数/保留期配额 |
| 读取 | 每租户并发与扫描预算；公平队列 |
| 发布 | 按 cell 灰度（账号→cell）+ one-box + 自动回滚（`../00_how_to_run_the_round.md` §7）|

### 4.8 告警评估：独立于查询路径

告警的可靠性要求**高于**仪表盘查询：事故时大家狂刷仪表盘（查询量暴增），告警不能因此变慢（卡 [problems-metrics-monitoring-alert-eval-independent-region](../../../../../domains/system-design/cards/problems/problems-metrics-monitoring-alert-eval-independent-region.md)）。
- 告警评估器是**独立的服务**：按固定节奏（每 10/30/60 秒）对每条告警读取最近窗口的数据——**常量工作**：无论发生什么事故，工作量不变。
- 评估器**直接读 ingester 的最近数据**（短路径）而不经查询前端。
- 缺失数据的语义要显式：`INSUFFICIENT_DATA` / treat-as-breaching / ignore，由客户选择。
- 评估器多副本、每条告警只由一个"主评估器"负责（租约+fencing），主挂了换人；状态转换去抖（连续 N 个窗口才变态）。
- 告警通知走 outbox + 至少一次投递，重复通知靠告警状态机幂等。

### 4.9 故障分析

| 故障 | 影响 | 处理 |
|---|---|---|
| 1 台 ingester 挂 | 其序列的 1/3 副本丢失 | RF=3，W=2；WAL 重放；新节点从对等节点拉取最近数据 |
| 1 个 AZ 挂 | 每序列失 1 副本 | 仍能 W=2 写入；**静态稳定**：事先留足容量，而不是事后扩容 |
| 对象存储抖动 | 历史查询慢、flush 延迟 | ingester 本地磁盘缓冲更久；查询降级为"只返回近期并标注不完整" |
| compactor 落后 | 存储成本上升、查询变慢 | 告警；compactor 优先级低于 ingestion，但有最低保障预算 |
| 基数爆炸 | 内存撑爆 | §4.6 |
| 坏发布 | 数据点被错误解析 | one-box + 回放对比（新旧版本并行解析同一流，对比结果）|

## 5. 追问与答案

**Q1. 为什么降采样要存 count/sum/min/max，而不是只存平均？百分位怎么办？**
A：见 §4.4。平均不可再聚合（加权）、会抹平峰值；百分位无法由其它统计量推导，也不能平均百分位——必须存**可合并的分布草图**或直方图，或在长期层明确不提供百分位。

**Q2. 如何让降采样"可重算"（比如修了 bug 要重做）？**
A：降采样是**原始（或上一层）数据的纯函数**，输出块名确定。只要保留上一层数据到下一层成功校验，就能重跑。代价：原始数据要比"理论最短保留"多留一段（回滚窗口）。

**Q3. 客户重复发送同一时间戳、不同值的点怎么办？**
A：定义语义：同一 `(series, timestamp)` 后写覆盖（last-write-wins，按服务端接收序），或拒绝并计数。对统计型数据（statistic set）可以改为"合并"。我倾向"同值幂等，异值取最后写入，并记录冲突计数"。注意 LWW 在多副本下需要版本（服务端时间戳或序号）才可确定（[distributed-lww-danger](../../../../../domains/system-design/cards/distributed/distributed-lww-danger.md)）。

**Q4. 一个租户 5 分钟内创建了 1 亿个新序列（比如把请求 ID 当维度）。**
A：前端新序列速率限制先触发 → 拒绝**新序列**（已有序列照常），返回明确错误并指出爆炸的维度名；ingester 的内存按租户核算，超限时驱逐"最久未写入"的序列；该租户 shuffle shard 外的租户不受影响。事后给租户一个"基数报告"。

**Q5. 查询过去 1 年、5 分钟粒度，数据在 1 小时层怎么办？**
A：该范围的老部分只有 1 小时分辨率，API 返回 1 小时粒度并**在响应中标注实际分辨率**；永远不"凭空插值"。如果客户需要更细，只能提前配置更长的高分辨率保留（成本更高）。

**Q6. 如何做到写入的 p99 延迟低、又不丢？**
A：写路径只做**内存 append + WAL 顺序追加**，到 2/3 副本确认即返回；压缩和落盘异步；批量化 flush。WAL 用组提交（group commit）摊薄 fsync。尾延迟靠对冲（hedged request）和快速剔除慢副本（W=2 不等第三个）。

**Q7. 为什么不把所有数据点直接放进 DynamoDB/通用 KV？**
A：每点一条记录的写放大和索引成本太高（5 亿序列 × 持续写入）；时序数据的访问模式是"按序列按时间范围"，适合**按块批量写、批量压缩**；通用 KV 无法提供 12 倍的压缩；删除过期数据要逐条墓碑。结论：热数据用专用 TSDB 块格式，冷数据用对象存储。

**Q8. 多区域怎么做？**
A：指标默认**区域内闭环**（写入、存储、查询、告警都在本区域），这样区域间故障隔离；跨区域查询通过聚合层调用多个区域的 API（故障时返回部分结果并标注）。跨区域复制只给关键指标，作为 DR。

**Q9. 怎么证明降采样是对的？**
A：持续校验：抽样租户，对同一窗口比较"原始层即时聚合"与"降采样层"的 count/sum/min/max；差异入告警。类似 DynamoDB 的 scrub（由归档日志离线重建并与线上副本比对，[DDB22] §5.3）。

## 6. 评分表

| 维度 | Strong | OK | Weak |
|---|---|---|---|
| 需求/估算 | 点出"基数是第一约束"，给出内存估算；用保留分层计算节省倍数 | 估了 QPS 和存储 | 只估存储字节 |
| 降采样 | count/sum/min/max；百分位用草图/直方图，说明不可平均；幂等重跑；迟到策略 | 说"保留最大最小" | 只存平均 |
| 存储 | 块 + 倒排索引 + 压缩（delta-of-delta + XOR）；删除=删块 | 提到 TSDB | 用通用 KV/SQL 存点 |
| 写路径 | 前端配额 + shuffle shard + WAL + RF/W；乱序窗口 | 有队列和存储 | 单点写入 |
| 读路径 | 拆分+缓存不可变块；扇出受限；查询保护；返回实际分辨率 | 有缓存 | 全量扫描 |
| 多租户 | 拒新序列不拒老序列；公平队列；告警路径独立 | 配额 | 无隔离 |
| 运维 | 校验降采样、cell 灰度、one-box、告警评估常量工作 | 监控 | 无 |

**Senior 常见失分点**：忘了维度即身份；用平均值降采样；告警与仪表盘共用查询路径；基数超限时拒绝所有写入。

## 7. 与题库的关系
- 先做 [design-metrics-monitoring](../../../../../domains/system-design/drills/problems/design-metrics-monitoring.md)，再做本题；[design-top-k](../../../../../domains/system-design/drills/problems/design-top-k.md)（近似与草图）、[design-ad-click-aggregation](../../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)（窗口与迟到数据）。
- 阅读：[google-sre-monitoring](../../../../../domains/system-design/readings/google-sre-monitoring.md)、[google-sre-slo](../../../../../domains/system-design/readings/google-sre-slo.md)。
