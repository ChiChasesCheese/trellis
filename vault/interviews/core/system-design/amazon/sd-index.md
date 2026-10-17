# 系统设计题单（System Design Questions）

这里每一篇都是一道完整的系统设计题：先用大白话讲清这个系统是什么、难在哪里，再按面试的顺序走一遍——澄清问题、
需求、容量估算、核心实体与 API、架构图、三到四个深挖、staff 层面的权衡与故障、面试官会追问什么、60 分钟怎么分配、
自测。标准按 senior / staff 写：每个选择都说清楚「是什么逼出了它」和「它换来了什么、代价是什么」。

和具体题目无关的通用知识（复制、分区、缓存、一致性……）在 [[System Design MOC|系统设计域]]。方法与词汇先读
[[00_how_to_run_the_round]] 和 [[00_ddia_refresh]]。

## 题单（按学习顺序）

先做前两道：一道考「读多写少的全局服务」，一道考「库存预留与状态流转」，覆盖了后面几道的大部分基本功。

| # | 题 | 考什么 | 题解 | 先读的通用题解 |
|---|---|---|---|---|
| SD01 | 短链接服务（URL Shortener） | 编号怎么生成才永不碰撞；怎样把 99% 的读挡在数据库之外；单个爆款链接的热点 | [[sd01-url-shortener]] | [[solution-url-shortener]] |
| SD02 | Amazon Lockers 投递系统 | 结账时预留柜格而不超卖；柜机断网时怎么取件；投递与退货的状态流转 | [[sd02-amazon-lockers]] | [[solution-amazon-locker]] |
| SD03 | 配送中心库存状态服务 | 海量库存事件的幂等摄入；账本与当前状态分开存；最后一件库存的争抢 | [[sd03-dc-stock-state]] | [[solution-e-commerce]]、[[solution-flash-sale]] |
| SD04 | 文件系统跨区域复制 | 只传变化的部分；文件内容与元数据的先后顺序；对端宕机后怎么追平 | [[sd04-fs-replication]] | [[solution-file-sync]]、[[solution-object-storage]] |
| SD05 | 疫苗资格与预约 | 资格规则可配置且可追溯；时段与剂量两种库存同时约束；开放日的瞬时洪峰 | [[sd05-vaccine-booking]] | [[solution-ticket-booking]]、[[solution-hotel-reservation]] |
| SD06 | AI Agent 安全事件平台（1 TB/天） | 每天 1 TB 事件的流式摄入；实时规则与离线检测两条路；多租户隔离与敏感数据脱敏 | [[sd06-agent-security]] | [[solution-ad-click-aggregation]]、[[solution-metrics-monitoring]] |
| SD07 | 大文件外部排序（200 GB 数据 / 8 GB 内存） | 内存放不下时怎么排序：分段排序再多路归并；多台机器怎么分工 | [[sd07-external-sort]] | — |

### AWS 数据服务题（在 `problems/` 里）

| 题 | 考什么 | 题解 | 先读的通用题解 |
|---|---|---|---|
| 托管数据库控制面 | 控制面与数据面分离；租约与 fencing；主从切换、备份与时间点恢复；多租户 | [[sd10-managed-db-control-plane]] | [[solution-job-scheduler]]、[[solution-key-value-store]] |
| 变更数据捕获复制管道 | 日志式捕获；至少一次加幂等；初始全量与增量衔接；顺序与重放 | [[sd08-cdc-replication-pipeline]] | [[solution-message-queue]] |
| 指标时序存储 | 降采样与保留分层；基数治理；百分位不能平均；告警路径与查询路径分离 | [[sd11-metrics-timeseries-store]] | [[solution-metrics-monitoring]] |
| 数据湖摄取与目录 | 摄取幂等；表格式；目录与治理 | [[sd09-data-lake-ingestion-catalog]] | [[solution-object-storage]]、[[solution-ad-click-aggregation]] |
| S3 上的无服务器查询 | 分区裁剪；列存；S3 吞吐；无服务器多租户 | [[sd12-serverless-query-over-s3]] | [[solution-object-storage]] |

## 通用题解的练习顺序与追加练习点

越贴近 AWS 数据服务的越靠前，前一道的机制是后一道的前置。读完通用题解后，做表里的追加练习，再进 `problems/`。

| 序 | 通用题解 | 对应的服务 | 追加练习 |
|---|---|---|---|
| 1 | [[solution-key-value-store]] | Dynamo / DynamoDB | 讲清无主复制（sloppy quorum、向量时钟）与「每分区一个 leader、跨 AZ 写 quorum」的差别；讲热分区的演进（突发容量、自适应容量、按消耗分裂）；画出一次 `PutItem` 的完整旅程 |
| 2 | [[solution-object-storage]] | S3 | 11 个 9 的耐久度怎么来：纠删码、校验和、持续巡检；前缀速率上限与 503 Slow Down 的含义；条件写做 CAS |
| 3 | [[solution-message-queue]] | SQS / Kinesis | 用每分片的写入上限估算分区数；积压、溢出队列、延迟队列、死信队列；公平：每客户分队列或 shuffle sharding |
| 4 | [[solution-job-scheduler]] | EventBridge Scheduler / Step Functions | 「每个任务只被一个 worker 执行」讲成租约加 fencing token；多租户公平调度；固定节奏扫描（常量工作）；毒丸任务隔离到 shuffle shard |
| 5 | [[solution-metrics-monitoring]] | CloudWatch | 保留分层与降采样；基数治理；告警评估路径与查询路径分离；接着做 [[sd11-metrics-timeseries-store]] |
| 6 | [[solution-ad-click-aggregation]] | Kinesis + Flink + DynamoDB / S3 | 精确一次的边界；用条件写做去重键而不是相信队列；热门 key 加盐；批流对账 |
| 7 | [[solution-distributed-cache]] | ElastiCache / DAX | 缓存的双峰行为：命中率很高，但冷启动时后端流量飙升；别让缓存隐藏本该承担的工作量；冷启动预热 |
| 8 | [[solution-top-k]] | Kinesis Analytics / Redis | Count-Min Sketch 与 Space-Saving 的误差界；分片局部 top-k 再合并；与「可合并的分位数草图」同一个思想 |

只剩一天：做 1（KV 存储）和 [[sd10-managed-db-control-plane]]，因为 Dynamo 式存储与「控制面 / 故障切换 / 多租户」是 AWS 数据服务的基础。

其他值得各过 15 分钟（只看追问）的题解：[[solution-lock-service]]（leader election、fencing）、[[solution-unique-id-generator]]、
[[solution-notification-system]]（扇出、去重、供应商故障切换）、[[solution-file-sync]]（内容寻址分块、元数据与数据分离）。
长期常考但没有写成 Amazon 版的题，直接读通用题解：[[solution-google-docs]]、[[solution-ride-hailing]]、[[solution-notification-system]]、
[[solution-news-feed]]、[[solution-hotel-reservation]]、[[solution-ticket-booking]]、[[solution-e-commerce]]、[[solution-video-streaming]]、
[[solution-chat-messaging]]。

## 题目对应到哪里

| 题 | 读哪里 |
|---|---|
| 制品仓库、Kindle 多设备同步、日志存储、员工目录（DynamoDB 分区键）、设备管理 / 配置同步、评论与评分 | [[hld_sketches]]（六个 25 分钟骨架） |
| 监控 / 指标 / 告警 | [[solution-metrics-monitoring]]、[[sd11-metrics-timeseries-store]] |
| 主库加只读副本的故障切换 | [[sd10-managed-db-control-plane]] |
| S3 上的分析查询 API | [[sd12-serverless-query-over-s3]]、[[sd11-metrics-timeseries-store]] |
| 分布式限流器 | [[solution-rate-limiter]] |
| Lambda 式代码执行 | [[solution-online-judge]]（沙箱、冷启动） |

## 怎么练

- 先读表里「先读的通用题解」，再读这里的题解：这里假设你已经知道通用版本，重点讲每道题自己特有的难点和 senior 深挖。
- 读完一篇，合上它，照着末尾的「60 分钟怎么分配」计时口述一遍，再做「自测」（答案在折叠块里）。
- 每次口述后对照自评：前 5 分钟写下非目标和数字化 SLO；估算后说出设计结论；API 有幂等令牌和分页；图里分控制面与数据面；
  深挖讲到「为什么、替代、代价、数字」；说了 AZ 故障时容量够不够；运维至少讲两个（one-box、波次发布、bake、自动回滚、cell、shuffle sharding）；点名自己设计里最弱的一环。
