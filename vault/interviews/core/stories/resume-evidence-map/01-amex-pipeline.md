# 学习画像 01 · AMEX Transaction-Fee 计算系统 / 端到端支付管线

> 用途:学习标杆,不是简历审计。这份文档把「Amex GRRCN 交易费管线」这条线上**最高水平的实现**集中起来,让 Chi 知道往哪里看齐。
> 结构:① 全景定位 → ② Chi 的 baseline → ③ ★往哪里看齐(重点) → ④ 知识点体系 → ⑤ 学习锚点表 → ⑥ 面试话术。
> 所有路径为绝对路径或 repo 相对路径(标识符/表名/文件名一律英文)。只读,未改动任何代码。

---

## 1. 主题定位:一个 Sr Eng 眼里的端到端 Amex Fee 管线全景

Amex 和 Visa/MC 不一样:Amex 既是发卡行又是收单网络(closed loop),它不走 interchange 文件,而是每天给收单方(Braintree)发一份**专有定宽结算文件 GRRCN**(Global Reconciliation Report & Chargeback Notification)。这份文件里既有交易明细、又有 Amex 收取的费率明细(transaction pricing),还有 chargeback / adjustment / summary。Braintree 要做的是:把文件吃进来 → 解析出每笔交易和它的定价 → 算出该向商户收的 Braintree interchange fee → 落进总账 → 触发出款。整条线在 Snowglobe(Braintree 基于 Snowflake 的清结算平台)里被重写成 **Snowflake-native** 的 task/stream/proc/UDTF 编排,取代了 Funding 里的老 Ruby 脚本。

**七个环节,每环点名真实工件:**

```
[Funding 落 GRRCN 定宽文件到 S3]  @FUNDING_S3_STAGE/outbound/aggregated-amex/YYYY-MM-DD/
        │  ① INGESTION —— TASK STAGE_AMEX_GRRCN_FILE(30min 调度 + feature-flag 门控)
        │     COPY INTO … FILE_FORMAT(FIELD_DELIMITER=NONE) 整行入表,GRRCN_FILE_ID=UUID
        ▼
  TABLE AMEX_GRRCN_STAGING(RECORD_TYPE=TRIM(LEFT($1,10)), RECORD_TEXT=整行, CHANGE_TRACKING=TRUE)
        │  ② FAN-OUT —— 6 条 APPEND_ONLY stream 按 record type 各自分流
        ▼
  6 个 PROCESS_AMEX_GRRCN_*_TASK(AFTER root + WHEN SYSTEM$STREAM_HAS_DATA)
        │  ③ PARSE —— proc 内 SUBSTRING(RECORD_TEXT,pos,len) + TRY_CAST/TRY_TO_DATE + MERGE
        ▼
  6 张 RAW 表:AMEX_GRRCN_{SUMMARY, TRANSACTIONS, TRANSACTION_PRICING, FEE_REVENUE, ADJUSTMENTS, CHARGEBACKS}
        │  ④ MOVEMENT —— TASK AMEX_PENDING_TRANSACTIONS_TO_TRANSACTIONS
        │     调 UDTF VALIDATE_AMEX_GRRCN_TRANSACTIONS_AND_CONSOLIDATE()(join PENDING_TRANSACTIONS、算 effective_date、滤 REJ)
        ▼
  TABLE TRANSACTIONS(Snowglobe 规范交易表)
        │  ⑤ FEE CALC —— TASK AGG_AMEX_INTERCHANGE_FEE_CALCULATION_TASK(双父依赖)
        │     CALL CALCULATE_AGGREGATE_AMEX_INTERCHANGE_FEE()(三表 join + 资格过滤 + 聚合 + MERGE)
        ▼
  TABLE braintree_fees(ledger_sub_kind = amex_interchange_flat / _discount / european_amex_interchange;amount 存 -1×)
        │  ⑥ FUND TRANSFER —— braintree_fees → journal_entries → balances
        │     TASK TRANSFER_DISBURSEMENTS_TO_ARBITER(5min)→ CREATE_ARBITER_DISBURSEMENTS_MESSAGES()→ Funding/Arbiter 出款
        │  ⑦ OBSERVABILITY —— CHECK_FUNDING_TRANSFERS_SLA + quality-check 框架(QUALITY_CHECK_RESULTS_V1)全程盯梢
        ▼
  [商户实际收款]
```

一个 Sr Eng 看这张图,看的不是「数据从左流到右」,而是四条隐藏的主线:**(a) 幂等**——同一个文件重跑几次结果不变;**(b) 事件驱动**——没有新数据就不烧 warehouse;**(c) 可急停**——一个 toggle 就能在不发版的情况下切断整条流;**(d) 错误旁路**——坏数据被记进 error_logs 而不是阻断主流程。这四条是本文所有「看齐标杆」的共同底色。

---

## 2. Baseline — Chi 已有的实现(起点)

Chi 是这条 Amex GRRCN 管线的 **end-to-end owner**,也是 snowglobe 主 repo 的全时段 #1 committer(615 commits / 63 merged PR / 17.1K+ 行)。他从前任(Simrandeep Singh)留的 stub 起步,独立完成了整条线的设计与落地:

- **架构**:`STAGE_AMEX_GRRCN_FILE` 根任务 + 6 条 append-only stream + 6 张 raw 表 + 解析/校验的 proc 与 UDTF + 7 张 staging/target 表 + feature-flag 急停 `AGGREGATED_AMEX_SEPARATE_FLOW`。
- **迁移**:把原本在 Funding 里的 Ruby `amex_settlement_parser` 定宽解析逻辑,整套翻译成 Snowflake-native SQL(定宽 byte offset → `SUBSTRING`)。
- **扩展**:从 US OptBlue 扩到 EU(`european_amex_interchange` / `amex_settlement_eur_grrcn` 文件 / EU aggregator SE number 分类),18 个月生产防御。
- **量级**:2025 年经此管线处理 **21,964,869 笔 Amex 交易 / $138,630,471,670 volume**(Chi 自己的 Impact Summary,Confluence 2750481503);任期最大单 PR #886 达 1,849 行。
- **锚点**:PR snowglobe #751/#856/#862/#886/#911/#1023 + ~10 个 hardening PR、#2598(EU 扩展)、#2820(`_WITH_SOURCE` 版本);Jira DTBTTFOUND-1960/1961/2084/2097/2139,epic 2074;Confluence 2233926829(设计)、1112867224(aggregation 语义)。

这就是起点。下面是把这个起点里每一环做到极致的样子——即 Chi 该往哪里看齐。

---

## 3. ★ 往哪里看齐 —— repo 最精华的 8 个实现(本文重点)

> 集百家之所成:跨 snowglobe / amex_settlement_parser / kafka-snowflake-connector / business_date 四个 repo,挑出这条线上最值得学的 8 个实现。每个讲清:**精华在哪 / 为什么是 Sr 级 / 文件路径 / 该学到什么程度**。

---

### 标杆 1 —— fee 计算主 proc:`CALCULATE_AGGREGATE_AMEX_INTERCHANGE_FEE_WITH_SOURCE`

**路径**:`app/src/main/resources/db/stored-procedures/braintree_fees/R__create-agg-amex-interchange-fee-calculation-with-source-stored-procedure.sql`

这是整条线的心脏,也是全 repo 最值得逐行读的一个 proc。它把「一份 GRRCN 定价记录 → 一条 Braintree fee」这件事,用一个 SQL proc 做到了幂等、可测、错误自愈。

**精华在四点:**

1. **`IDENTIFIER(:SOURCE_TABLE)` = SQL 层的依赖注入**。proc 签名带一个 `SOURCE_TABLE VARCHAR` 参数,内部用 `FROM IDENTIFIER(:SOURCE_TABLE) AS fee` 读源。生产里传的是 live stream,测试里传的是 fixture 表——**同一段业务逻辑,prod 和 test 走完全一致的代码路径**。这是全 repo 最干净的可测性 seam。

2. **`LEFT JOIN` 故意保住「匹配不到」的行**。fee → `transactions`(`ON LOWER(t.public_id)=LOWER(fee.reference_number)`)→ `pricing_schedules` 两次 LEFT JOIN,匹配不到 transaction 的定价记录不会被 join 掉,而是留下来走错误旁路:
   ```sql
   FROM IDENTIFIER(:SOURCE_TABLE) AS fee
   LEFT JOIN transactions AS t ON LOWER(t.public_id) = LOWER(fee.reference_number)
   LEFT JOIN pricing_schedules AS ps ON t.pricing_schedule_id = ps.public_id
   WHERE IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE('JOURNAL_TRANSACTIONS', t.country_iso_code, LOWER(fee.seller_id), CURRENT_TIMESTAMP())
     AND (
       ( t.public_id IS NOT NULL AND ps.public_id IS NOT NULL
         AND t.payment_instrument_sub_kind = 'american_express'
         AND ps.pricing_model IN ('interchange_plus_plus', 'interchange_plus')
         AND t.ledger_kind = 'sale'
         AND t.created_at >= DATEADD(DAY, -7, CURRENT_DATE()) )   -- Flow 1: 合格费用
       OR (t.public_id IS NULL)                                   -- Flow 2: 只为记错误日志
     )
   ```
   这个 `(合格条件) OR (t.public_id IS NULL)` 的双分支 WHERE 是设计精髓:一趟 join 同时喂两条下游——合格的去算费,匹配不到的去记 error。

3. **分类 + 取数用「精确值」而非 rounded 值**,聚合用 `GROUP BY … HAVING SUM(amount)<>0` 抑掉净零费:
   ```sql
   CASE WHEN GET_AGGREGATOR_SE_NUMBER_CATEGORY(fee.PAYEE_MERCHANT_ID)='eu_aggregator_se_numbers'
          THEN 'european_amex_interchange'
        ELSE IFF(fee.fee_amount<>0, 'amex_interchange_flat', 'amex_interchange_discount')
   END AS ledger_sub_kind,
   IFF(fee.fee_amount<>0, fee.fee_amount, fee.discount_rate*10000) AS rate,
   IFF(fee.fee_amount<>0, fee.fee_amount, fee.discount_amount)     AS amount
   ```
   一笔交易的多条定价记录被 `GROUP BY transaction+merchant+ledger_sub_kind` 聚合成一条 fee(这就是 "Aggregated Amex" 的字面来源),`SUM(rate)`/`SUM(amount)`。

4. **insert-only MERGE + 符号翻转 + 内联错误日志**。落地用 `MERGE … WHEN NOT MATCHED THEN INSERT`(费用一经写入不可改,匹配 header 注释「no updated pricing records … all fees are finalized」),`amount` 存 `-1 * SUM(amount)`(费用记为借记),`id = UUID_STRING()`。Step 2 再对同一 join 用 `t.public_id IS NULL` 过滤,把校验失败 `INSERT INTO error_logs`,team 用 `GET_TEAM_FOR_ERROR('BRAINTREE_FEES')` 自动路由——**错误永不阻断 MERGE**。

**为什么是 Sr 级**:它把「可测性(依赖注入)+ 容错(LEFT JOIN 保住坏行)+ 幂等(insert-only MERGE)+ 可观测(自动路由的错误旁路)」四件事塞进一个 proc,还保持可读。初级工程师会写「join → insert」,Sr 会写成「一趟扫描同时产出正确结果和错误清单,且重跑安全」。

**Chi 该学到什么程度**:能默画出这个 proc 的骨架,能解释为什么用 LEFT JOIN 而不是 INNER、为什么 MERGE 只 INSERT、`-1*` 的账务含义、`HAVING SUM<>0` 防的是什么。这是面试里被追问 fee-calc 细节时的底牌。

---

### 标杆 2 —— Proc / UDTF 双胞胎:同一套业务规则的两种 Snowflake 惯用法

**路径**:
- UDTF(fee):`app/src/main/resources/db/functions/pass_through_fees/R__create-udtf-agg-amex-interchange-fee-validation.sql` → `VALIDATE_AGGREGATE_AMEX_INTERCHANGE_FEE_AND_CONSOLIDATE()`
- UDTF(transaction):`app/src/main/resources/db/functions/pass_through_fees/R__create-udtf_amex_transaction_record_validation.sql` → `VALIDATE_AMEX_GRRCN_TRANSACTIONS_AND_CONSOLIDATE()`

**这是全 repo 最有教学价值的对照**:标杆 1 的 proc 是「命令式 + 内联 DML」,而 UDTF 把**完全相同**的校验/聚合规则打包成一个返回 `TABLE` 的**纯函数**(无副作用、无 DML)。学会看这两者的取舍,基本就懂了 Snowflake 里「逻辑放 proc 还是放 UDTF」这个核心决策。

**精华在:UDTF 用一个结果集 `UNION ALL` 出两种形状**——合格行(已聚合、可直接 MERGE)和错误行(每条带 `error_type`/`error_source`/`error_id`),调用方一趟 `SELECT * FROM TABLE(VALIDATE_…())` 就能扫一遍分流:
```sql
-- 校验逻辑纯投影,函数体内没有任何 INSERT/MERGE
IFF(error_description <> '', 'VALIDATION_ERROR', NULL) AS error_type,
IFF(error_description = 'NO VALID TRANSACTION TO MATCH GRRCN PRICING RECORD', amex_id, NULL) AS error_id
...
SELECT * FROM aggregated_valid_records
UNION ALL
SELECT * FROM errors
```
transaction UDTF 还多两个亮点:`WHERE IS_FEATURE_ACTIVE('AGGREGATED_AMEX_SEPARATE_FLOW')=TRUE`(feature-flag 门控进 UDTF 内层,残留数据也进不来)+ 按 byte 位置滤掉 Amex 的 REJ 拒付记录:
```sql
-- REJ indicator at position 365-367 in GRRCN file
AND (s.TRANSACTION_REJECTED_INDICATOR IS NULL OR s.TRANSACTION_REJECTED_INDICATOR <> 'REJ')
```

**为什么是 Sr 级**:把校验逻辑抽成无副作用的 UDTF = 单一事实来源、可独立测试、可组合。Sr 的判断是「校验/一致性逻辑用 UDTF(纯、可测),落地 DML 用 proc(有副作用、事务包裹)」,而不是把所有东西塞进一个巨型 proc。

**Chi 该学到什么程度**:能讲清「同一规则为什么既有 proc 又有 UDTF」——UDTF 是 canonical spec + 可测,proc 是 prod task 实际跑的落地器。面试问「你怎么保证 fee 计算逻辑可测/可验证」,这就是答案。

---

### 标杆 3 —— 结算日的跨语言桥:`SnowflakeBusinessDate` Java UDF + `EffectiveDateFactory` 策略模式 ★staff 级

**路径**:
- Java UDF handler:`app/src/main/java/com/braintree/snowglobe/SnowflakeBusinessDate.java`
- 策略工厂 + 区域实现:`app/src/main/java/com/braintree/snowglobe/effectivedates/`(`EffectiveDateFactory.java` / `AbstractEffectiveDate.java` / `USEffectiveDate.java` / `EUEffectiveDate.java` / `AUEffectiveDate.java`)
- SQL 绑定:`app/src/main/resources/db/functions/_shared/R__0004_create-effective-date-function-for-net-settlement-with-currency.sql`(`GET_FEE_EFFECTIVE_DATE`)、`R__0005_get-effective-date-for-bt-fee.sql`(`GET_BRAINTREE_FEE_EFFECTIVE_DATE`)
- 原型对照:`/Users/czhang17/Code/business_date/lib/business_date.rb`(Ruby gem,同一套 business-day 逻辑)

**这是整个画像里最「往上够」的一块——staff 级**。fee 该在哪一天生效(`effective_date` / `posting_date`),不是 `settlement_date + N` 这么简单:要跳周末、跳银行假日、按国家/币种/pricing model 走不同 SLA。团队没有在 SQL 里手写日历,而是把成熟的 JVM business-day 逻辑(`com.braintree.BusinessDate` / `ICPlusDate`,与 Ruby `business_date` gem 同源)**作为 Snowflake Java UDF 装进数据库**,SQL 端一个 `GET_FEE_EFFECTIVE_DATE(...)` 就调到 JVM:
```sql
CREATE OR REPLACE FUNCTION GET_FEE_EFFECTIVE_DATE(iso3_country_code STRING, settlement_date DATE, ...)
RETURNS DATE LANGUAGE JAVA RUNTIME_VERSION='17'
IMPORTS=('@SNOWGLOBE_JAVA_STAGE/app-${VERSION}-all.jar')
HANDLER='com.braintree.snowglobe.SnowflakeBusinessDate.nextEffectiveFeeDay';
```

**精华在三层:**

1. **策略模式按区域派发**(`EffectiveDateFactory`):`USA → USEffectiveDate(SLA=1)`、`AUS → AUEffectiveDate(net-settlement 才 +1,flat pricing 不 +)`、EU → `EUEffectiveDate`,不识别的国家直接 `throw UnsupportedOperationException`(fail loud)。
2. **EU 的币种资金延迟矩阵**(`EUEffectiveDate.getOffset()`):按 disbursement 币种分 T+1(EUR/GBP)/ T+2(USD 等 18 币)/ T+3(JPY/HKD/SGD/THB),未知币种降级到 USD/T+2 安全兜底(永不早于资金到账);Amex 走 caller 给的 funding date 不加币种 offset。这份矩阵是把真实资金到账规律编码进代码。
3. **overload 收敛**:把历史上 4/5/6/7 参数的一堆 overload,收敛成一个带 `DEFAULT NULL` 的 7 参签名(旧调用点不改照样工作),旧 overload 用 `V20260712120000__drop-old-*` 显式 DROP、repeatable 里留注释墓碑而不删。这是维护大规模 SQL 函数库的正确姿势。

配套还有一处教科书级注释——transaction UDTF 里对 US 的 `payment_date - 1` 修正(抵消 `GET_EFFECTIVE_DATE` 内建的 +1 business day,让所有区域都归到 `currentOrNextBusinessDay(payment_date)`),注释直接引用 incident DTBTDATASC-2906,把一个微妙的时区/SLA bug 的来龙去脉写在代码旁边。

**为什么是 staff 级**:跨语言边界(SQL ↔ JVM)+ 策略模式 + 领域规则(多国结算日历/币种 SLA)+ API 演进治理,四样叠在一起。绝大多数人写不出「在 Snowflake 里跑 JVM 业务日历」这种方案,更别说把 US/EU/AU 差异、币种矩阵、overload 收敛处理得这么干净。

**Chi 该学到什么程度**:这是他的「进阶天花板样板」。至少要能讲清 (a) 为什么用 Java UDF 而不在 SQL 里手写日历(复用久经考验的 business-day 库、避免逻辑分叉);(b) 策略工厂怎么按国家分派;(c) EU 币种矩阵解决什么真实问题。能把这块讲透,就是 staff 级信号。

---

### 标杆 4 —— 事件驱动 task DAG:dark-launch + 精确触发 + fan-in + 弹性算力

**路径**:
- 根任务 + staging 表 + 6 stream:`app/src/main/resources/db/squashed/V20250403142923__create-amex-grrcn-staging-table-and-ingestion-task.sql`
- 6 个子任务:`.../squashed/V20250405090000__create-amex-grrcn-processing-tasks.sql`
- fee-calc 双父任务:`.../tasks/braintree_fees/R__agg-amex-interchange-fee-calculation-task.sql`(及 squashed `V20250515005100__agg_amex_bt_fee_calculation.sql`)
- 出款任务:`.../squashed/V20250314145934__transfer_disbursements_to_arbiter_task.sql`

**这是 Snowflake「event-driven task graph」的范本**,四个决策每个都值得学:

1. **根任务 = 调度 + feature-flag 门控(整条 DAG 的 dark launch 开关)**:
   ```sql
   CREATE OR REPLACE TASK STAGE_AMEX_GRRCN_FILE
     SCHEDULE='30 MINUTE' SUSPEND_TASK_AFTER_NUM_FAILURES=1
   AS EXECUTE IMMEDIATE $$ BEGIN
     IF (IS_FEATURE_ACTIVE('AGGREGATED_AMEX_SEPARATE_FLOW')) THEN
       CALL LOAD_AMEX_GRRCN_FILE_TO_STAGING_TABLE();
     END IF; END; $$;
   ```
   toggle 关 = 根本不拉文件 → 下游因 stream 无数据全部静默停摆。这就是整条新流的 dark launch / kill switch。

2. **子任务 = `AFTER 父` + `WHEN SYSTEM$STREAM_HAS_DATA`,无数据不空跑**:6 个 `PROCESS_AMEX_GRRCN_*_TASK` 各挂自己的 stream,哪个 record type 有新行,哪个才 fire。不烧空 warehouse。

3. **fee-calc = 双父 fan-in + 事务包裹 + 弹性算力**:只有「交易已进 TRANSACTIONS」且「pricing 已解析」两个前置都满足才算费:
   ```sql
   AFTER AMEX_PENDING_TRANSACTIONS_TO_TRANSACTIONS, PROCESS_AMEX_GRRCN_TRANSACTION_PRICING_TASK
   WHEN SYSTEM$STREAM_HAS_DATA('AMEX_TRANSACTION_PRICING_TO_BRAINTREE_FEES_STREAM')
   AS BEGIN
     CALL HANDLE_TASK_TIMEOUT_WITH_WAREHOUSE_UPGRADE();   -- 跑太久自动升 warehouse
     BEGIN TRANSACTION;
       CALL CALCULATE_AGGREGATE_AMEX_INTERCHANGE_FEE();
       CALL LOG_VALIDATION_ERRORS('amex_transaction_pricing');
     COMMIT;
   END;
   ```
   `BEGIN TRANSACTION … COMMIT` 把「算费 + 记错误」包成原子;`HANDLE_TASK_TIMEOUT_WITH_WAREHOUSE_UPGRADE()` 是可复用的弹性算力原语。

4. **fail-fast**:所有任务 `SUSPEND_TASK_AFTER_NUM_FAILURES=1`——坏文件让任务自挂,不反复污染。出款任务 `TRANSFER_DISBURSEMENTS_TO_ARBITER`(`SCHEDULE='5 MINUTE'` + stream-gated + 事务包裹)是这个惯用法的最小样例。

**为什么是 Sr 级**:把 DAG 当成一个可观测、可急停、成本受控的系统来设计,而不是一串 cron。dark-launch、精确触发省算力、fan-in 保证前置、原子事务、fail-fast——这些是生产级编排的标配思维。

**Chi 该学到什么程度**:能在白板上画出这个 DAG 并解释每条边为什么存在;尤其能讲「双父 fan-in 解决什么竞态」「feature-flag 在根任务门控 vs 在 UDTF 内门控的区别」。

---

### 标杆 5 —— 幂等 ingestion:append-only stream + 整行 COPY INTO

**路径**:
- ingestion proc:`app/src/main/resources/db/stored-procedures/pass_through_fees/R__load-amex-grrcn-file-to-staging-table.sql`
- stream + staging 表:同标杆 4 的 `V20250403142923__…`
- stale 重建:`.../squashed/V20250610111308__set-aggregate-amex-system-toggle-active.sql`

**精华在把「文件吃进来」做成幂等 + 可独立重放:**
```sql
grrcn_id := UUID_STRING();                          -- 每批 ingest 一个 lineage id(≈ funding 的 AMEX_SETTLEMENT_ID)
COPY INTO AMEX_GRRCN_STAGING (...)
FROM ( SELECT :grrcn_id, TRIM(LEFT($1,10)) AS RECORD_TYPE, $1 AS RECORD_TEXT,
              METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, CURRENT_TIMESTAMP()
       FROM @FUNDING_S3_STAGE/outbound/aggregated-amex/ (
         PATTERN => '^\\d{4}-\\d{2}-\\d{2}/(amex_opt_blue_settlement_grrcn|amex_settlement_eur_grrcn).*$' ) )
FILE_FORMAT = ( FIELD_DELIMITER = NONE  RECORD_DELIMITER = '\n'  SKIP_BLANK_LINES = TRUE )
ON_ERROR = 'ABORT_STATEMENT'  FORCE = FALSE;
```
- **`FIELD_DELIMITER=NONE`**:整行原封不动进 `RECORD_TEXT`(定宽文件不能按分隔符切),切列留给下游 proc。
- **`PATTERN` 扫所有日期子目录**:躲开经典的时区文件夹边界 bug(文件落在昨天的文件夹但今天在处理)——注释里挂了 Slack 链接记录这个坑。
- **`FORCE=FALSE` + Snowflake load history**:同一文件重跑不重复入库 = 幂等;文件 checksum 变了才当新记录。
- **6 条 `APPEND_ONLY=TRUE` stream**:staging 表只 INSERT 不 update/delete,append-only stream 只捕 INSERT、更轻、语义贴合「不可变事件日志」,且 6 个 record type 各有各的游标可独立消费/重放。
- **运维细节**:上线前 `DROP STREAM … / CREATE STREAM IF NOT EXISTS` 重建全部 stream——stream 会因底表 DDL 变更而 stale 失效,必须重置游标(这正是 Chi 在 snowglobe-tools 里处理 Flyway/stream 失效顺序的同类问题)。

**为什么是 Sr 级**:幂等和 lineage 是金融文件 ingestion 的生死线。用 UUID 打批次、用 load history 去重、用 append-only stream 拿独立重放能力——每一个都是「重跑安全」的具体手段。

**Chi 该学到什么程度**:能解释「为什么这条管线重跑一百次结果不变」的每一层机制(UUID lineage + FORCE=FALSE + append-only stream + insert-only MERGE)。这是面试问「幂等怎么保证」的标准答案。

---

### 标杆 6 —— 平台化 quality-check 框架:动态派发的通用校验 runner

**路径**:
- 通用 runner:`app/src/main/resources/db/stored-procedures/_shared/R__execute_quality_check-procedure.sql` → `EXECUTE_QUALITY_CHECK(...)`
- 幂等短路:`.../_shared/R__check-if-quality-check-already-passed.sql`
- 跨对账一致性 proc(高级 SQL 样例):`app/src/main/resources/db/stored-procedures/transactions/R__populate-quality-check-results.sql`
- feature-flag 底座:`app/src/main/resources/db/functions/_shared/R__0002-create-feature-active.sql`

**这是全 repo 最 sophisticated 的单个 proc**——一个 subject-area 无关的通用校验执行器,所有 quality-check 复用它:
```sql
-- 返回码协议:100=success / 0=error / 200=skipped(已 PASS/WARNING)
CALL CHECK_IF_QUALITY_CHECK_ALREADY_PASSED(...) INTO :already_passed;
IF (already_passed) THEN RETURN 200; END IF;               -- 幂等短路
quality_check_call_sql := 'CALL ' || STORED_PROCEDURE_NAME || '(...)';
EXECUTE IMMEDIATE :quality_check_call_sql;                  -- 动态派发任意校验 proc
SELECT $1 INTO :validation_result FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));  -- 抓上一句的返回
IF (validation_result:status IS NOT NULL)                  -- 归一化两种返回契约
  THEN final_status := UPPER(validation_result:status::STRING);           -- 新格式 {status,details}
  ELSE final_status := IFF(validation_result:result::BOOLEAN,'PASS','FAIL'); -- 旧格式 {result,details}
...
EXCEPTION WHEN OTHER THEN                                   -- 校验自己崩了也写 FAIL 行,不消失
  ... INSERT ... 'FAIL' ...; RETURN 0;
```

**精华在:**
- **`EXECUTE IMMEDIATE` + `RESULT_SCAN(LAST_QUERY_ID())`**:动态调任意校验 proc 并回收其结果——这是 Snowflake 里做「插件式框架」的核心手法。
- **双返回契约归一化**:新老两代 check proc 的返回格式都能吃,平滑演进。
- **`EXCEPTION WHEN OTHER` 仍写 FAIL 行**:一个崩溃的校验会表现为「失败」而不是「凭空消失」——fail-safe。
- **返回码协议(100/0/200)+ 幂等短路**:框架级的清晰契约。

配套的 `POPULATE_QUALITY_CHECK_RESULTS` 是高级对账 SQL 样例:用 `UNION ALL` 把 6 个 subject area(transfer/fee/dispute/tax/rolling-reserve/bank-return)的金额汇到一起,用 `LATERAL FLATTEN(INPUT => PARSE_JSON(linked_transfers))` 展开 JSON 关联转账,再按 `ABS(diff) <= 100` 容差判 PASS/FAIL。feature-flag 底座 `IS_FEATURE_ACTIVE` 用 `COALESCE(..., FALSE)`——未知 flag 一律当关(fail safe)。

**为什么是 Sr 级(平台工程信号)**:这不是一个 feature,是一个所有未来 quality-check 复用的**框架**。造框架、定契约(返回码/返回格式)、保证 fail-safe——这是平台工程师而非 feature 工程师的活儿。(这条线对应 Chi 的 S2 故事:他建框架并铺开 ~8 次,后来还写 ADR 把框架从 subject-area-level block 改成 merchant-level。)

**Chi 该学到什么程度**:能讲清 `EXECUTE IMMEDIATE + RESULT_SCAN` 这套动态派发机制,以及「为什么校验崩了也要留下 FAIL 记录」。这是他证明「平台化思维」的核心工件。

---

### 标杆 7 —— 定宽解析的漂亮原型:`amex_settlement_parser` 的声明式 DSL(迁移源头)

**路径**(`/Users/czhang17/Code/amex_settlement_parser`):
- 分发入口:`lib/amex_settlement_parser/grrcn.rb`
- 记录类:`lib/amex_settlement_parser/grrcn/{transaction_record, transaction_pricing_record, summary_record, chargeback_record, adjustment_record, fees_and_revenues_record, header_record}.rb`
- 费码表:`lib/amex_settlement_parser/grrcn/fee_code_map.rb`
- 隐含小数 formatter:`lib/amex_settlement_parser/formatter/implied_decimals_numeric.rb`

**这是 Chi 迁移的源头,也是「定宽解析该长什么样」的漂亮样板**。它建立在外部 gem `FixedWidthParser` 之上,用**声明式字段 DSL** 把 byte offset 变成可读的字段声明:
```ruby
class TransactionRecord
  include FixedWidthParser
  RECORD_TYPE = "TRANSACTN"
  constant_field     1..10,   :record_type, :value => RECORD_TYPE
  alphanumeric_field 11..25,  :payee_merchant_id
  date_field         39..46,  :payment_date, :format => "%Y%m%d"
  numeric_field      229..244, :transaction_amount        # ← 与 SQL SUBSTRING(...,229,16) 一一对应
  ...
```
```ruby
class TransactionPricingRecord           # 隐含小数:源 5 位 → 目标 4 位
  implied_decimals_numeric_field 219..225, :discount_rate,
    source_implied_decimal_places: 5, target_implied_decimal_places: 4
  def fee_description; FeeCodeMap.description_for(fee_code); end
end
```

**精华在:**
- **单趟线性 dispatch + 父子挂载**:`GRRCN.parse` 逐行读,`line[0..9].strip` 取前 10 字符判 record type,`case` 分发;`TXNPRICING` 记录被挂到「上一条 transaction」的 `.fees` 数组上——在一趟扫描里重建了「交易 → 多条定价」的层级关系。
- **round-trip(parse + generate 同一份 spec)**:同一套字段声明既能 `parse` 文件,又能 `generate` 文件——测试 fixture 直接用生产 spec 生成,不会漂移。`ImpliedDecimalsNumeric` formatter 的 `convert`/`generate` 就是一对逆运算(`10 ** (source - target)`)。
- **`FeeCodeMap`**:100+ 个 Amex 费码 → 语义的查表(`fetch(fee_code, "FEE CODE #{fee_code}")` 未知码优雅降级),这是 Amex 领域知识的沉淀。

- **测试策略双层**:每个 record 一个 spec(内联一条定宽 line 逐字段断言,把 offset 回归精确定位到单字段)+ 一个整文件集成 spec(断言 40 txn / 6 adj / 6 cb 等计数与 `transactions.first.fees.first` 嵌套,并 **parse↔generate round-trip** 验证对称)。
- **容错设计**:未知 record type 无 `else` 静默跳过(fixture 里的 `SUBMISSION`/`TRAILER` 就被有意忽略);chargeback 被有意折进 adjustments(向后兼容老 TILR 格式)——dispatch 时做语义归一化。

**对照价值 + 一个真实的迁移论据**:把 Ruby 的 `numeric_field 229..244`(1-based inclusive range)和 SQL 的 `SUBSTRING(RECORD_TEXT, 229, 16)` 并排看,就懂了 Chi 迁移做的是什么——**把声明式 DSL 的字段字典,逐字段翻译成 stored proc 里的 `SUBSTRING + TRY_CAST`**(见 `R__amex_grrcn_transactions_processor.sql`)。更有意思的是:原型里 `transaction_record.rb` 有一处手抄 offset 的 bug——`:submission_gross_amount` 的声明被硬换行断成了 `:submission_g` + 悬空的 `ross_amount`,字段名实际错了。**这正是「人肉维护 byte offset 表很脆弱」的活教材,也是迁移到 Snowflake(offset 集中在 raw 表列注释里、TRY_CAST 防炸、有 e2e/集成测试兜底)的最好论据之一**。

**Chi 该学到什么程度**:能讲清「原型的声明式 DSL 好在哪(round-trip、可读、父子挂载、容错跳过)」以及「迁移到 SQL 后哪些优点保住了、哪些让给了 Snowflake 的增量/幂等能力」;能把那个 offset 手抄 bug 当成「为什么要迁移」的具体证据。这是讲「迁移」这个 bullet 的技术底料。

---

### 标杆 8 —— 上游 CDC ingestion:`kafka-snowflake-connector` 的流式入湖设计

**路径**(`/Users/czhang17/Code/kafka-snowflake-connector`):
- Protobuf→JSON 转换器基类:`src/main/java/com/braintreepayments/ProtobufConverter.java`
- CDC 配置(最值得学):`docker/connector/cdc/funding.properties`
- 自定义 SMT:`src/main/java/com/braintreepayments/transforms/PartitionAssignTransform.java`

**这是 fee-calc join 所依赖的那些源表(transactions / pricing_schedules)是怎么进 Snowflake 的**——Amex fee 管线的上游。它不是手写 CDC,而是包 Snowflake 官方 Kafka connector + 一层自定义 Protobuf 转换器 + SMT。

**精华在:**
- **Snowpipe Streaming(不是 batch COPY)**:`snowflake.ingestion.method=SNOWPIPE_STREAMING` + `enable.streaming.client.optimization=TRUE`,offset token per channel 给 exactly-once;buffer 三阈值(`buffer.count.records=100000` / `buffer.flush.time=60` / `buffer.size.bytes=5000000`)先到先 flush。
- **`ProtobufConverter` = deep module**:`JsonFormat.printer().preservingProtoFieldNames().includingDefaultValueFields()` 让 proto 字段名→稳定的 snake_case 列、每个字段都在场,配合 `snowflake.enable.schematization=TRUE` 自动建/演进列;解析失败返回 `SchemaAndValue.NULL`(log-and-skip,一条毒消息不炸整个 task)。17+ 个具体转换器每个只 ~15 行。
- **JSONPath CDC 过滤(最有启发的一条)**:在 connector 层用 JSONPath 谓词只放行白名单表、丢弃硬删除——**直接就是 fee 管线要的那几张表**:
  ```
  transforms.filterCdcTables.filter.condition=$[?(
    (@.table == 'gateway_transactions' || @.table == 'gateway_transaction_fees'
     || @.table == 'pricing_fee_records' || ...) && @.kind != 'delete')]
  ```
- **`topic2table.map` 双 topic 打进一张表**:迁移期让 legacy CDC 流和新流落到同一张 Snowflake 表——真实的运维级迁移手法。

**为什么是 Sr 级**:exactly-once、schema 演进、毒消息隔离、迁移期双写——流式入湖的四个硬问题都有干净答案。deep module(`ProtobufConverter`)+ 配置即架构(JSONPath 过滤)是两个可迁移的设计品味。

**Chi 该学到什么程度**:理解层次即可(这是上游,不是 Chi 的 owning 面)。能讲「我 fee-calc join 的 transactions/pricing_schedules 是通过 Snowpipe Streaming + CDC 过滤进 Snowflake 的,exactly-once 由 offset token 保证」——把自己的管线放进更大的数据平台上下文,是 Sr 的视野信号。

---

## 4. 知识点体系(掌握这个领域的完整知识树)

**A. Snowflake 原生编排(核心)**
- Task:`SCHEDULE` vs `AFTER`(root vs child)、`WHEN SYSTEM$STREAM_HAS_DATA` 门闩、多父 fan-in、`SUSPEND_TASK_AFTER_NUM_FAILURES`、`CREATE OR ALTER TASK`、CRON in named timezone、task 内 `BEGIN TRANSACTION`/`EXCEPTION WHEN OTHER`、warehouse 自动升级。
- Stream:标准 vs `APPEND_ONLY`、stream 作为「增量游标 + 触发信号」、多 stream 独立消费同一底表、stream stale 失效与重建、`CHANGE_TRACKING`。
- Stored proc:`IDENTIFIER(:var)` 动态表名、`EXECUTE IMMEDIATE` + `RESULT_SCAN(LAST_QUERY_ID())` 动态派发、`SQLROWCOUNT`、返回码协议、`MERGE … WHEN NOT MATCHED`(insert-only 幂等)。
- UDF/UDTF:SQL UDTF 返回 `TABLE`(纯、可测、可组合)、`UNION ALL` 出多形状结果、Java UDF(`LANGUAGE JAVA` + `IMPORTS` jar + `HANDLER`)把 JVM 逻辑装进 Snowflake、DEFAULT 参数收敛 overload。
- VARIANT/半结构化:`col:path` 取 JSON 字段、`LATERAL FLATTEN(INPUT => PARSE_JSON(...))`、`ARRAY_CONSTRUCT/ARRAY_COMPACT/ARRAY_TO_STRING`(累积错误描述)。

**B. 定宽(fixed-width)文件解析**
- record-type 标签(前 N 字符)分发;byte offset + length 字段字典;1-based inclusive range(Ruby)↔ `SUBSTRING(text,pos,len)`(SQL)对应关系;`TRY_CAST`/`TRY_TO_DATE`/`NULLIF/TRIM` 防炸;隐含小数(sign + 整数 + 隐含 N 位小数,`/10000`→cents、`/100000`→rate);声明式 DSL + round-trip(parse=generate);费码表(FeeCodeMap)。

**C. 幂等 / 重跑安全**
- UUID 批次 lineage(GRRCN_FILE_ID);`COPY … FORCE=FALSE` + load history 去重;append-only stream 独立重放;insert-only MERGE + 内容自然键去重;`HAVING SUM<>0` 抑净零。

**D. Feature flag / 灰度 / 急停**
- `SYSTEM_TOGGLES` + `IS_FEATURE_ACTIVE`(`COALESCE(...,FALSE)` fail-safe);全局 flag vs `IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE` 商户级;门控点选址(root task 入口 vs UDTF 内层);一个 UPDATE 即急停(不发版)。

**E. 结算日 / business-day 逻辑**
- 跳周末 + 观察日假日(`:observed`);T+N business days;国家日历(us_banking/federal_reserve/nyse/ecb_target);区域 SLA(US +1 / AU net-settlement +1 / EU 币种矩阵 T1/T2/T3);flat vs 非 flat pricing、daily vs monthly billing cadence;时区约定(America/Chicago = funding TZ);Java UDF 桥 vs Ruby gem 双实现。

**F. 错误处理 / 可观测性**
- 错误旁路(LEFT JOIN 保住坏行 → error_logs,不阻断主流);`GET_TEAM_FOR_ERROR` 数据驱动的错误归属路由(COMPONENT_METADATA);quality-check 框架(通用 runner + 返回码 + fail-safe FAIL 行);SLA health-check task(时区 CRON + warehouse 升级 + 返回值反映健康);对账一致性(跨 subject area UNION ALL + 容差)。

**G. 上游数据平台(视野)**
- CDC / Snowpipe Streaming;Kafka connector + Protobuf→JSON schematization;exactly-once(offset token);JSONPath 表过滤;迁移期 topic 双写。

**H. 业务量级($138.6B / 21.96M 怎么来)**
- 口径 = 生产 `TRANSACTIONS` / `AMEX_GRRCN_TRANSACTIONS` 里 2025 全年 Amex 记录的 `COUNT` 与 `SUM(transaction_amount)`(Confluence Impact Summary 2750481503)。能讲清这是「经此管线处理的 Amex volume」,以及 Aggregated Amex 的 flat/discount/EU 三类费如何构成。

---

## 5. 学习锚点表

| 环节 / 主题 | 关键工件 | 路径(snowglobe 相对,除非另注) |
|---|---|---|
| ① Ingestion task + 6 stream | `STAGE_AMEX_GRRCN_FILE` + `AMEX_GRRCN_STAGING`(CHANGE_TRACKING)+ 6× APPEND_ONLY stream | `app/src/main/resources/db/squashed/V20250403142923__create-amex-grrcn-staging-table-and-ingestion-task.sql` |
| ① COPY INTO load proc | `LOAD_AMEX_GRRCN_FILE_TO_STAGING_TABLE`(FIELD_DELIMITER=NONE + S3 PATTERN + FORCE=FALSE) | `.../stored-procedures/pass_through_fees/R__load-amex-grrcn-file-to-staging-table.sql` |
| ② 6 parse tasks | `PROCESS_AMEX_GRRCN_*_TASK`(AFTER + WHEN STREAM_HAS_DATA) | `.../squashed/V20250405090000__create-amex-grrcn-processing-tasks.sql` |
| ③ parse proc(定宽切列样例) | `PROCESS_AMEX_GRRCN_TRANSACTIONS`(SUBSTRING + TRY_CAST + 内容键 MERGE) | `.../stored-procedures/pass_through_fees/R__amex_grrcn_transactions_processor.sql` |
| ④ movement UDTF | `VALIDATE_AMEX_GRRCN_TRANSACTIONS_AND_CONSOLIDATE`(join PENDING_TRANSACTIONS、滤 REJ、feature-flag 内门控) | `.../functions/pass_through_fees/R__create-udtf_amex_transaction_record_validation.sql` |
| ④ eventstream 校验 UDTF(VARIANT 样例) | `VALIDATE_AND_CONSOLIDATE_UDTF_FOR_PENDING_AGGREGATED_AMEX_TRANSACTIONS`(processor_settings VARIANT、ARRAY 累积错误、EU flag) | `.../functions/pass_through_fees/R__create-eventstream-validation-and-consolidate-for-pending-aggregated-amex-udtf.sql` |
| ⑤ fee calc proc ★ | `CALCULATE_AGGREGATE_AMEX_INTERCHANGE_FEE_WITH_SOURCE`(IDENTIFIER 注入 + 双分支 WHERE + 聚合 MERGE + error 旁路) | `.../stored-procedures/braintree_fees/R__create-agg-amex-interchange-fee-calculation-with-source-stored-procedure.sql` |
| ⑤ fee 校验 UDTF | `VALIDATE_AGGREGATE_AMEX_INTERCHANGE_FEE_AND_CONSOLIDATE`(UNION ALL valid+errors) | `.../functions/pass_through_fees/R__create-udtf-agg-amex-interchange-fee-validation.sql` |
| ⑤ fee-calc 双父 task | `AGG_AMEX_INTERCHANGE_FEE_CALCULATION_TASK`(dual AFTER + BEGIN TRANSACTION + warehouse 升级) | `.../tasks/braintree_fees/R__agg-amex-interchange-fee-calculation-task.sql`;`.../squashed/V20250515005100__agg_amex_bt_fee_calculation.sql` |
| ⑤ toggle 激活 + stream 重建 | `AGGREGATED_AMEX_SEPARATE_FLOW = TRUE`(DROP/CREATE stale streams) | `.../squashed/V20250610111308__set-aggregate-amex-system-toggle-active.sql` |
| 结算日 Java UDF ★staff | `SnowflakeBusinessDate` + `EffectiveDateFactory`/`US/EU/AUEffectiveDate` | `app/src/main/java/com/braintree/snowglobe/SnowflakeBusinessDate.java`;`.../effectivedates/*.java` |
| 结算日 SQL 绑定 | `GET_FEE_EFFECTIVE_DATE`(7-param DEFAULT,LANGUAGE JAVA)、`GET_BRAINTREE_FEE_EFFECTIVE_DATE` | `.../functions/_shared/R__0004_create-effective-date-function-for-net-settlement-with-currency.sql`;`R__0005_get-effective-date-for-bt-fee.sql` |
| feature flag 底座 | `IS_FEATURE_ACTIVE`(COALESCE fail-safe)、`IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE` | `.../functions/_shared/R__0002-create-feature-active.sql`;`R__create-is-merchant-account-features-active.sql` |
| 错误路由 | `GET_TEAM_FOR_ERROR`(COMPONENT_METADATA 驱动) | `.../functions/_shared/R__01_get-team-for-error-function.sql` |
| quality-check 通用 runner ★ | `EXECUTE_QUALITY_CHECK`(EXECUTE IMMEDIATE + RESULT_SCAN + 返回码 + fail-safe) | `.../stored-procedures/_shared/R__execute_quality_check-procedure.sql` |
| 跨对账一致性 proc | `POPULATE_QUALITY_CHECK_RESULTS`(UNION ALL 6 area + LATERAL FLATTEN + 容差) | `.../stored-procedures/transactions/R__populate-quality-check-results.sql` |
| ⑥ fund transfer task | `TRANSFER_DISBURSEMENTS_TO_ARBITER`(5min + stream-gated + 事务) → `CREATE_ARBITER_DISBURSEMENTS_MESSAGES` | `.../squashed/V20250314145934__transfer_disbursements_to_arbiter_task.sql` |
| ⑦ SLA health-check | `CHECK_FUNDING_TRANSFERS_SLA`(CRON in Australia/Sydney + warehouse 升级 + EXCEPTION) | `.../tasks/transfers/health_checks/R__check-funding-transfers-sla-task.sql` |
| 定宽原型(Ruby)| `AmexSettlementParser::GRRCN` DSL + FeeCodeMap + ImpliedDecimalsNumeric | `/Users/czhang17/Code/amex_settlement_parser/lib/amex_settlement_parser/grrcn.rb` 及 `grrcn/*.rb`、`formatter/implied_decimals_numeric.rb` |
| business-day 原型(Ruby)| `BusinessDate`(effective_date / business_days_from / observed holidays) | `/Users/czhang17/Code/business_date/lib/business_date.rb` |
| 上游 CDC | Snowpipe Streaming + `ProtobufConverter` + JSONPath 表过滤 | `/Users/czhang17/Code/kafka-snowflake-connector/src/main/java/com/braintreepayments/ProtobufConverter.java`;`docker/connector/cdc/funding.properties` |
| e2e / 集成测试 | `AmexGrrcnE2ETest` / `AmexGRRCNIntegrationTest` / `CalculateAggregateAmexInterchangeFeeTest` | `app/src/e2eTest/java/pass_through_fees/`;`app/src/integrationTest/java/pass_through_fees/`;`.../braintree_fees/` |
| 设计文档 | AMEX GRRCN Flow(2233926829)、Aggregated Amex(1112867224)、Impact Summary(2750481503) | Confluence |
| Jira | epic DTBTTFOUND-2074;story 1960/1961/2084/2097/2139;PR #886/#2598/#2820 | Jira / GitHub |

---

## 6. 面试怎么讲(一段话术,把整套讲成 Chi 懂透的东西)

> "我 own 的是 Braintree 处理 American Express 结算的端到端管线——2025 年经它处理了 **21.96M 笔 Amex 交易、$138.6B volume**。Amex 是 closed-loop 网络,每天发一份专有定宽文件 GRRCN,里面混着交易、定价、chargeback、adjustment 五六种记录。我把原本在 Funding 里的一套 Ruby 定宽解析脚本,整套迁到 Snowflake-native 的 task/stream/proc/UDTF 上重建了这条线。
>
> 架构上它是一个事件驱动的 task DAG:一个 30 分钟调度的根任务用 feature flag 门控——这既是灰度开关也是急停,一个 toggle 不发版就能切断整条流;根任务 `COPY INTO` 时用 `FIELD_DELIMITER=NONE` 把整行原样入 staging 表,每批打一个 UUID 做 lineage,`FORCE=FALSE` 靠 load history 去重保证重跑幂等。staging 表上挂 6 条 append-only stream 按 record type 分流,6 个子任务各自 `WHEN SYSTEM$STREAM_HAS_DATA` 才触发,没数据不烧 warehouse。
>
> 费用计算是核心 proc:我用 `IDENTIFIER(:SOURCE_TABLE)` 参数化数据源,让 prod 跑 live stream、test 跑 fixture 走同一段逻辑;join 用 LEFT JOIN 故意保住匹配不到交易的定价记录,WHERE 写成『合格 OR 无交易』双分支,一趟扫描同时产出要落账的费用和要记 error 的坏行——错误进 error_logs 并用 `GET_TEAM_FOR_ERROR` 自动路由到 owning team,永不阻断主流程。费用按交易聚合(这就是 Aggregated Amex),`MERGE` 只 INSERT 因为费用一经 finalize 不可改,金额存负值表借记。fee 的生效日不是简单 T+N——我们把 JVM 的 business-day 逻辑做成 Snowflake Java UDF,按 US/EU/AU 用策略模式分派,EU 还按 disbursement 币种走 T+1/T+2/T+3 矩阵。
>
> 算完的费用进 braintree_fees、过 journal 和 balances,再由一个 5 分钟的 stream-gated 任务推给 Arbiter 出款,全程有 SLA health-check 和一套我参与建的通用 quality-check 框架盯着——那个框架用 `EXECUTE IMMEDIATE + RESULT_SCAN` 动态派发任意校验、归一化返回契约,校验自己崩了也会留下 FAIL 记录而不是消失。
>
> 我对这条线最满意的地方是四条隐藏主线全都立住了:幂等、事件驱动省算力、一键急停、错误旁路自愈——这些让它 18 个月生产零重大事故地扛住了 $138.6B 的量。"

一句收尾定位:**这条线证明的不是「会写 SQL」,而是「能把一个金融级文件管线设计成可测、幂等、可急停、自愈的系统」——这是 Sr 的判断力,不是 feature 的堆砌。**
