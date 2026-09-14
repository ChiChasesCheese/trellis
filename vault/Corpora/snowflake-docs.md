%% trellis:begin %%
# Snowflake Documentation — core mechanisms

Snowflake Inc. · free-online · [[Snowflake 原理 MOC|Snowflake 原理]]
[Home ↗](https://docs.snowflake.com/en/guides)

35 sections · 34 readings · 392 cards · 77/110 leaves reached

## Outline
- **Snowflake key concepts and architecture¶** — [[snowflak-key-concepts-architecture|Snowflake 关键概念与整体架构]] → [[architecture.three-layer-model|三层架构]], [[architecture.storage-compute-separation|存储与计算分离（storage/compute separation）]], [[architecture.multi-cluster-shared-data|多集群共享数据模型]], [[architecture.cloud-services-layer|云服务（Cloud Services，GS）层]], [[architecture.cloud-agnostic-multi-region|跨云与多区域部署]], [[storage.object-storage-backend|对象存储后端]] · 29 cards
- **Micro-partitions & Data Clustering¶** — [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]] → [[storage.micro-partition-format|微分区（micro-partition）格式]], [[storage.micro-partition-metadata|微分区元数据]], [[storage.columnar-compression-encoding|列式压缩与编码]], [[storage.clustering-keys|聚簇键（clustering key）]], [[pruning.min-max-zone-maps|最小/最大值剪枝（zone map）]], [[pruning.partition-elimination|分区消除（partition elimination）]], [[pruning.clustering-depth-metric|聚簇深度（clustering depth）]], [[metadata.optimizer-statistics|优化器统计信息]] · 39 cards
- **Clustering Keys & Clustered Tables¶** — [[snowflak-clustering-keys-strategy|聚簇键的选择与何时需要它]] → [[storage.clustering-keys|聚簇键（clustering key）]], [[storage.natural-vs-explicit-clustering|自然聚簇与显式聚簇]] · 12 cards
- **Automatic Clustering¶** — [[snowflak-automatic-clustering|自动重新聚簇服务(Automatic Clustering)]] → [[storage.automatic-reclustering|自动重新聚簇（automatic reclustering）]] · 6 cards
- **Overview of warehouses¶** — [[snowflak-warehouses-overview|虚拟仓库总览:尺寸、自动挂起与排队]] → [[warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]], [[warehouse.auto-suspend-resume|自动挂起与自动恢复]], [[warehouse.query-queuing|查询排队]], [[cost.warehouse-billing-60s-minimum|仓库最低计费时长]] · 21 cards
- **Multi-cluster warehouses¶** — [[snowflak-multicluster-warehouses|多集群仓库与扩缩容策略]] → [[warehouse.multi-cluster-scaling-policy|多集群伸缩策略]], [[warehouse.query-queuing|查询排队]] · 11 cards
- **Warehouse considerations¶** — [[snowflak-warehouse-best-practices|仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存]] → [[warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]], [[warehouse.auto-suspend-resume|自动挂起与自动恢复]], [[warehouse.scaling-up-vs-out|纵向扩展与横向扩展]], [[cache.warehouse-local-disk-cache|仓库本地 SSD 缓存]] · 21 cards
- **Using Persisted Query Results¶** — [[snowflak-result-cache|结果缓存(Result Cache)命中与失效条件]] → [[cache.result-cache|持久化结果缓存]], [[cache.result-cache-invalidation|结果缓存失效]] · 10 cards
- **Monitor query activity with Query History¶** — [[snowflak-query-profile-history|查询画像(Query Profile)与查询历史的定位方法]] → [[query.reading-query-profile|解读查询画像（query profile）]], [[query.spilling-to-remote-disk|溢出（spilling）到本地与远程磁盘]], [[pruning.partition-elimination|分区消除（partition elimination）]], [[cost.query-history-and-account-usage|QUERY_HISTORY 与 ACCOUNT_USAGE]] · 20 cards
- **Search optimization service¶** — [[snowflak-search-optimization|搜索优化服务(Search Optimization Service)]] → [[pruning.search-optimization-service|搜索优化服务（Search Optimization Service）]] · 5 cards
- **Using the Query Acceleration Service (QAS)¶** — [[snowflak-query-acceleration|查询加速服务(QAS)加速离群查询]] → [[pruning.query-acceleration-service|查询加速服务（Query Acceleration Service）]], [[cost.serverless-feature-billing|无服务器功能计费]] · 11 cards
- **Working with Materialized Views¶** — [[snowflak-materialized-views|物化视图(Materialized View)的预计算与维护成本]] → [[pruning.materialized-views-maintenance|物化视图（materialized view）]] · 5 cards
- **Understanding & using Time Travel¶** — [[snowflak-time-travel|时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP]] → [[continuity.retention-vs-failsafe|时间旅行与故障保护对比]], [[continuity.at-before-statement-syntax|AT / BEFORE 查询语法]], [[continuity.undrop-recovery|UNDROP 恢复]], [[txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]], [[storage.table-types|表类型]] · 25 cards
- **Cloning considerations¶** — [[snowflak-zero-copy-clone|克隆(CLONE)的元数据本质与常见陷阱]] → [[continuity.zero-copy-clone|零拷贝克隆（zero-copy clone）]] · 6 cards
- **Transactions¶** — [[snowflak-transactions-isolation|事务、隐式提交与 READ COMMITTED 隔离级别]] → [[txn.acid-guarantees|ACID 保证]], [[txn.multi-statement-transactions|多语句事务]], [[txn.ddl-as-transaction|DDL 即事务]], [[txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]] · 20 cards
- **Introduction to loading semi-structured data¶** — [[snowflak-semistructured-loading|半结构化数据的加载与内部表示(VARIANT/ARRAY/OBJECT)]] → [[semistructured.variant-type-storage|VARIANT 类型与存储]], [[semistructured.schema-on-read-parsing|读时模式解析（schema-on-read）]] · 10 cards
- **Overview of data loading¶** — [[snowflak-data-loading-overview|数据加载总览:内部/外部 stage 与批量 COPY INTO]] → [[ingestion.bulk-copy-into|批量加载（COPY INTO）]], [[ingestion.file-formats-and-stages|文件格式与暂存区（stage）]] · 10 cards
- **Snowpipe¶** — [[snowflak-snowpipe|Snowpipe:事件驱动的自动微批加载]] → [[ingestion.snowpipe-auto-ingest|Snowpipe 自动摄取]] · 5 cards
- **Snowpipe Streaming¶** — [[snowflak-snowpipe-streaming|Snowpipe Streaming:行级流式写入与精确一次投递]] → [[ingestion.snowpipe-streaming-offset-tokens|Snowpipe Streaming 与偏移量令牌（offset token）]] · 5 cards
- **Introduction to streams¶** — [[snowflak-streams|流对象(Stream)的偏移量、类型与消费语义]] → [[pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]], [[pipelines.stream-types|流类型（标准 / 仅追加 / 仅插入）]], [[pipelines.stream-consumption-and-offset-advance|偏移量仅在消费 DML 内前移]], [[pipelines.stream-staleness-and-retention-extension|流的陈旧化与保留期延长]] · 21 cards
- **Introduction to tasks¶** — [[snowflak-tasks|任务(Task):调度、算力模型与失败处理]] → [[pipelines.task-scheduling-cron-and-dag|任务调度与 DAG]], [[pipelines.task-serverless-vs-warehouse|无服务器任务与仓库支持型任务]], [[pipelines.task-failure-handling|任务失败处理]], [[pipelines.task-conditional-execution|条件式任务执行]] · 22 cards
- **Dynamic tables¶** — [[snowflak-dynamic-tables|动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task]] → [[pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]], [[pipelines.dynamictable-incremental-vs-full-refresh|增量刷新与全量刷新]], [[pipelines.dynamictable-adaptive-refresh|自适应刷新]] · 15 cards
- **Overview of Access Control¶** — [[snowflak-access-control-rbac|访问控制总览:角色层级与 OWNERSHIP]] → [[security.rbac-role-hierarchy|RBAC 角色层级]], [[security.rbac-ownership-and-grants|所有权与授权传播]] · 11 cards
- **Understanding row access policies** — [[snowflak-row-access-policies|行访问策略(Row Access Policy):按角色过滤行]] → [[security.row-access-policies|行级访问策略（row access policy）]] · 6 cards
- **Understanding Column-level Security** — [[snowflak-column-masking|列级安全:动态数据脱敏(Masking Policy)]] → [[security.column-masking-policies|动态数据脱敏（dynamic data masking）]] · 6 cards
- Understanding end-to-end encryption in Snowflake¶ — *skipped*
- **Controlling network traffic with network policies¶** — [[snowflak-network-policies|网络策略:IP 允许/阻止名单与私有连接]] → [[security.network-policies-private-connectivity|网络策略与私有连接]] · 5 cards
- **About Secure Data Sharing¶** — [[snowflak-secure-data-sharing|安全数据共享(Secure Data Sharing)、Reader 账户与 Listing]] → [[sharing.secure-data-sharing-mechanics|安全数据共享（Secure Data Sharing）机制]], [[sharing.reader-accounts|只读账户（reader account）]], [[sharing.data-marketplace-listings|数据市场（Data Marketplace）挂牌]] · 13 cards
- **Apache Iceberg™ tables¶** — [[snowflak-iceberg-tables|Apache Iceberg 表:开放格式与目录(Catalog)选型]] → [[openplatform.iceberg-tables|Iceberg 表]], [[openplatform.polaris-catalog|Polaris（开放目录）]], [[openplatform.external-engine-commit-protocol|外部引擎写入与提交协议]] · 15 cards
- **Hybrid tables¶** — [[snowflak-hybrid-tables|混合表(Hybrid Table):行存与点查/高并发写]] → [[openplatform.hybrid-tables-oltp|混合表（Hybrid Table，Unistore）]] · 5 cards
- **Understanding overall cost¶** — [[snowflak-cost-overview|整体成本构成:计算、存储与数据传输]] → [[cost.credit-model-per-second-billing|信用点模型与按秒计费]] · 5 cards
- **Understanding compute cost¶** — [[snowflak-compute-cost-detail|计算成本细则:60 秒起收、serverless 计费与云服务 10% 免费额度]] → [[cost.warehouse-billing-60s-minimum|仓库最低计费时长]], [[cost.serverless-feature-billing|无服务器功能计费]], [[cost.cloud-services-free-tier|云服务免费额度]], [[cost.credit-model-per-second-billing|信用点模型与按秒计费]] · 20 cards
- **Working with resource monitors¶** — [[snowflak-resource-monitors|资源监控器(Resource Monitor):信用点配额与自动挂起]] → [[cost.resource-monitors-and-budgets|用资源监控器强制执行预算]], [[warehouse.resource-monitors|资源监控器（resource monitor）]] · 7 cards
- **Introduction to replication and failover across multiple accounts¶** — [[snowflak-replication-failover|跨账户复制与故障切换(Replication & Failover)]] → [[continuity.replication-and-failover|数据库复制与故障切换]] · 6 cards
- **Introduction to external tables¶** — [[snowflak-external-tables|外部表(External Table):原地查询数据湖]] → [[ingestion.external-tables-over-lake|数据湖之上的外部表]] · 6 cards

## Leaves this corpus never reached (33)
Your reading list: the map says these exist and the book does not teach them.
- [[architecture.elasticity-multitenancy|弹性与多租户]] — 秒级增减计算资源而无需重新分区数据，以及众多独立租户如何安全地共享同一个元数据/控制平面。
- [[metadata.foundationdb-role|FoundationDB 作为元数据存储]] — 为何所有表/模式（schema）/事务元数据都存放在一个强一致的分布式键值（KV）存储中，而不是一个定制的目录服务（catalog service）。
- [[metadata.execution-anchor|执行锚点（Execution Anchor）]] — 一个查询在其整个生命周期内如何被绑定到唯一一个云服务（Cloud Services）实例，以及当该实例繁忙或崩溃时，主动转移与被动转移这两条路径。
- [[metadata.query-compiler-pipeline|查询编译流水线]] — 在分配任何计算资源之前，于云服务（Cloud Services）中运行的解析（parse）、绑定（bind）、优化（optimize）阶段。
- [[metadata.ddl-metadata-versioning|DDL 即元数据版本化]] — 为何 ALTER/CREATE/DROP 都是仅涉及元数据的操作，它们创建一个新的表版本，而不是就地修改数据。
- [[metadata.metadata-scaling-consistency|元数据层的伸缩与一致性]] — 元数据层如何在同时服务一个账户内所有仓库的情况下保持强一致性，以及它在何处会成为瓶颈。
- [[warehouse.isolation-workload-separation|工作负载隔离]] — 将 ETL、BI 与临时查询（ad hoc）工作负载分别运行在独立的仓库上，使某个负载的突增不会抢占另一个负载的计算资源。
- [[query.compilation-pipeline|编译流水线]] — 解析（parse）→ 绑定（bind）→ 优化（optimize）→ 代码生成（codegen）的顺序，以及每个阶段运行在哪里。
- [[query.dag-execution-model|DAG 执行模型]] — 编译后的查询会变成一个由算子（operator）组成的有向无环图（DAG），并被分发给仓库各节点上的工作进程执行。
- [[query.vectorized-columnar-execution|向量化列式执行]] — 按批次、面向列的算子执行方式，以及为何它在分析型负载上优于逐行解释执行。
- [[query.join-strategies-broadcast-shuffle|连接（join）策略]] — 广播连接（broadcast join）与洗牌连接（shuffle/hash-repartition join）的对比，以及优化器据以选择其一的数据量启发式规则。
- [[query.explain-plan-interpretation|EXPLAIN 执行计划解读]] — 在运行查询之前读取逻辑/物理执行计划，以预测剪枝效果与连接策略。
- [[query.adaptive-runtime-optimizations|自适应运行时优化]] — 基于运行时信息做出的决策（例如自适应连接策略选择），利用实际观测到的基数在执行过程中修订计划，而不仅依赖编译期估算。
- [[cache.metadata-cache-pruning-stats|用于剪枝的元数据缓存]] — 直接缓存最小值/最大值/计数等统计信息本身，使剪枝和简单聚合运算完全无需接触数据文件。
- [[cache.cache-layer-tradeoffs|各缓存层的权衡]] — 比较每一层缓存的收益（延迟 vs 陈旧风险 vs 预热成本），以及给定症状究竟指向哪一层。
- [[txn.optimistic-concurrency-conflicts|写并发：表级锁与写冲突]] — 普通表上 UPDATE、DELETE、MERGE 会加锁，通常阻塞同表上其他 UPDATE/DELETE/MERGE，而 INSERT 与 COPY 一般可以并行；锁等待超时与死锁如何表现。
- [[continuity.clone-storage-billing|克隆的存储计费]] — 为何一个克隆在发生分叉之前不产生任何存储成本，以及分叉（任一侧发生新写入）之后如何开始累积存储费用。
- [[continuity.client-redirect|客户端重定向]] — 一种连接层面的 DNS/URL 间接寻址机制，使客户端驱动能够跟随账户的故障切换而无需重新配置。
- [[semistructured.flatten-lateral-joins|FLATTEN 与 LATERAL 连接]] — 用 FLATTEN 将嵌套的数组或对象展开成多行，以及为何这需要一次 LATERAL 连接。
- [[semistructured.schema-evolution-tables|半结构化数据源上的模式演进]] — 随着导入的 JSON/Parquet 中出现新字段而让表的列自动增长，以及约束这一过程的兼容性规则。
- [[ingestion.datastream-kafka-compatible|Datastream（兼容 Kafka 协议的摄取）]] — 一个原生流式服务，直接用 Kafka 线上协议（wire protocol）向表中写入数据，并继承 RBAC、血缘（lineage）与时间旅行（Time Travel）能力。
- [[ingestion.unload-export|数据卸载（COPY INTO location）]] — 将查询结果或表数据以文件形式导出回暂存区，以及影响下游消费者的格式/压缩选择。
- [[security.authn-mfa-sso|身份认证（MFA、SSO、密钥对）]] — 密码/多因素认证（MFA）、联合单点登录（SSO，基于 SAML/OAuth），以及密钥对认证——这几种方式在机器人/自动化场景下的适配程度各不相同。
- [[security.encryption-key-hierarchy|加密密钥层级]] — 分层的密钥结构（根密钥 → 账户密钥 → 表密钥 → 文件密钥），以及对用户完全透明的自动密钥轮换/重新加密。
- [[security.data-classification-and-tagging|数据分类与对象标签]] — 自动化的敏感数据分类，以及基于标签（tag）的策略挂载，使脱敏/行级策略能够规模化应用，而不必逐列配置。
- [[security.data-lineage-and-access-history|数据血缘与访问历史]] — 通过视图和 CTAS 追踪一列数据的来源，以及 ACCESS_HISTORY 作为记录谁实际读取或写入了哪些列的审计轨迹。
- [[security.trust-center-posture|信任中心（Trust Center）安全态势]] — 一个内置扫描器，将错误配置（公开的网络策略、过度授权等）汇总为一份按优先级排序的风险清单，无需借助外部工具。
- [[sharing.clean-rooms-privacy|数据洁净室（Data Clean Room）]] — 让双方在受治理策略约束下，对彼此的数据进行连接或聚合计算，而任何一方都看不到对方的原始行数据。
- [[openplatform.snowflake-postgres|Snowflake Postgres]] — 平台内置的、协议兼容的托管 Postgres 实例，面向需要混合表（Hybrid Table）尚不提供的事务语义的 OLTP 工作负载。
- [[openplatform.snowpark-udf-udtf|Snowpark 用户自定义函数（UDF）与表函数（UDTF）]] — 在仓库的沙箱环境中以标量函数或表函数的形式运行用户代码（Python/Java/Scala），以及由此带来的逐行调用开销。
- [[openplatform.stored-procedure-sandboxing|存储过程沙箱化]] — 围绕用户提供的存储过程代码建立的隔离边界，以及为何它默认无法访问网络或文件系统。
- [[cost.ai-token-metering|AI/Cortex 令牌计量]] — Cortex AI 函数按令牌（token）计费，与计算信用点分开单独追踪，并可设置账户级别的支出上限。
- [[cost.access-history-lineage-for-cost|将成本归因到查询模式]] — 连接 ACCESS_HISTORY 与 QUERY_HISTORY，找出究竟是哪些表、仓库或用户在驱动支出——这是在优化任何东西之前的诊断步骤。
%% trellis:end %%

## Notes
