---
title: TS09 · SQL 与数据建模
aliases:
  - TS09
  - SQL 与数据建模
tags:
  - interview/stack
  - stack/sql
stories: [S5, S10, S2]
---

# 09 · SQL 与数据建模（SQL & Data Modeling）

> 知识层（想更深时去哪）：[[System Design MOC|system-design]]：[[storage.record-modeling]] · [[storage.relational.indexing]] · [[storage.internals.lsm]] · [[analytics.olap]] · [[distributed.partitioning.skew]]；[[Snowflake Internals MOC|snowflake]]：[[storage.clustering-keys]] · [[pruning.min-max-zone-maps]] · [[pruning.partition-elimination]] <!-- domain-links -->
> 适用于：JD 上出现 SQL / data modeling / data warehouse / dbt / analytics engineering；被问"这个查询怎么优化"、"这张表你会怎么设计"。
> 不适用于：OLTP 数据库的深度调优（锁、事务隔离级别的实现、连接池）——见第 5 节。

---

## 0. 这个栈在 JD 里到底在问什么

**一、你会不会写超出 CRUD 的 SQL。** 窗口函数、CTE、`MERGE`、半结构化数据的展开。这是门槛，不是亮点。

**二、你知不知道你的 SQL 为什么慢。** 分水岭。能读执行计划、知道数据是怎么被扫的，和"加个索引试试"，差距很大。而且**数仓和 OLTP 的答案完全不同** —— 这一点很多人不知道。

**三、你设计的表能不能扛住需求变化。** 建模的真正考验不在第一版，在第三次改需求的时候。

---

## 1. 来龙去脉

### 1.1 关系模型解决的问题：让数据独立于使用它的程序

在关系模型（Codd，1970）之前，数据的组织方式和访问它的程序是绑死的——层次模型、网状模型里，改一个访问路径要改数据结构。

关系模型的核心主张是：**把数据组织成表，把"怎么取"交给查询优化器**。你声明要什么（SQL 是声明式的），系统决定怎么取。这样数据的物理组织可以独立演化，而不影响上层的查询。

这个主张的代价是你放弃了对执行方式的控制权——**当优化器选错计划时，你只能间接地影响它**（改写查询、加统计信息、加提示）。这是所有 SQL 性能问题的根源，也是为什么理解底层仍然必要。

### 1.2 范式化与反范式化：一个关于"谁付代价"的选择

**范式化**：每个事实只存一处。好处是更新只需改一个地方，不会出现同一事实的两个矛盾版本。代价是查询要 JOIN。

**反范式化**：故意冗余。好处是查询快（数据已经在一起了）。代价是更新要改多处，而且**必须有机制保证冗余副本一致，否则它们一定会不一致**。

判据不是"哪个更优雅"，是**读写比例和一致性要求**：

- OLTP（交易系统）：写频繁、要强一致 → 偏范式化
- OLAP（分析系统）：写一次读很多次、能接受延迟 → 偏反范式化

数仓里的星型模型（事实表 + 维度表）就是一个折中：事实表窄而长（每行一个事件），维度表宽而短（描述性属性），JOIN 只发生在维度上，代价可控。

**一条实用的判据**：如果冗余的那份数据是**派生的**（可以从别处重算出来），反范式化的风险就低很多——不一致了重算一遍就好。如果它是**独立写入的**，那你就有了两个真相来源，迟早出事。这和 [[01-system-design]] §2.3 里"明细永远保留、余额是派生的"是同一条原则。

### 1.3 索引：B-tree 与 LSM，两种对写入的态度

索引的本质是**用额外的写入和存储，换查询时少扫数据**。两种主流实现的分歧在于怎么对待写：

**B-tree**（Postgres、MySQL InnoDB）：原地更新一棵平衡树。读取路径短且可预测（树高约 3–4 层），但写入要找到位置、可能分裂节点，是随机 I/O。

**LSM-tree**（[[storage.internals.lsm]]，RocksDB、Cassandra）：写入先进内存表，满了顺序刷成不可变文件，后台做 compaction 合并。**写入全是顺序 I/O，所以写吞吐高得多**；代价是读可能要查多层文件（靠 bloom filter 缓解），而且 compaction 会周期性吃 I/O。

选择的判据是**写入密集程度**。但要知道的是：**这两种在数仓里都不是主角** —— 下一节说明为什么。

### 1.4 OLTP 与 OLAP：为什么数仓根本不建索引

这是本文最重要的一节，也是很多人的盲区。

| | OLTP | OLAP |
|---|---|---|
| 典型查询 | 按主键取一行，或取少数几行 | 扫几亿行，聚合出几十行 |
| 访问的列 | 一行的所有列 | 几亿行的少数几列 |
| 存储布局 | **行存**——一行的字段物理相邻 | **列存**——同一列的值物理相邻 |
| 加速手段 | 索引（精确定位少数行） | **剪枝**（跳过不需要读的数据块） |

**列存为什么对分析快，有三个独立的原因**，不只是"少读几列"：

1. **只读需要的列。** 一张 200 列的表，查询只用 3 列，就只读这 3 列的数据。I/O 直接降到 1.5%。
2. **压缩率高一个数量级。** 同一列的值类型相同、取值范围接近，往往还重复——游程编码、字典编码在这种数据上效果极好。压缩率高意味着同样的 I/O 带宽能读更多行。
3. **向量化执行。** 同类型的值连续排列，可以用 SIMD 一次处理一批，而不是一行一行走。

**而索引在 OLAP 场景下基本没有意义**：一个扫 50% 数据的聚合查询，走索引（随机 I/O 逐行取）比全扫（顺序 I/O）还慢。索引擅长的是"从一亿行里精确挑出 10 行"，分析查询做的恰恰相反。

**所以数仓的性能游戏不是索引，是剪枝** —— 在读之前就判断出"这一整块数据里没有我要的，跳过"。

### 1.5 剪枝：数仓性能的全部

现代数仓（Snowflake、BigQuery、Iceberg）把数据切成不可变的块（Snowflake 叫 **micro-partition**，通常几十到几百 MB 压缩前）。每一块都带一份元数据：**这块里每一列的最小值、最大值、非空数量、distinct 值数**。这叫 **zone map**（[[pruning.min-max-zone-maps]]）。

于是查询 `WHERE created_at = '2026-09-15'` 的执行变成：先读元数据，凡是 `max(created_at) < '2026-09-15'` 或 `min(created_at) > '2026-09-15'` 的块**整块跳过**，剩下的才真读。

**剪枝的效果完全取决于数据在块之间的排列方式。** 如果数据按 `created_at` 顺序写入，每块的时间范围窄且不重叠，按时间过滤能跳掉 99% 的块；如果数据是乱序写入的，每块都横跨所有日期，**一块都跳不掉，zone map 形同虚设**。

这就是 **clustering key**（[[storage.clustering-keys]]）的意义：告诉系统按哪些列组织数据，让同类的值聚在同一批块里。

它的取舍非常实在：
- **只对高频过滤列有意义。** 给一个从没出现在 `WHERE` 里的列建 clustering，纯浪费。
- **维护有持续成本。** 新数据不断写入会让聚集度退化，自动 reclustering 要花计算资源（真金白银）。
- **基数要适中。** 基数太低（比如只有 3 个值）分不开块；基数太高（比如唯一 ID）每块都跨全域，等于没聚。
- **列的顺序很重要。** 复合 clustering key 和复合索引一样，前缀列的过滤效果远好于后缀列。

**判断 clustering 好不好，看的不是查询快不快，是"扫了多少块 / 总共多少块"** —— 这是唯一直接反映剪枝效果的指标。

### 1.6 倾斜：分布式查询的隐形杀手

[[distributed.partitioning.skew]]。分布式执行时数据按某个 key 分到各个 worker 上，如果 key 分布不均，一个 worker 处理 90% 的数据，其余的早早干完在等它。**整个查询的耗时由最慢的那个 worker 决定。**

数据倾斜的典型来源：NULL 值（全部哈希到同一个桶）、超级大客户、默认值（`'UNKNOWN'` 这种占了一半的行）。

症状是：加机器没用，总时长纹丝不动。应对是打散热 key（加盐）、单独处理大 key、或者换 JOIN 策略（小表广播）。**"加了资源不变快"这个现象本身就是倾斜的指纹**，值得记住。

---

## 2. 在我们这套系统里它怎么用

这套系统的业务逻辑**绝大部分是 SQL** —— 不是"用 SQL 查数据"，是 Snowflake 的存储过程、UDF、task、stream 承载了核心的计费与记账逻辑。所以 SQL 质量直接等于系统质量。

### 2.1 分层建模：明细 → 派生，每层唯一输入

```
TRANSACTIONS（交易明细）
  + BRAINTREE_FEES（自收费用）
  + PASS_THROUGH_FEES（透传费用，来自 Fiserv）
  + DISPUTES（争议，来自 Arbiter 的 Kafka 事件）
        ↓
JOURNAL_ENTRIES（视图，汇总所有账本表）
        ↓  按 cutoff time 聚合
SNOWGLOBE_BALANCES（每商户每周期净额）
```

这是 1.2 那条原则的落地：**冗余的都是派生的**。`SNOWGLOBE_BALANCES` 是 `JOURNAL_ENTRIES` 的聚合，算错了改逻辑重算即可，因为明细永远在。不存在"余额和明细对不上，不知道谁对"的情况——**明细就是权威，定义如此**。

`JOURNAL_ENTRIES` 是**视图**而不是物化表，这个选择值得说：它保证了汇总口径只有一处定义，不会出现"三个地方各自 JOIN 了一遍、其中一个漏了争议"这种经典事故。代价是每次查询都要现算，所以再往下才物化成 `SNOWGLOBE_BALANCES`。**视图定口径，物化表扛性能**，是清楚的分工。

### 2.2 幂等 MERGE：一条语句里的四层设计

核心的取数 procedure `COPY_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_TO_PASS_THROUGH_FEES_STAGING`（见 [[S5]]）在一条 `MERGE` 里叠了四个独立的技巧。逐个看它们各自防什么：

**(1) 幂等键**
```sql
UNIQUE_IDENTIFIER = CONCAT_WS('_', 'INTERCHANGE', SETTLE.INVOICE_NR)
```
`MERGE ... WHEN NOT MATCHED THEN INSERT`，键是业务字段拼出来的自然键。**同一天重跑不会重复插。** 这是数据管道的第一道保险（[[10-correctness-idempotency]]）。

用自然键而不是自增代理键，是因为幂等需要一个**在重跑时能算出同样值**的东西——代理键做不到这一点。

**(2) MERGE ON 带时间窗**
```sql
ON EQUAL_NULL(STAGING.UNIQUE_IDENTIFIER, ...)
   AND STAGING.CREATED_AT > DATEADD(MONTH, -1, :LOOKUP_DATE)
```
**这一条是本文最值得学的技巧。** 没有它，每次 MERGE 都要拿新数据去比对 staging 表的全部历史——表越长越慢，而且是 O(历史长度) 的持续退化。

加上时间窗之后，`ON` 条件里有了一个可剪枝的谓词：只有最近一个月的 micro-partition 会被读（1.5 的 zone map 生效）。**扫描量从"全表"变成"一个月"，而且不随历史增长。**

这背后是一个业务判断：同一个 `INVOICE_NR` 不可能在一个月后重复出现。**性能优化的前提是一个业务不变量** —— 如果那个假设不成立，这个优化会静默地产生重复数据。这类"用业务约束换性能"的手法必须在注释里写清楚，否则后人不敢动也不知道边界在哪。

**(3) 上游就绪握手**
```sql
JOIN CLX_TRIGGER_STATUS_V1 T1
  ON T1.SUBJECT_AREA = 'Settlement' AND T1.STATUS = 'Completed'
```
不读半成品数据。这是正确性机制不是性能机制，详见 [[08-observability-oncall]] §2.3。

**(4) 逐商户开关 + 管道隔离**
```sql
WHERE IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE('JOURNAL_TRANSACTIONS', ...)
  AND PRDT_CD_ORG != '00006'   -- 排除 Amex，走 GRRCN 独立管线
```
前者是灰度（[[06-cicd-progressive-delivery]]），后者是管道隔离。

**四件事写在一条语句里，每一条都对应一类生产事故。** 这是我在面试里最愿意讲的一段代码——不是因为它复杂，而是因为每一行都能说清"不写会怎样"。

### 2.3 配置驱动的校验：把规则变成数据

Quality-Check 框架的核心是一张 `QUALITY_CHECK_CONTRACT_CONFIG` 配置表加通用 procedure 动态执行（见 [[S2]]）。

**这是一个数据建模层面的决策，不只是工程技巧**：与其为每个 subject area 写一个校验过程（N 份相似代码，改规则要改 N 处），不如把"校验什么"建模成数据，让一份通用代码去解释它。加一个校验从"写一个 procedure"变成"插一行配置"。

代价是**失去了静态检查**：配置写错了要到运行时才发现，IDE 帮不上忙。这是所有"把逻辑变成数据"的设计共有的取舍——[[04-terraform-iac]] 里把 SQL 包进 HCL 也是同一类。

### 2.4 定长文本的解析：SQL 也能干这个

GRRCN 管道里六种记录类型的定长字段解析，是写在 procedure 里的 `MERGE ... USING (SELECT SUBSTRING(...))`（见 [[07-data-pipelines-cdc]]）。

值得说的是**为什么在 SQL 里做而不是拉到应用层**：数据已经在仓库里了，拉出去解析再写回来要跨网络两趟，而且失去了 Snowflake 的并行执行。在数据所在的地方做计算，是数仓编程的基本取向。

代价是 SQL 做字符串处理很笨拙，且难以单元测试。设计文档里原本计划用 UDTF（会好一些），实现时变成了 procedure 里的 SUBSTRING —— **文档和代码的这个不一致本身就是好的面试素材**。

### 2.5 我做的部分 `[me]`

上面 2.2、2.3、2.4 三段的代码主要是我写的：

- `COPY_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_TO_PASS_THROUGH_FEES_STAGING` —— PR **#1615**，Trans View → Settle View 的取数迁移
- Quality-Check 框架 —— PR **#1997（1,489 行）**，外加约 8 次在各 fee subject area 的铺开
- GRRCN 六种记录的解析与处理 —— PR **#886（1,849 行，我最大的一个 PR）**

需要说明的边界：**`HAS_MERCHANT_DETAIL` 那个 merchant-level 改造只是 ADR 提案，状态 `Proposed`、未批准、代码里不存在**（Confluence `2894288991`）。讲这块要讲成"识别出缺陷并写了提案"，不是"改好了"。

原始证据：[[S5]]、[[S2]]、[[S1]]、本机 `raw/repo-snowglobe`。

---

## 3. stripe kit 考到的点

OA 里 SQL 思维出现得非常频繁——因为大多数题的本质就是"读入 → 分组聚合 → 定序输出"，那是一条手写的 SQL：

- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]] —— 用 dict 手写 JOIN 和 GROUP BY
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]] —— `ORDER BY` 必须给全 tie-break，否则结果不确定。**这条在 SQL 里同样成立而且更隐蔽**：并行执行下同分行的顺序每次都可能不同
- [[s11-idempotency-dedup|S11 幂等 / 去重]] —— 对应 2.2 的 MERGE 幂等键
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计]] —— 对应 2.1 的分层

`study/00-prereq/01-从SQL到Python的思维迁移.md` 正好是反向的映射，两边对照着读效果好。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| 范式化还是反范式化 | 看读写比和一致性要求；冗余的是派生数据时风险才低 | 1.2，接到 2.1 的分层 |
| 列存为什么快 | 三个独立原因：只读需要的列、压缩率高一个量级、能向量化 | 1.4 |
| 数仓为什么不建索引 | 分析查询扫大比例数据，随机 I/O 比顺序全扫还慢；数仓靠剪枝不靠定位 | 1.4 最后一段——**这一条能答好会明显加分** |
| clustering key 怎么选 | 高频过滤列、基数适中、前缀列优先；看"扫了多少块"而不是看耗时 | 1.5 的四条取舍 |
| 查询慢怎么查 | 先看 query profile 的扫描块数占比，判断是剪枝失效还是倾斜 | 1.5 + 1.6 |
| **（三层）加了机器查询没变快** | **典型倾斜。总时长由最慢的 worker 决定,加机器不改变数据分布** | 1.6；NULL / 大客户 / 默认值三类来源 |
| **（三层）MERGE 的 ON 里为什么要加时间窗** | **不加就是每次比对全部历史,O(历史长度) 持续退化。加了之后 zone map 能剪枝,扫描量恒定** | 2.2(2)。**追问"那假设不成立怎么办"——答:会静默产生重复,所以这个业务不变量必须写在注释里** |
| **（三层）配置驱动的校验有什么代价** | **失去静态检查,配置写错要到运行时才发现** | 2.3；所有"逻辑变数据"的设计共有的取舍 |

---

## 5. 我的边界

**OLTP 的深度调优不是我的领域。** 锁竞争、事务隔离级别的实现差异、死锁分析、连接池、慢查询日志调优——这些我知道概念，没实操过。
→ 我会说："我的 SQL 经验集中在数仓侧。OLTP 那套——锁、隔离级别的实现、连接池——我理解原理，但生产调优没做过。这两边的性能模型差别很大，我不想把数仓的经验假装成通用经验。"

**Postgres / MySQL 的具体运维我没做过。** 我们的 OLTP 库（pricing 用 Postgres）不归我管。
→ 我会说："pricing 那边的 Postgres 不是我的领域，我只是通过 gRPC 消费它的数据。"

**dbt 没用过。** 我们的转换编排是 Snowflake 原生的 task DAG + Flyway 迁移。
→ 我会说："我们没用 dbt，用的是 Snowflake task 的依赖链加 Flyway。概念上覆盖的是同一块——声明式转换、依赖图、测试——但 dbt 的 model/ref/test 那套约定我没实操过，上手应该不难但我不会说我熟。"

**大规模查询优化的经验有上限。** 我优化过的是分钟级的查询，不是小时级的。
→ 接回去："不过方法论是一样的：先看扫描块数判断剪枝有没有生效，再看分布判断有没有倾斜，最后才改写查询。2.2 那个时间窗就是这么找出来的。"

---

## 6. 往深里看

| 节点 | 什么时候去读它 |
|---|---|
| [[storage.record-modeling]] | 记录建模：存明细还是存聚合、键怎么设计 |
| [[storage.relational.indexing]] | B-tree 索引、复合索引、覆盖索引（我的 OLTP 补课方向） |
| [[storage.internals.lsm]] | LSM-tree 与写放大（1.3 的展开） |
| [[analytics.olap]] | 列存、向量化、OLAP 引擎的完整体系 |
| [[distributed.partitioning.skew]] | 倾斜的成因与应对（1.6） |
| [[storage.clustering-keys]] | Snowflake clustering 的维护成本与自动 reclustering |
| [[pruning.min-max-zone-maps]] · [[pruning.partition-elimination]] | 剪枝机制的细节——数仓性能的核心 |

相邻的几份：[[03-snowflake-warehouse]]（这些机制在 Snowflake 里的实现）、[[10-correctness-idempotency]]（2.2 那个幂等键的完整论证）、[[07-data-pipelines-cdc]]（这些 SQL 跑在什么管道里）。

卡片在 `vault/domains/system-design/cards/storage/`、`vault/domains/snowflake/cards/`；术语见 本机 `raw/background/03-glossary`。
