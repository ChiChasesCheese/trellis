# 系统设计练习路线（先做题库里的 8 道，再做 5 道 AWS 新题）

> 规则：题库里的题**不复制**，只在这里给"顺序 + Amazon 口味的追加练习点"。每道题的标准流程：
> ① 看题面（`drills/problems/design-*.md`）→ ② 自己限时 40–50 分钟口述/白板 → ③ 对照题解（`readings/problems/solution-*.md`）→ ④ 做"Amazon 追加练习"（本表最后一栏）→ ⑤ 在题库的 Attempt log 里记自评。
> 方法论与运维口径：`00_how_to_run_the_round.md`；概念速成：`00_ddia_refresh.md`。bar：senior。
> 路径前缀 `domains/system-design/` 省略为 `SD/`。

## 1. 顺序与理由

排序原则：**(a) 越贴近 AWS Data Services 的真实产品越靠前；(b) 前一道的机制是后一道的前置；(c) 从"单机心智"逐步到"控制面/多租户"。**

| 序 | 题（题库）| 对应 AWS 产品 | 为什么在这个位置 | Amazon 口味的追加练习（做完题解后再做）|
|---|---|---|---|---|
| 1 | [design-key-value-store](../../../../domains/system-design/drills/problems/design-key-value-store.md) · 题解 [solution-key-value-store](../../../../domains/system-design/readings/problems/solution-key-value-store.md) | **Dynamo (2007) / DynamoDB (2022)** | 复制、分区、quorum、热点全部在这里；后面每题都复用 | ① 能一口气讲清 **Dynamo（无主、sloppy quorum、vector clock）与 DynamoDB（每分区一个 Multi-Paxos leader、2/3 AZ 写 quorum、log replica）的差别**（[DDB22] §2–3、§6.1）。② 讲"热分区/吞吐稀释 → burst → adaptive capacity → GAC → 按消耗分裂"这条演进（[DDB22] §4）。③ 画出一次 `PutItem` 的旅程（`00_ddia_refresh.md` §9）。 |
| 2 | [design-object-storage](../../../../domains/system-design/drills/problems/design-object-storage.md) · 题解 [solution-object-storage](../../../../domains/system-design/readings/problems/solution-object-storage.md) | **S3** | 数据服务的底座；持久性、前缀分区、元数据 | ① **11 个 9 的耐久度怎么算**：纠删码 + 校验和 + 持续巡检（scrub）；② S3 前缀速率（3,500 写 / 5,500 读每秒/前缀）与 503 Slow Down 的含义（[S3PERF]）；③ ShardStore：LSM 索引 + 只追加 extent + 回收（[S3-21] §2）；④ 条件写做 CAS（卡 [storage-s3-conditional-writes](../../../../domains/system-design/cards/storage/storage-s3-conditional-writes.md)）。 |
| 3 | [design-message-queue](../../../../domains/system-design/drills/problems/design-message-queue.md) · 题解 [solution-message-queue](../../../../domains/system-design/readings/problems/solution-message-queue.md) | **SQS / Kinesis / MSK** | 日志与队列抽象；CDC、流摄取、指标写入都依赖 | ① Kinesis 数字：每 shard 写 1 MB/s 或 1,000 条/s、读 2 MB/s（[KDS]）→ 用它做分区数估算；② 阅读 Builders' Library《Avoiding insurmountable queue backlogs》（[aws-queue-backlogs](../../../../domains/system-design/readings/aws-queue-backlogs.md)）：积压、spillover 队列、延迟队列、DLQ；③ 公平：每客户分队列 / shuffle-sharding 到少数队列（Lambda 的做法）。 |
| 4 | [design-job-scheduler](../../../../domains/system-design/drills/problems/design-job-scheduler.md) · 题解 [solution-job-scheduler](../../../../domains/system-design/readings/problems/solution-job-scheduler.md) | **EventBridge Scheduler / Step Functions / 工作流引擎** | 控制面的核心（题 5 的前置）：租约、fencing、至少一次 | ① 把"每个调度任务只被一个 worker 执行"讲成**租约 + fencing token**（卡 [problems-job-scheduler-fencing-token-lease](../../../../domains/system-design/cards/problems/problems-job-scheduler-fencing-token-lease.md)）；② 多租户公平调度（[problems-job-scheduler-multi-tenant-weighted-fairness](../../../../domains/system-design/cards/problems/problems-job-scheduler-multi-tenant-weighted-fairness.md)）；③ **常量工作**：用固定节奏扫描而不是随负载变化的触发（[aws-constant-work](../../../../domains/system-design/readings/aws-constant-work.md)）；④ 毒丸任务 → 隔离到 shuffle shard。 |
| 5 | [design-metrics-monitoring](../../../../domains/system-design/drills/problems/design-metrics-monitoring.md) · 题解 [solution-metrics-monitoring](../../../../domains/system-design/readings/problems/solution-metrics-monitoring.md) | **CloudWatch** | 是新题 3 的前置 | ① 保留分层与降采样（CloudWatch：<60 s 保留 3 小时，1 分钟 15 天，5 分钟 63 天，1 小时 455 天）；② 基数治理；③ **告警评估路径与查询路径分离**（[problems-metrics-monitoring-alert-eval-independent-region](../../../../domains/system-design/cards/problems/problems-metrics-monitoring-alert-eval-independent-region.md)）；④ 接着做 `problems/metrics_timeseries_store.md`。 |
| 6 | [design-ad-click-aggregation](../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md) · 题解 [solution-ad-click-aggregation](../../../../domains/system-design/readings/problems/solution-ad-click-aggregation.md) | **Kinesis + Lambda/Flink + DynamoDB/S3** | 流处理正确性（窗口、水位线、迟到、对账）| ① exactly-once 的**边界**（卡 [async-eos-boundary-choice](../../../../domains/system-design/cards/async/async-eos-boundary-choice.md)）；② 用 DynamoDB **条件写**做去重键（`attribute_not_exists`），而不是"相信队列"；③ Kinesis 热分区（热门 ad_id）→ 加盐（[problems-ad-click-aggregation-hot-ad-id-salting](../../../../domains/system-design/cards/problems/problems-ad-click-aggregation-hot-ad-id-salting.md)）；④ 批流对账（Lambda 架构）。 |
| 7 | [design-distributed-cache](../../../../domains/system-design/drills/problems/design-distributed-cache.md) · 题解 [solution-distributed-cache](../../../../domains/system-design/readings/problems/solution-distributed-cache.md) | **ElastiCache / DAX / DynamoDB 内部 MemDS** | 缓存的"双峰行为"是 Amazon 爱问的深挖 | ① 讲 DynamoDB 元数据缓存故事：命中率 ~99.75%，但路由器冷启动时元数据服务流量飙升 75% → 改造成 MemDS（[DDB22] §6.6）；② Builders' Library《Caching challenges and strategies》（[aws-caching-challenges](../../../../domains/system-design/readings/aws-caching-challenges.md)）；③ **别让缓存隐藏本该承担的工作量**（[DDB22] §1 第四条教训）；④ 冷启动预热（[problems-distributed-cache-cold-start-peer-warm](../../../../domains/system-design/cards/problems/problems-distributed-cache-cold-start-peer-warm.md)）。 |
| 8 | [design-top-k](../../../../domains/system-design/drills/problems/design-top-k.md) · 题解 [solution-top-k](../../../../domains/system-design/readings/problems/solution-top-k.md) | **Kinesis Analytics / Redis / 近似算法** | 小而精，当"热身题"；也用于指标/日志分析 | ① Count-Min Sketch、Space-Saving 的误差界；② 分片局部 top-k 再合并（可合并性）；③ 与题 3 的"可合并的分位数草图"同一个思想。 |
| 9 | `problems/managed_db_control_plane.md` | **RDS / Aurora 控制面** | 综合：控制面/数据面、租约、fencing、备份、多租户 | 全部在文件里 |
| 10 | `problems/cdc_replication_pipeline.md` | **DMS** | 日志/CDC/幂等的综合 | 同上 |
| 11 | `problems/metrics_timeseries_store.md` | **CloudWatch 指标 / Timestream** | 降采样、基数、百分位 | 同上 |
| 12 | `problems/data_lake_ingestion_catalog.md` | **Glue / Lake Formation / S3** | 摄取幂等、表格式、目录、治理 | 同上 |
| 13 | `problems/serverless_query_over_s3.md` | **Athena** | 分区裁剪、列存、S3 吞吐、无服务器多租户 | 同上 |

**如果只剩一天**：做 1（KV 存储）+ 9（控制面），因为 Dynamo/DynamoDB 与"控制面/故障切换/多租户"是 AWS Data Services 的 DNA。

## 2. 五天排期（今天 2026-10-15 → onsite 约 10-20/21）

| 日 | 内容（每块 = 题 + 追加练习，约 90 分钟）| 备注 |
|---|---|---|
| 10-15（晚）| 读 `00_how_to_run_the_round.md`（60 分钟）+ `00_ddia_refresh.md` §1–§5（90 分钟）| 先把词汇表补上；做 §10 自测前 8 题 |
| 10-16 | 题 1 KV 存储 + 题 2 对象存储 | 做完口述一遍"PutItem 旅程" |
| 10-17 | 题 3 消息队列 + 题 4 作业调度 + 新题 5（控制面）的 §4.1–4.3 | 重点练**租约/fencing**这段话 |
| 10-18 | 题 5 指标 + 新题 3 + 题 6 广告点击 | 练"降采样 + 百分位不能平均" |
| 10-19（去西雅图）| 新题 1 CDC / 新题 2 数据湖 / 新题 4 Athena 各读一遍 §4 + 追问；题 7、8 用 20 分钟各过一遍卡片 | 路上只读，不再新做 |
| 10-20/21 | 早上 30 分钟：`00_how_to_run_the_round.md` §9 开场脚本 + §7 运维五件套 | 保持睡眠 |

> 若 `catalog/raw/forums.md` 显示设计轮对 SDE I 实际是 LLD 为主，则把 10-17 之后的 1/3 时间挪给 `../lld/route.md`（见该文件）。

## 3. 每次练习的"自评表"（复制到题库的 Attempt log）

- [ ] 前 5 分钟写下了非目标和数字化 SLO
- [ ] 估算后说出了设计结论（不是算完就扔）
- [ ] API 有幂等令牌；分页；错误可重试性
- [ ] 图里有控制面/数据面
- [ ] 深挖讲到了"为什么 + 替代 + 代价 + 数字"
- [ ] 故障：说了 AZ 故障时容量够不够（静态稳定）
- [ ] 运维：one-box / 波次 / bake / 自动回滚 / cell / shuffle sharding 至少讲了两个
- [ ] 点名了自己设计里最弱的一环

## 4. 题库之外也值得过一遍的（各 15 分钟，仅看题解的"追问"）
- [design-lock-service](../../../../domains/system-design/drills/problems/design-lock-service.md)（leader election / fencing；Amazon 的《Leader election in distributed systems》）
- [design-unique-id-generator](../../../../domains/system-design/drills/problems/design-unique-id-generator.md)（ID 生成与时钟）
- [design-notification-system](../../../../domains/system-design/drills/problems/design-notification-system.md)（SNS/SQS 扇出、去重、供应商故障切换）
- [design-file-sync](../../../../domains/system-design/drills/problems/design-file-sync.md)（内容寻址分块、元数据 vs 数据分离，对应 S3 + DynamoDB 的常见组合）

## 5. 论坛真实报告的 HLD 题 → 本 kit 的覆盖对照

来源：`../catalog/raw/forums.md` §4.4（SDE II+ 栏的 HLD 行，#refs 为独立报告数）与 §3.3（AWS 数据/存储方向原文）。**SDE I 栏的 HLD 全是 0**；以下是 senior 档要会的。

| 报告里的题（#refs，II+）| 覆盖在哪里 |
|---|---|
| News feed（7）/ Twitter | 题库 [design-news-feed](../../../../domains/system-design/drills/problems/design-news-feed.md)、[design-social-graph-search](../../../../domains/system-design/drills/problems/design-social-graph-search.md)；LC6841317 的 Twitter 追问点名了 "LSM vs B-tree、consistent hashing、read-after-write、sharding vs replication、celebrity 倾斜"——全在 `00_ddia_refresh.md` §1–§3 |
| Hotel / ticket booking（5）| 题库 [design-hotel-reservation](../../../../domains/system-design/drills/problems/design-hotel-reservation.md)、[design-ticket-booking](../../../../domains/system-design/drills/problems/design-ticket-booking.md) |
| Uber / 打车匹配（5）| 题库 [design-ride-hailing](../../../../domains/system-design/drills/problems/design-ride-hailing.md)、[design-proximity](../../../../domains/system-design/drills/problems/design-proximity.md) |
| Inventory management（4，"最后一件库存两个人同时下单"）| 题库 [design-e-commerce](../../../../domains/system-design/drills/problems/design-e-commerce.md)、[design-flash-sale](../../../../domains/system-design/drills/problems/design-flash-sale.md)（条件写 / 锁 / 事务；DynamoDB 条件表达式）|
| Netflix / video catalogue（4）、Spotify（2）| 题库 [design-video-streaming](../../../../domains/system-design/drills/problems/design-video-streaming.md)；LC8315111 追问 "OpenSearch + CDC" → 新题 `problems/cdc_replication_pipeline.md` |
| WhatsApp / chat（4）| 题库 [design-chat-messaging](../../../../domains/system-design/drills/problems/design-chat-messaging.md) |
| File storage / Drive / Dropbox（3）、S3-like（1）| 题库 [design-file-sync](../../../../domains/system-design/drills/problems/design-file-sync.md)、[design-object-storage](../../../../domains/system-design/drills/problems/design-object-storage.md) |
| Device management / config sync / backup（3）| `hld_sketches.md` S5 |
| Artifact repository（2）| `hld_sketches.md` S1 |
| Kindle / e-reader sync（2，一次是 Bar Raiser）| `hld_sketches.md` S2 |
| Dashboarding / metrics monitoring / telemetry min-max / alerting on metric streams（共 5）| 题库 [design-metrics-monitoring](../../../../domains/system-design/drills/problems/design-metrics-monitoring.md) + 新题 `problems/metrics_timeseries_store.md` |
| Log storage / logging + monitoring（2）| `hld_sketches.md` S3 |
| Employee directory（DynamoDB 分区键，1）| `hld_sketches.md` S4 |
| Reviews & ratings（2）| `hld_sketches.md` S6 |
| Notification service / router（2）| 题库 [design-notification-system](../../../../domains/system-design/drills/problems/design-notification-system.md) |
| URL shortener（2）| 题库 [design-url-shortener](../../../../domains/system-design/drills/problems/design-url-shortener.md) |
| Primary DB + read-replica failover（1，DB group）| 新题 `problems/managed_db_control_plane.md` §4.6 |
| S3 上的分析查询 API（<2 秒，1，AWS L5 Bar Raiser）| 新题 `problems/serverless_query_over_s3.md` + `problems/metrics_timeseries_store.md`（"streams → 时序库；聚合移出查询路径"）|
| AWS Lambda 式代码执行（1）| 题库 [design-online-judge](../../../../domains/system-design/drills/problems/design-online-judge.md)（沙箱、冷启动）+ 卡 [architecture-cold-starts](../../../../domains/system-design/cards/architecture/architecture-cold-starts.md) |
| 分布式限流器，central leasing service（1，SDE3）| 卡 [traffic-distributed-rate-limiting](../../../../domains/system-design/cards/traffic/traffic-distributed-rate-limiting.md)；`../lld/route.md` 第 4 项 |
| Google Docs / OT vs CRDT（1）| 题库 [design-google-docs](../../../../domains/system-design/drills/problems/design-google-docs.md) |

**读法**：senior 档设计轮（HM 或 Bar Raiser）最常见的 5 个主题是 news feed、订房/订票、打车、库存、流媒体——都在题库里；AWS 数据团队的特色题（监控、日志、S3 查询、DB 故障切换、CDC）由 `problems/` 的 5 道新题和 `hld_sketches.md` 覆盖。
