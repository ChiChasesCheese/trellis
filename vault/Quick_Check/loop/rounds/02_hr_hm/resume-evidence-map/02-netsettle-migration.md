# Net Settlement + 跨系统迁移 + Shadow-Run 对账 + PostgreSQL 数据层 —— Sr Eng 学习画像

> 用途:Chi 带着这张画像去 repo 学知识、看实现,知道往哪看齐。第 2 节是 Chi 自己已经拥有的 baseline(自信陈述),第 3 节是跨 repo 挑出来的最精华实现——**这是篇幅最大、最该反复读的部分**。标识符保留英文,叙述用中文。

---

## 1. 主题定位:这个领域到底在解决什么

### 1.1 Gross 结算 vs Net 结算(一句话本质)

一笔卡交易,商户拿到的钱不等于消费者付的钱——中间要扣掉 interchange(发卡行拿的大头)、scheme fee(卡组织 Visa/MC/Amex 拿的)、以及 BT 自己的 discount/transaction fee。**Gross vs Net 的区别在于「谁先垫这笔 IC++ 费用、什么时候结清」:**

- **Gross 结算(旧)**:商户先按毛额出款,BT 在自有账户里**先垫付**给 Fiserv / card network 的 interchange + pass-through 费用,等 Fiserv 的 TRAN/SETTLE 费用文件到齐后再回收。这段「垫付 → 回收」的时间差就是 **float**——BT 的钱被占用。
- **Net 结算(新,Fiserv direct)**:Fiserv 每日直接按**净额**(销售额 − IC++ 费用)结算给 BT,BT 不再垫付 IC++,出款周期从 **T+X 压到 T+1**。

净额到底怎么算,funding(Ruby)里的 `DisbursementQuery::NetAmounts` 写死了公式(见 §3 exemplar G):
```
net_amount = (settlement + service_fee_revenue + prefunded + escrow净额 + chargeback净额 + unauth + ...)
           - (braintree_disbursement + interchange_cost + amex_interchange_cost + recovered_prefunded)
```
被减掉的 `interchange_cost` / `amex_interchange_cost` 就是 gross 模式下 BT 要垫、net 模式下 Fiserv 直接扣掉的那部分。

### 1.2 T+X → T+1 的业务规模

Net Settlement 是承接 **$55B+ 增量 TPV** 的前提(Google ~$40B / Microsoft ~$10B / Meta ~$5–7B 这类超大 LE 商户,要 Fiserv direct + 每日净结才符合他们的现金流与对账要求),同时释放 **≈$450M/月 的 working capital float**(不再垫付 IC++)。这是一条跨越 2 年+、多季度、收入关键的旗舰线。

### 1.3 迁移全景:Ruby + Kotlin legacy → Snowflake/Java

费用计算与结算逻辑原本散落在两个 legacy 服务里,迁移的终点统一到 snowglobe(Snowflake-native SQL + Java 17):

| 源(legacy) | 语言/repo | 目标 | 为什么迁 |
|---|---|---|---|
| GRRCN / Amex 结算费用聚合脚本、`aggregated_amex_interchange_fees_*.sql.erb`、disbursement net-amount CTE | **Ruby**(`funding`) | Snowflake-native SQL + Java(`snowglobe`) | 走 Snowflake 原生管线后可对账、可 CDC 灰度、可扩到几十亿行 |
| interchange / pass-through fee 取数(原走 TRAN 视图) | Kotlin/SQL 混合(`pricing` + snowglobe 旧路径) | snowglobe SETTLE 视图取数(Java/SQL) | TRAN 视图有时在 disbursement cutoff **之后**才给数据 → 换更早到达的 SETTLE 视图,才能当日净结 |

### 1.4 PostgreSQL(OLTP)vs Snowflake(OLAP)的分工

整个费用生态是清晰的两层:

| 系统 | 数据库 | 角色 | 一句话 |
|---|---|---|---|
| `pricing`(Kotlin/Spring, gRPC) | **PostgreSQL**(主库) | OLTP | 存 pricing schedule / fee schedule / merchant account / MID 等**配置型数据**——"商户当前该被怎么收费"的 system of record。要毫秒级点查、强事务一致、唯一约束。 |
| `funding`(Ruby on Rails) | **PostgreSQL**(Aurora,分片) | OLTP | 存 disbursement / journal entry / settlement / 各卡种 fee 的**出款账务数据**——"商户实际拿到多少钱"。 |
| `snowglobe`(Java 17 + Snowflake SQL) | **Snowflake** | OLAP | 对**几十亿行**交易做 fee 计算、聚合、对账(AMEX GRRCN、Net Settlement)。 |

核心认知:**同一份 pricing schedule,在 Postgres 里是权威副本,会同步一份到 Snowflake 供 snowglobe 做大规模 fee 计算。** 为什么双写?Snowflake 是列存 OLAP 仓库,不适合"给我商户 X 今天的费率"这种单行点查;Postgres 又扛不住"扫 39B 行算聚合费用"。两边各干各擅长的——这就是 OLTP/OLAP 分层的教科书案例,而 Net Settlement 这条线恰好横跨这两层:pricing 侧在 Postgres 打 `net_settlement` 标,snowglobe 侧在 Snowflake 消费同步上来的数据做净额费用计算和对账。

---

## 2. Baseline — Chi 已经拥有的实现

Chi 是 snowglobe(BT 基于 Snowflake 的清结算/对账平台)全时段 **#1 committer**,端到端拥有 **Net Settlement Pricing** 这条旗舰线,已经 2 年+ 持续唯一 owner。这条线的三个硬核产物:

1. **Net Settlement 端到端 ownership**:plan-code/fee 映射、pass-through fee 计算、schedule 同步、审计、对 Fiserv 上报费用的 reconciliation。Jira epic 链 DTBTTFOUND-2071→2074→2232→2541→2879→**3126(P1,进行中)**,parent solution PSCBU-1645。snowglobe 侧建了 `NET_SETTLEMENT` 列 + `CHANGE_TRACKING`(为 CDC 灰度铺路),pricing 侧对应 `pricing_schedules.net_settlement` flag。

2. **Trans → Settle 视图切换(PR #1615)**:把 US credit interchange 取数从 `TRAN_FEE_BTFISERV` 切到更早到达的 `SETTLE_BTFISERV_V1`,解决 TRAN 视图晚于 cutoff 导致无法当日净结的卡点。带 feature toggle `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED`(默认 OFF、PROD 强制先 PREPROD)、独立新 task、旧路径旁挂防双计。

3. **Shadow-run 对账方法论 + CDC backfill 模板**:切换前用 day-level SQL 把 SETTLE 侧和 TRAN 侧 normalize 成同一 staging shape、`FULL OUTER JOIN` 逐字段 null-safe 比对——**单日 13.7M 行、字段一致率 >99.9%、0.224% volume variance**。整套方法沉淀成两篇 Confluence(2698298357 discovery + 2747965111 implementation,均 Chi 亲笔)和一份可复用的 "CDC Table Backfilling Template"(2747848324 + PR #1833)。

**证据锚点**:PR snowglobe **#1615**(interchange 取数切换,branch `DTBTTFOUND-2461-...`)、**#1833**(CDC backfill oob 脚本 +310/−185);Jira epic 链见上;Confluence 2698298357 / 2747965111 / 2747848324。

下面第 3 节把这条线上「最值得当学习标杆的实现」逐个拆开——既包括 Chi 自己的核心工件,也集百家之所成挖出这个领域里最漂亮的实现。

---

## 3. ★ 往哪里看齐 —— repo 最精华实现(重点)

挑了 9 个跨 repo 的实现,按「精华在哪 / 为何 Sr 级 / 路径+锚点 / 学到什么程度」拆解。**A/B/C 是 Chi 这条线的核心工件(自信当 baseline 深读),D–I 是生态里最该学的配套实现。**

---

### A. Shadow-run day-level 对账 SQL —— 这个领域的皇冠

**精华在哪**:切换数据源前不是"切了再看",而是**切换前**用一条 day-level SQL 把两个视图都 normalize 成完全相同的 staging shape,再 `FULL OUTER JOIN` 逐字段比对。关键手法有四层:
- **两个对称 CTE**:`settle_norm`(从 `SETTLE_BTFISERV_V1` 映射)和 `trans_norm`(从 `TRAN_FEE_BTFISERV`)。`trans_norm` 通过 `JOIN FEE_SEQUENCE_CODES FSC ON ... AND LOWER(FSC.FEE_TYPE)='interchange'` **只取 interchange**,保证与 SETTLE 侧 1:1 可比(SETTLE 天然只有 interchange)。
- **稳定的 join key**:`transaction_public_id + mid + plan_code + record_date + currency + payment_network` 六元组,而不是靠某个单一 ID。
- **null-safe 逐字段相等**:每个字段用 `EQUAL_NULL(...)` 比(fee_amount 先 `ROUND(...,4)` 消浮点噪音),把结果落成一列列 `eq_*` 布尔——**一眼看出是哪个字段不一致,而不是只知道"这行不一样"**。
- **差异归因到底**:结论是 >99.9% 字段一致(两侧都有记录时),≈0.07% mismatch 全是"只在单侧当天出现"的时序差——并用 **±3 天窗口**验证这不是真冲突。唯一系统性差异是 SETTLE 天然缺 `FEE_SEQUENCE_CODE` 和 `ALT_DISPUTE_ID`,而这俩对 interchange journaling 都非必需。

**为何 Sr 级**:大多数人做迁移是"切完对总数",这套是"切之前就把两个 source 拉平到字段级、把 0.07% 的每一行都解释清楚是时序而非错误"。这是把"zero regression"从口号变成可辩护证据的方法论。变量口径也算得干净:`(13,768,430 − 13,737,670) / 13,737,670 = 0.002239 ≈ 0.224%`。

**路径+锚点**:Confluence **2698298357**(完整 day-level 对账 SQL,含 `settle_norm`/`trans_norm`/`cmp` 三段 + 映射规范 + ALT_DISPUTE_ID/FEE_SEQUENCE_CODE 差异分析)、**2747965111**(Data Validation 表 + 单侧 count 校验 query)。两篇均 Chi 亲笔(authorId `96f8d728`)。

**学到什么程度**:能默写出这套结构——两个 normalize CTE、六元组 join key、`EQUAL_NULL` 逐字段落布尔、单侧差异用时间窗口证伪。**这是任何跨系统数据源迁移都能直接套用的通用模板**,不限于 Fiserv。

---

### B. SETTLE 取数 stored procedure —— 幂等 + handshake + 逐户灰度

**精华在哪**:`COPY_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_TO_PASS_THROUGH_FEES_STAGING(LOOKUP_DATE)` 一个 proc 里塞了四个 Sr 级细节:
- **幂等 MERGE**:`MERGE ... WHEN NOT MATCHED THEN INSERT`,`UNIQUE_IDENTIFIER = CONCAT_WS('_','INTERCHANGE', SETTLE.INVOICE_NR)`——同一天重跑不会重复插。
- **MERGE ON 带限窗**:`ON EQUAL_NULL(STAGING.UNIQUE_IDENTIFIER, ...) AND STAGING.CREATED_AT > DATEADD(MONTH, -1, :LOOKUP_DATE)`——防止每次 MERGE 全表扫历史 staging,只比最近一个月。
- **trigger-status handshake**:`JOIN CLX_TRIGGER_STATUS_V1 T1` 且 `T1.SUBJECT_AREA='Settlement' AND T1.STATUS='Completed' AND T1.PLATFORM='North'`——**只有当上游宣告"这天的 Settlement 数据已就绪"才读**,不读半成品。
- **merchant-level gate**:`WHERE IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE('JOURNAL_TRANSACTIONS', MA.BUSINESS_COUNTRY_ISO_CODE, MA.UNIQUE_IDENTIFIER, CURRENT_TIMESTAMP())`——逐户开关,而非全局。外加 `PRDT_CD_ORG != '00006'` 排除 Amex(Amex 走 GRRCN 独立管线)。

**为何 Sr 级**:一个"取数"proc 同时做到了幂等、抗全表扫、上游就绪握手、逐户灰度、跨管线隔离——每一条都是生产事故的常见来源,这里一次性全防住。`FEE_AMOUNT = SETTLE.IC_FEE_AM`(天然负值)、`FEE_SEQUENCE_CODE = NULL`、`FEE_SOURCE='SETTLE_BTFISERV_V1'`、`FEE_CATEGORY='SETTLEMENT'` 的字段口径也和对账 SQL 完全对齐。

**路径+锚点**:`snowglobe/app/src/main/resources/db/stored-procedures/pass_through_fees/R__create-stored_procedure-copy-fiserv-credit-interchange-from-settle.sql`(PR #1615)。

**学到什么程度**:记住"取数 = 幂等 MERGE + 限窗 ON 条件 + 上游 status handshake + 逐户 feature gate"这套组合拳,能解释每一条为什么存在。

---

### C. 旧路径旁挂防双计 —— zero-regression 的真正保证

**精华在哪**:切换不是"删旧建新",而是**旧路径不动、新路径旁挂,用一个 toggle 精确切走重叠部分**。修改后的 TRAN 取数 proc 里加了这段条件:
```sql
AND (
  IS_FEATURE_ACTIVE('US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED') = FALSE
  OR UPPER(TRANFEE.FEE_DATA_SOURCE) = 'CHARGEBACK'
  OR LOWER(TRIM(COALESCE(FSC.FEE_TYPE, ''))) != 'interchange'
)
```
- toggle **OFF**:所有费用(含 interchange)照旧从 TRAN 取——**原行为一字节不变**。
- toggle **ON**:从 TRAN 分支里**只排除 normal interchange**(scheme / chargeback / auth / non-tran 永远仍走 TRAN),interchange 改由 SETTLE proc 单独取。
- 用一个独立新 task `FETCH_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_STAGING`(cron `15 6-9 * * * America/Chicago`,cutoff 前的清晨拿 SETTLE 早到优势)与旧 task 并行、条件执行。

**为何 Sr 级**:这是"strangler fig"迁移模式在 SQL 管线里的精确落地——新旧并存、按数据类别切、随时能一键切回。双计(interchange 被 TRAN 和 SETTLE 各算一次)是这类迁移最凶的坑,这里用"从旧分支条件排除"而非"靠 MERGE 去重"来根治(discovery 文档明确写了 *"avoid double counting by source filtering rather than relying on MERGE equality alone"*)。

**路径+锚点**:`snowglobe/.../stored-procedures/pass_through_fees/R__create-stored_procedures-required-for-pass-through-fees-staging-credit.sql`(第 76–82 行的 toggle 条件);toggle 建表 `V20251021130500__add-us-credit-interchange-from-settle-feature.sql`;PROD 强制关 `V20251120140000__disable-us-credit-interchange-from-settle-in-prod.sql`。

**学到什么程度**:能讲清"为什么用 source filtering 排除而不是 MERGE 去重",以及"toggle OFF 时新代码路径对旧行为零影响"是怎么用一个布尔条件保证的。

---

### D. CDC backfill 模板 —— 历史数据回填的可复用套路

**精华在哪**:把 Data Lake 的历史 dimension 数据回填进 snowglobe 的 CDC replica 表,固化成一个 4 步模板(文件头注释直接写明):
1. **COPY INTO TEMP staging**:`CREATE TEMP TABLE _STG_xxx LIKE 目标表`,再从 external stage(`@DATALAKE_S3_STAGE/funding/.../`,PARQUET + LZO)`COPY INTO`,`ON_ERROR = CONTINUE` 容错。每个字段用 `TRY_TO_NUMBER/TIMESTAMP/BOOLEAN` 安全转型。
2. **MERGE staging → target**:`ON TGT.ID = SRC.ID`,`WHEN MATCHED UPDATE / WHEN NOT MATCHED INSERT`——**注释明确写了"Direct COPY INTO may lead to duplicates",所以必须过 MERGE**,不能直灌。
3. **event timestamp 兜底**:`SOURCEDB_EVENT_TS = COALESCE(timestamp → updated_at → created_at)`,都没有才留 NULL——CDC 排序/去重的时间基准永远有值可用。
4. **覆盖一组表**:`FUNDING_CDC_MERCHANT_ACCOUNTS` / `FUNDING_PRICING_SCHEDULES` / `FUNDING_PRICING_SCHEDULE_FEES`(单表 1.07 亿行)/ `FUNDING_PROCESSOR_SETTINGS`,每张表同一套模式。

**为何 Sr 级**:回填最容易翻车的两点——重复插入、时间基准缺失——被"TEMP + MERGE"和"COALESCE 三级兜底"系统性根治;PARQUET/LZO + `TRY_TO_*` + `ON_ERROR=CONTINUE` 让脏数据不阻断整批。这不是一次性脚本,是被写成团队可复用模板(配 Confluence 文档)的基建。

**路径+锚点**:`snowglobe/app/src/main/resources/db/oob-migrations/copy-datalake-cdc-to-snowglobe-ma-mids-ps-psf.sql`(PR #1833,+310/−185);Confluence "CDC Table Backfilling Template" 2747848324。

**学到什么程度**:能默写 4 步骨架,并解释"为什么不能 COPY INTO 直灌目标表""为什么 event_ts 要三级 COALESCE"。

---

### E. Postgres → Snowflake 应用层同步 —— OLTP/OLAP 之间怎么连

**精华在哪**:pricing 服务在 Postgres 里成功创建/更新一个 pricing schedule 后,**不是靠 Debezium/CDC,而是应用层异步 dual-write** 到 Snowflake 的 snowglobe schema:
- `PricingScheduleService.kt` 里 `launch(Dispatchers.IO)` 起协程,并行 sync `pricing_schedules_v1` / `_v2` / snowglobe 三路,最后 `.join()` 汇合;写 snowglobe 那路是 fire-and-forget(`// always return true as status, for now don't consider snowglobe sync status`),不阻塞主 gRPC 响应。
- 通过 `SnowflakeDataUploader` + `SnowglobeQueries` upsert,带**幂等 + 冲突检测**:Snowflake 里已存在同 public_id 但值不同 → 抛 `FAILED_PRECONDITION`("cannot update existing record")。
- 反方向:pricing 也**从 Snowflake 读** Fiserv 的 interchange/scheme 原始费用(`SnowflakeDataFetcher` + `FiservSnowflakeQueries`)落进 Postgres 的 `interchange_fees` / `scheme_fees` 表。所以 pricing 既是 Snowflake 的生产者也是消费者。

**为何 Sr 级**:这是两个异构存储(OLTP Postgres ↔ OLAP Snowflake)保持最终一致的真实工程解——用应用层异步而非 CDC(权衡:简单、可控冲突语义,代价是弱一致 + fire-and-forget 丢失风险),并显式用 `FAILED_PRECONDITION` 把"值冲突"和"新写入"区分开。面试常问"你们两个库怎么同步",这就是标准答案的活样本。

**路径+锚点**:`pricing/src/main/kotlin/com/braintree/pricing/api/PricingScheduleService.kt`(L154–233 sync 协程区);`client/snowglobe/SnowflakeDataUploader.kt`、`SnowglobeQueries.kt`;反向 `worker/fiserv/SnowflakeDataFetcher.kt`、`FiservSnowflakeQueries.kt`;配置 `PricingSnowflakeConfiguration.kt`(同时含 read/write 两组 role/db/schema)。

**学到什么程度**:能讲出这句话——"pricing 变更走应用层异步 sync 上 Snowflake,带幂等和冲突检测(值冲突抛 FAILED_PRECONDITION);Fiserv 费用反向从 Snowflake 拉进 Postgres;我在 snowglobe 那侧消费的就是这份被同步上来的 pricing 数据",并能说清为什么不用 CDC。

---

### F. Postgres schema/migration —— 按字节宽度排列列的存储级 craft

**精华在哪**:pricing 库 96 表 / 526 个 Flyway migration。每个 `V<timestamp>__desc.sql` 是不可变变更,Flyway 顺序执行并在 `flyway_schema_history` 记录;配置(`build.gradle.kts` 的 `flyway {}`)里 `outOfOrder = true`(多人并行开发允许乱序补跑)、prod/qa `cleanDisabled = true`(防误删生产库)。最精华的是**建表列顺序规范**——migration 头部注释写死:
> Postgres 在 64 位系统上按 8 字节对齐每列的磁盘存储,小于 8 字节的值会被 padding。**按字节宽度递减排列列**(primary key → bigint → timestamp → integer → date → enum → numeric → text → boolean)能让小值打包在一起,减少 padding 浪费的磁盘。

`net_settlement BOOLEAN`(Net Settlement 这条线在 Postgres 侧的落点)正是因为 boolean 最小,排在列顺序最后。

**为何 Sr 级**:大多数团队的 migration 是"能跑就行",这里把 Postgres 的 tuple 物理布局(8 字节对齐 padding)写进了团队规范并逐 migration 执行——这是懂存储引擎的信号。加上 `outOfOrder` / `cleanDisabled` 的环境分治,是一套成熟的 schema 演进工程。

**路径+锚点**:`pricing/src/main/resources/db/migration/V20240905104646__add_net_settlement_to_pricing_schedule.sql`(头部字节对齐注释 + `ALTER TABLE ... ADD COLUMN net_settlement BOOLEAN` 打在 `pricing_schedules` 和 `pricing_schedules_v2` 两张表);`build.gradle.kts` 的 `flyway {}` 块。

**学到什么程度**:能解释"为什么 boolean 放最后""什么是 8 字节对齐 padding""outOfOrder / cleanDisabled 各防什么"。这是 Postgres 面试里能让人眼前一亮的存储细节。

---

### G. net_amounts.rb —— 净额公式的 source of truth(legacy Ruby)

**精华在哪**:`DisbursementQuery::NetAmounts` 用 15 个 CTE(`SettlementAmounts` / `InterchangeCosts` / `AmexInterchangeCosts` / `ChargebackAmounts` / `PrefundedAmounts` / `HeldInEscrowAmounts` / ...)各算一块金额,主 query `LEFT OUTER JOIN` 全部挂到 `merchant_accounts.id` 上,再一个大 `(收入项之和) - (成本项之和)` 算出 `net_amount`,每项都 `COALESCE(..., 0)` 防 NULL 传染。**这是"net 到底怎么算"的权威定义**——gross vs net 的差异,本质就是 `interchange_cost` / `amex_interchange_cost` 这两项由谁垫、何时结。

**为何 Sr 级**:把一个复杂的账务净额拆成 15 个正交的、可单独测试/复用的 CTE(每个 CTE 是独立的 `DisbursementQuery` 类,`self.ctes` 列出来组装),而不是一条几百行的巨型 SQL——这是可维护的金融计算代码范本。`LEFT OUTER JOIN + COALESCE(,0)` 保证"某商户某类金额缺失"时是 0 而非整行 NULL,这在钱的计算里是硬要求。

**路径+锚点**:`funding/app/models/disbursement_query/net_amounts.rb`;各分项在 `funding/app/models/disbursement_query/*.rb`(如 `interchange_costs.rb`、`amex_interchange_costs.rb`、`pricing_interchange_fee_record_costs.rb`)。

**学到什么程度**:能背出净额公式的结构(收入项 − 成本项、逐项 COALESCE),并指出 `interchange_cost`/`amex_interchange_cost` 就是 float 的来源。这是把 Net Settlement 业务讲透的地基。

---

### H. journaling_schedules —— 记账归属的 OLTP 边界表

**精华在哪**:一张极简但极关键的表,定义"某商户从某天起由谁记账":
```
merchant_account_unique_identifier  text
effective_date                      date
journaling_method  enum(funding, snowglobe)   -- ← 谁记这个商户的账
```
`JournalingScheduleRepository` 里那条 native query(取 `effective_date <= :date` 里最新一条)就是"某商户此刻归谁记账"的判定——**费率是有时间版本的,记账归属也是**。这张表是 funding 和 snowglobe 两个记账系统之间的产权边界。

**为何 Sr 级**:用"带 effective_date 的 schedule 表 + 取最新一条"这个模式表达"随时间迁移的归属",而不是一个会被覆盖的布尔 flag——保留了完整历史、支持"任意历史时点谁记账"的回溯查询。这正是 Net Settlement 迁移(商户逐户从 funding 切到 snowglobe)需要的数据结构,也是防重复计费(Pricing 不能对已迁到 snowglobe 的商户再算一遍)的判据来源。

**路径+锚点**:`pricing/src/main/kotlin/com/braintree/pricing/common/data/JournalingSchedule.kt`、`JournalingScheduleRepository.kt`、`api/JournalingScheduleService.kt`;表 `journaling_schedules`。

**学到什么程度**:能解释"为什么归属要用 effective-dated schedule 表而非布尔 flag",以及这张表如何界定 snowglobe 领域的边界。

---

### I. 逐户 shadow 灰度 + 环境分治 —— 灰度切换的真实操作

**精华在哪**:切换不靠一个全局大开关,而是**先在一批 shadow 商户上跑、验证后再扩**,分三层控制:
- **全局 toggle**:`US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED`(SYSTEM_TOGGLES,默认 FALSE)。
- **环境分治**:`V20251120140000__disable-...-in-prod.sql` 专门在 PROD 强制关掉——先在 PREPROD 验,PROD 后开。
- **merchant 级灰度**:一连串 migration(`V20250409171105__enable-net-settlement-mechants-for-shadowing.sql` 对首批 58 商户 MERGE 打开 `JOURNAL_TRANSACTIONS` + `JOURNAL_PASS_THROUGH_FEES`,后续 `V20250821...__enable-sept-merchants`、`V20250919...__enable-shadowing-for-octob-merchant-accounts`、`V20260128...__shadowing-2-bt-global-eu-alpha-cohort` 按月/按 cohort 逐批扩)。取数 proc 里再靠 `IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE(...)` 逐户 gate。

**为何 Sr 级**:这是"feature toggle × 环境 × 逐户 cohort"三维灰度的完整落地——爆炸半径始终可控,任何一批出问题只影响那批商户,且能一键切回。migration 文件名本身就是一部灰度节奏的编年史(4 月 58 户 → 9 月 → 10 月 → 次年 1 月 EU alpha cohort)。

**路径+锚点**:`snowglobe/app/src/main/resources/db/squashed/` 下 `V20250409171105__enable-net-settlement-mechants-for-shadowing.sql`、`V20250821111842__enable-sept-merchants-for-shadowing.sql`、`V20250919164910__enable-shadowing-for-octob-merchant-accounts.sql`、`V20260128133124__shadowing-2-bt-global-eu-alpha-cohort-merchants.sql`;PROD 关闭 `V20251120140000__disable-us-credit-interchange-from-settle-in-prod.sql`。

**学到什么程度**:能讲清"全局 toggle / 环境分治 / 逐户 cohort"三层各解决什么,以及为什么金融系统的切换必须是逐户扩而非一次全开。

---

## 4. 知识点体系

**OLTP vs OLAP 为什么必须分层**
OLTP(Postgres)要的是毫秒级单行点查/写、强事务一致、唯一约束——服务 gRPC 的"给我商户 X 的费率""创建一个 pricing schedule"。OLAP(Snowflake)是列存、面向全表扫描——服务"扫 39B 行算聚合费用"。互相不能替代:Snowflake 单行点查慢、无传统 OLTP 事务语义、无行级唯一约束;Postgres 扛不住几十亿行聚合。用对工具就是分层的本质。

**事务一致性为什么对计费是生死线**
钱不能算错、更不能算两次。一个 pricing schedule 头 + N 条 fee 明细必须**原子性**一起写(否则出现"有头没明细"的商户,fee 计算要么崩要么算错);唯一约束(`uidx_*`)防重复 schedule / 重复 MID;强 schema(enum、NOT NULL、外键)是第一道防线。迁移里的"双计"(interchange 被两个 source 各算一次)本质就是一致性问题,靠 exemplar C 的 source filtering 根治。

**CDC / journaling sync 的两条路**
(1) 应用层异步 dual-write(exemplar E):pricing → Snowflake,简单可控、弱一致。(2) Data Lake → Snowglobe CDC replica 的批量回填(exemplar D):COPY INTO TEMP + MERGE + event_ts 三级兜底。两者服务不同场景:前者是在线增量,后者是历史/补数。`journaling_schedules`(exemplar H)则用 effective-dated 表表达"归属随时间迁移",是迁移期的产权判据。

**shadow 对账方法论(可迁移到任何数据源切换)**
切换前 → 两侧 normalize 成同一 shape → 稳定多元组 join key → `EQUAL_NULL` 逐字段落布尔 → 量化字段一致率 → 单侧差异用时间窗口(±N 天)证伪为时序而非错误 → 只保留系统性可解释的差异(如 SETTLE 天然缺 FEE_SEQUENCE_CODE)。这套是 exemplar A,是"zero regression"从口号到证据的桥。

**灰度切换的三维**
全局 feature toggle(默认 OFF)× 环境分治(PROD 强制先 PREPROD)× 逐户/逐 cohort 扩(merchant-level feature flag)。爆炸半径始终可控、随时可切回——见 exemplar B(逐户 gate)+ C(toggle 旁挂)+ I(cohort 编年史)。

---

## 5. 学习锚点表

| 要学的能力 | 看齐标杆(exemplar) | 路径 / 锚点 | 学到什么程度 |
|---|---|---|---|
| 迁移前字段级对账方法论 | **A** shadow-run SQL | Confluence 2698298357 / 2747965111(Chi 亲笔) | 默写两 CTE + 六元组 key + `EQUAL_NULL` 落布尔 + ±3天证伪 |
| 幂等取数 proc | **B** SETTLE copy proc | `snowglobe/.../pass_through_fees/R__create-stored_procedure-copy-fiserv-credit-interchange-from-settle.sql` | 讲清幂等 MERGE / 限窗 ON / status handshake / 逐户 gate 各为什么 |
| 无回归迁移(strangler) | **C** 旧路径旁挂防双计 | 同上 `...staging-credit.sql` L76-82 + toggle 建表/PROD关闭 migration | 讲清 source filtering vs MERGE 去重、toggle OFF 零影响 |
| 历史数据回填 | **D** CDC backfill 模板 | `snowglobe/.../oob-migrations/copy-datalake-cdc-to-snowglobe-ma-mids-ps-psf.sql`(#1833)+ Confluence 2747848324 | 默写 COPY INTO TEMP → MERGE → COALESCE event_ts 4 步 |
| OLTP↔OLAP 同步 | **E** 应用层 dual-write | `pricing/.../api/PricingScheduleService.kt` L154-233 + `SnowflakeDataUploader/Fetcher` | 讲清"为什么不用 CDC""FAILED_PRECONDITION 区分什么" |
| Postgres 存储级 schema | **F** 字节对齐列排序 + Flyway | `pricing/.../migration/V20240905104646__...net_settlement...sql` + `build.gradle.kts flyway{}` | 解释 8 字节对齐 padding / boolean 放最后 / outOfOrder / cleanDisabled |
| 金融净额计算范式 | **G** net_amounts.rb | `funding/app/models/disbursement_query/net_amounts.rb` + 各分项 CTE | 背净额公式结构 + 指出 interchange_cost 是 float 来源 |
| effective-dated 归属边界 | **H** journaling_schedules | `pricing/.../common/data/JournalingSchedule*.kt` | 解释为什么用 schedule 表而非布尔 flag 表达归属 |
| 三维灰度切换 | **I** 逐户 shadow cohort | `snowglobe/.../squashed/V2025...enable-...-shadowing.sql` 系列 + PROD 关闭 migration | 讲清全局toggle/环境/cohort 三层各防什么 |

---

## 6. 面试怎么讲

**30 秒电梯版(业务规模先行)**
"我端到端拥有 Braintree 的 Net Settlement 这条线——把 LE/MM 大商户从 gross 结算迁到 Fiserv 每日净额直连,出款周期从 T+X 压到 T+1。这是承接 **$55B+ 增量 TPV**(Google/Microsoft/Meta 这类客户)的前提,同时释放大约 **$450M/月的 working capital**,因为 BT 不再需要垫付 interchange 等 IC++ 费用等 Fiserv 文件来回收。"

**技术深挖版(迁移 + 对账)**
"这条线最硬的一块是把 interchange 取数从 Fiserv 的 TRAN 视图切到更早到达的 SETTLE 视图——TRAN 有时晚于 disbursement cutoff,数据就当天结不了净额。我做的不是切完再看,而是切之前先做字段级 shadow 对账:把两个视图 normalize 成完全相同的 staging shape,用一个稳定的六元组 key 做 FULL OUTER JOIN,每个字段用 EQUAL_NULL 落成布尔,量化下来是**单日 13.7M 行、字段一致率 >99.9%、volume variance 0.224%**;剩下 0.07% 的差异全是只在单侧当天出现的记录,我用 ±3 天窗口证明是时序差而不是数值错误。上线用 feature toggle 默认 OFF、PROD 强制先 PREPROD,旧路径不删、新路径旁挂——toggle ON 时只把 interchange 从旧的 TRAN 分支条件排除,靠 source filtering 而不是 MERGE 去重来防双计。灰度是逐户的,从首批 58 个 shadow 商户按月扩 cohort。"

**OLTP/OLAP 版(Postgres)**
"我们的费用生态是 Postgres(OLTP)和 Snowflake(OLAP)两层。Postgres 是 pricing 服务的主库,存 pricing schedule、fee schedule、merchant account 这些配置型数据,是费率的 system of record,要毫秒级点查和强事务一致——计费不能算错也不能算两次。我主战场 snowglobe 在 Snowflake 上,对几十亿行做聚合费用计算。两边怎么连?pricing schedule 在 Postgres 写成功后,通过应用层异步 sync upsert 一份到 Snowflake,带幂等和冲突检测——值冲突会抛 FAILED_PRECONDITION;反方向 Fiserv 的 interchange 费用又从 Snowflake 拉回 Postgres 参与计费。我在 Snowflake 那侧消费的就是这份被同步上来的 pricing 数据。Net Settlement 在 Postgres 侧就是 `pricing_schedules` 上那个 `net_settlement` flag——顺带一提,他们的 migration 有个很讲究的规范,建表列按字节宽度递减排(bigint→timestamp→...→boolean),为的是让 Postgres 8 字节对齐时少浪费 padding。"
