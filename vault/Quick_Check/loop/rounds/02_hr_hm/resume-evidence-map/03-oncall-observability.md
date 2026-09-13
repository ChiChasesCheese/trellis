# 学习画像 03 — 生产可靠性 / On-Call / 可观测性 / 数据质量门禁

> 用途:学习标杆,不是简历审计。Chi 自己的实现当 baseline 自信陈述,再跨 repo 集百家之所长,挖出这套 fee 管线里最精华的可靠性/可观测性实现作为看齐目标。
> 所有标识符(表名/proc/文件/PR)用英文,叙述中文。深挖来源:snowglobe / snowglobe-terraform / kafka-snowflake-connector / PassthroughFee-HealthCheck-Dashboard。

---

## 1. 主题定位 —— 一个 Sr Eng 眼里的 fee 管线生产可靠性全景

Braintree 的 fee 管线是钱的管线:一笔交易进来,要在 Snowflake 上被摄取、promote、算费、对账、出款,任何一环静默出错都直接等于漏算/多算真金白银($138.6B/年 Amex volume 从这条管线过)。所以"生产可靠性"在这里不是加几个告警,而是一个**闭环系统**,由四层构成,缺一层就漏:

```
                     ┌─────────────────────────────────────────────┐
   数据进来 ───────▶ │  1. 数据质量门禁 (data-quality gate)          │  出错就不放行
                     │     config-driven checks + handshake          │  下游只读一个 COMPLETED 信号
                     └───────────────┬─────────────────────────────┘
                                     │ 放行的数据继续跑
                     ┌───────────────▼─────────────────────────────┐
   持续观测 ───────▶ │  2. 可观测性三支柱                            │
                     │     metrics: Datadog 三层 monitor            │  基础设施/管线/业务正确性
                     │     logs:    Sentry (DALM/ingestion 错误)    │  log4j appender → braintree.sentry.io
                     │     traces:  Streamlit 自建 tracing 工具     │  阈值突变曲线 + merchant 下钻
                     └───────────────┬─────────────────────────────┘
                                     │ 告警触发
                     ┌───────────────▼─────────────────────────────┐
   出事定位 ───────▶ │  3. transaction-tracing → RCA                │
                     │     告警 → 受影响集合切片 → 单笔字段级归因    │  PagerDuty → 一笔交易 → SQL 工件
                     │     → 回溯 promote proc → 读 UDF 定义         │
                     └───────────────┬─────────────────────────────┘
                                     │ 找到根因
                     ┌───────────────▼─────────────────────────────┐
   防止复发 ───────▶ │  4. prevent-recurrence                       │
                     │     不只 hotfix,消灭失败模式本身            │  UDF 合并 / ADR / config 补齐
                     └─────────────────────────────────────────────┘
```

关键洞察(Sr 级的区别):**这套系统的每一层都是"声明式 + 通用引擎"而不是硬编码**。质量门禁是 config 表驱动的,告警路由是 metric 自带 metadata 驱动的,tracing 工具的 dashboard 和 prod 验证 SQL 共用一份 SQL 生成逻辑。这种"把策略从机制里抽出来"的设计,是把一堆脚本变成平台的分界线。

---

## 2. Baseline — Chi 已有实现(自信陈述)

Chi 是这条 fee 管线事实上的 on-call go-to person,四层里每一层都有他亲手的实现:

**数据质量门禁**:Chi 造了 Quality-Check & Handshake 框架(PR #1997,1,489 行,DTBTTFOUND-2664),然后自己在几乎每个 fee subject area 铺开约 8 次(#2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237)。这不是一个 feature,是所有未来 quality-check 复用的平台底座:config 表 `QUALITY_CHECK_CONTRACT_CONFIG` 声明"查什么",通用 proc 执行"怎么查",`TRIGGER_STATUS_V1` 发布"能不能读"的握手信号。后来他识别出原框架"某 subject area ~4% 失败就 block 全部 merchant"的粒度缺陷,写了正式 ADR(MADR 3.0.0,含正确性证明 + 否掉 3 个备选方案)把它推向 merchant-level。

**可观测性**:Chi 在团队的 Datadog 平台上运维/扩展 monitor,用 Sentry 查 DALM 层错误,并且**自建了两个 Streamlit-in-Snowflake 监控 app**——`PTF Explorer`(repo `PassthroughFee-HealthCheck-Dashboard`,21 个 commit 全是 Chi)和 `NON_AGG_AMEX_TASK_MONITOR`。这两个是 bullet "building transaction-tracing and observability tooling" 最硬的支撑:让工程师自助查 pass-through fee 异常和 task failure,不用翻原始 Datadog 或手写 SQL。

**RCA go-to(四个真实事故,全部他主导)**:
- **ACH fee-calc 生产事故**(S3):一条 PagerDuty `CHECK_TRANSACTION_HAS_BRAINTREE_FEES`,Chi 自己转发到 #snowglobe 并当场给出完整根因(2026-07-29),精确定位到 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND` 的 1-arg vs 2-arg overload 分叉。~196 merchants / ~$11.3M/day GMV / ~1.05M rows。持续 owning 数周,发起 UDF consolidation(DTBTTFOUND-3246)防复发。Sahar/Dylan 公开致谢。
- **AU Amex refund fees 跨团队 RCA**(S4):PM Liz Lippow 走正式 "Request Help" 表单,Tejesh 点名把问题路由给 Chi。根因:所有 AU merchant 的 `fee_refund_policy='partial'`→ non-agg Amex refund fee 在 AU 从不生成。USA 1,079,627 rows vs AUS 0,跨 157 merchants。催生 DTBTTFOUND-3269。
- **Terraform grant-ownership 7 分钟 RCA**(S8):release 卡住,Chi ~7 分钟定位——`GRANT OWNERSHIP` 被拒因为依赖角色已持 USAGE grant,资源缺 `outbound_privileges`。补齐后确认这是全 repo 唯一缺这个属性的 ownership grant(commit `598750d`,DTBTTFOUND-3198)。
- **DoorDash Amex disbursement 事故**(S9):正式事故频道,指挥 Kiran Patil 点名 Chi 为三个 fix owner 之一,George Fashho 在 SLA 问题上 defer 给 Chi,Chi 给出领域权威判断("T+7 是 US 内部管线 SLA,要等 Amex settle 到我们账户才出款",把"延迟"定性为 upstream 依赖而非内部 bug)。

**告警噪音治理**:Pinless 误报根因修复(31.0M 条 junk 误报,Confluence 3008530291);pinless 漏算重放(为 2 个 merchant 重算 14,434,816 rows 漏掉的 BT fee,走 `RETRY_ERRORS` 而非直接 UPDATE)。

这是一个 Sr on-call engineer 完整的能力面。下面是往哪里看齐把它每一块都做到极致。

---

## 3. ★ 往哪里看齐 —— repo 最精华实现(重点)

跨 repo 挑出 9 个最值得当学习标杆的实现。每个:精华在哪 / 为什么 Sr 级 / 路径 + 锚点 / 学到什么程度。

### 3.1 Datadog 三层告警 + 数据驱动路由 ★可观测性设计的天花板

**路径**:`snowglobe-terraform/modules/datadog/monitors.tf`(687 行,20 个 `datadog_monitor`)

精华不在"有 20 个 monitor",而在**三层分工 + 路由 metadata 由 metric 自己携带**。三层各用不同 metric family、不同 query 形状、不同升级严重度:

- **基础设施层**:`monitor_increasing_task_failures`(L323-360)——`sum(last_4h):sum:snowflake.task.duration.count{...task_state:failed}.rollup(sum,3600) >= 2`,warning=1 / critical=2。`task_state_not_started`(L1-44)有个 Sr 级细节:把每日只跑一次的 ML fee-estimate task 单独排除(`NOT task.name:...`)并给它一个 `last_1d` 窗口的专属 monitor(L54-85),避免一个日频 task 对着共享的 ~25 分钟窗口天天 flap 23 小时。
- **管线层**:`alert_increase_dynamic_table_refresh_lag`(L543-579)——`min(last_10m):avg:snowflake.refresh.dynamic_table.lag{...} > 3540`。两个 Sr 级手法:用 `min(last_10m)` 要求 lag **持续** 10 分钟才报(抗抖动),阈值 3540 秒 = 59 分钟(卡在 1 小时 SLA 之下留 buffer),消息里 `{{ eval "value / 60" }} minutes` 把秒数人性化。
- **业务正确性层**:`bt_fee_gst_entries_missing`(L252-271)——`sum:snowflake.snowglobe.journal_entries.created{...ledger_kind:braintree_fees_gst} < 1`。它报的是**预期业务产出的缺失**(该生成的 journal entry 没生成),这是正确性告警,不是 infra 告警,而且消息直接指向要查的 task(`BRAINTREE_FEES_TO_GST`)。

**全库最漂亮的一个 resource** —— `snowglobe_health_check_failed`(L456-493):完全数据驱动的路由。它 `for_each` 遍历数据库,并按 **health-check 自己发出的 tag** 分组:

```
sum(last_1h):sum:snowflake.health_check.count{health_check.status_code:failed,...}
  by {health_check.name, health_check.on_call_priority,
      health_check.on_call_slack_channel, health_check.on_call_pagerduty_service,
      health_check.on_call_run_book} > 0
```

然后路由从 tag 里取,而不是硬编码:

```
@slack-{{ [health_check.on_call_slack_channel].name }}
%{if var.snowglobe_dimension == "prod"~}
{{#is_exact_match "[health_check.on_call_priority].name" "high"}}
@pagerduty-{{[health_check.on_call_pagerduty_service].name}}
{{/is_exact_match}}
%{endif}
```

**为什么 Sr 级**:加一个新的 health check、改它的告警去哪、调它的优先级——全都在数据侧(health check 发的 metric tag)完成,terraform 一行不用动。这是"config as contract"思想在 IaC 层的体现。PagerDuty 只在 `env==prod AND check 自称 high` 时才响,严重度分层也是数据驱动的。

**学到什么程度**:能自己写出一个三层 monitor 集,并且理解"路由 metadata 应该跟着 metric 走而不是写死在 monitor 里";能解释 `min(last_10m)` 抗抖动、阈值留 SLA buffer、per-task carve-out 抗 flap 这三个手法各自解决什么噪音问题。

### 3.2 Stream-based 告警去重 / exactly-once ★分布式系统正确性

**路径**:proc `snowglobe/app/.../stored-procedures/_shared/R__process-task-metrics-alerts.sql`;DDL `.../db/squashed/V20250820143132__create-task-alert-tracking.sql`;文档 `app/wiki_export/7._Operations_and_Monitoring/7.2_Monitoring_and_Alerting.md`

问题:多个 Datadog agent 并发跑同一个告警扫描,怎么保证同一个 task failure 只发一次告警?精华是**三个机制叠起来**,而不是一把锁:

1. **Snowflake change stream(`task_metrics_stream`)当变更源**——agent 从不轮询基表,只看流里的增量。
2. **15 分钟冷却的 `NOT EXISTS` 反连接**——对 claim 台账 `task_alert_offset` 做反连接,同一个 (task, state) 15 分钟内已被 claim 过就不再报。这一个谓词同时做了跨 agent 去重 **和** 重复告警节流:

```sql
AND NOT EXISTS (
  SELECT 1 FROM task_alert_offset tao
  WHERE tao.task_id = s.task_id AND tao.task_name = s.task_name
    AND tao.database_name = s.database_name
    AND tao.alert_status = s.task_state
    AND tao.processed_at >= DATEADD('minutes', -15, CURRENT_TIMESTAMP()) )
```

3. **claim-then-consume 在单事务里**——赢的 agent 在同一个 `BEGIN…COMMIT` 里把 claim 写进台账 **并** 消费 stream,stream offset 只在 claim 提交时才推进;每次调用发一个 `v_task_run_id = UUID_STRING()`,最后只返回带自己 run_id 的 claim,所以 agent 精确只对它赢下的告警发 Datadog。外加 10k 告警熔断上限 + 完整 `EXCEPTION` handler(写审计表 + 返回哨兵行而不是抛)。

**为什么 Sr 级 + 一个要学的辨析**:文档的时序图把 exactly-once 描述成"第一个 agent 赢,其他撞主键报错"。但真实 proc **不靠主键冲突**——Snowflake 根本不强制主键唯一,而且 PK 里带了 per-call `task_run_id` 和 `agent_id`,两个 agent 插"同一条"告警会产生两行不同 PK 而非冲突。真正的 exactly-once 来自**事务前就物化好的 15 分钟 `NOT EXISTS` 冷却过滤** + claim-and-consume 单事务。要学的正是这个:**在最终一致 / 无强约束的数仓里,幂等靠"读时冷却过滤 + 原子 claim",不能想当然靠数据库约束**。看代码,别信图。

**学到什么程度**:能讲清"为什么 Snowflake 里不能靠 unique 约束做去重",能画出 stream → 冷却过滤 → 单事务 claim-and-consume 这条链,并说明 offset 只随 claim 提交推进为什么保证了 at-least-once 不丢 + 冷却过滤保证了 not-too-often。

### 3.3 Quality-Check config 驱动框架 + handshake ★平台工程范式

**路径**:handshake proc `snowglobe/app/.../stored-procedures/_shared/R__update-trigger-statuses.sql`;通用调度引擎 `.../R__populate-quality-checks.sql`;结果写入 `.../transactions/R__populate-quality-check-results.sql`;config DDL `snowglobe/replication/.../V20251215105109__create-quality-check-contract-config-table.sql`

精华:把**查什么 / 怎么查 / 能不能读**三件事彻底解耦。加一个新质量门禁 = 往 config 表插一行,**不是改代码**。

- **config 即契约**——`QUALITY_CHECK_CONTRACT_CONFIG` 不只声明 which validation,还带 `STORED_PROCEDURE_NAME`(哪个 proc 来跑)和 `PROCEDURE_PARAMETERS VARIANT`(JSON 参数),外加 `VALIDATION_ENABLED` 逐条 kill-switch。调阈值 = 一行 `UPDATE`(实证:`oob-migrations/...update-fiserv-au-settlement-row-count-threshold-to-250000.sql` 就是把 JSON 里 threshold 改成 250000)。甚至 `REQUIRED_COLUMNS_PRESENT` 校验的期望列名/类型/长度都写在 JSON 里(`{"CURRENCY_ISO_CODE": {"type":"STRING","size":3}}`),一个通用 proc 完全被 config 参数化。
- **通用引擎**——`POPULATE_QUALITY_CHECKS(SUBJECT_AREA, CHECK_DATE)` 从 config 读 `WHERE VALIDATION_ENABLED=TRUE`,游标遍历,动态 `CALL EXECUTE_QUALITY_CHECK(...)`。这就是"config 驱动 + 通用 proc 动态执行"的机制本体。
- **handshake 门禁**——`UPDATE_TRIGGER_STATUSES()` 是最精华的一环。从 `TRIGGER_STATUS_V1_STREAM` 拿 IN_PROGRESS 的 (subject_area, record_date),用 `LATERAL` 关联 config 展开成"必须过的校验清单",对 `QUALITY_CHECK_RESULTS_V1` 用 `ROW_NUMBER()=1` 取每个 validation 最新一条,然后:

```sql
-- LEFT JOIN 让"缺失的结果"计入 required 但不计入 pass
COUNT(*) AS required_count,
COALESCE(SUM(CASE WHEN latest_checks.STATUS='PASS' THEN 1 ELSE 0 END),0) AS pass_count
...
IFF(required_count > 0 AND pass_count = required_count, 'COMPLETED', 'IN_PROGRESS') AS STATUS_CALC
-- MERGE 只从 IN_PROGRESS 前进,永不回退
WHEN MATCHED AND TARGET.STATUS = 'IN_PROGRESS' THEN UPDATE SET STATUS = SOURCE.STATUS_CALC
```

那个 `LEFT JOIN` 是灵魂:缺结果的校验 `required_count` 照数、`pass_count` 不数,门禁就一直卡在 IN_PROGRESS,直到每个必须校验都有一条最新 PASS。下游任何 job 只需读一个 `TRIGGER_STATUS_V1.STATUS='COMPLETED'`,完全不必知道背后有哪些 check。

**为什么 Sr 级**:这是"策略 vs 机制"分离的教科书。config 表是契约,proc 是引擎,`TRIGGER_STATUS_V1` 是发布出去的握手面。`LATEST-result-wins` 让重跑幂等(后来的 PASS 盖掉早先的 FAIL),门禁是纯计数比较(`pass_count = required_count`)——"全过了"是算出来的,永远不用人肉维护。

**学到什么程度**:能从零画出 config表→通用proc→结果表→handshake 状态表 这四件套,并解释为什么"下游只读一个 COMPLETED 信号"是关键的解耦;能说清 `LEFT JOIN` + `ROW_NUMBER()=1` 分别负责"缺失算失败"和"重跑幂等"。

### 3.4 merchant-level quality check ADR(dense relational rows)★架构决策工件

**路径**:`snowglobe/branch_files/DTBTTFOUND-2749-.../discovery/DTBTTFOUND-2749-option-d-dense-relational-rows.md`(及同目录 adr-writing-guide);Confluence ADR 2894288991,DTBTTFOUND-2749

精华:识别出 3.3 那个框架的**粒度缺陷**——门禁 key 只到 `(SUBJECT_AREA, RECORD_DATE)`,`IFF(pass_count=required_count,...)` 是整个 subject_area 一刀切,某域 4% 校验失败就 block 全部 merchant。ADR 用 MADR 3.0.0 模板,含正确性证明 + 否掉 3 个备选方案,推向 merchant-level(复用 dense relational rows;结果表 `QUALITY_CHECK_RESULTS_V1` 已经带 `MERCHANT_ID`/`MERCHANT_ACCOUNT_UNIQUE_IDENTIFIER`,数据模型已为这次扩展预埋)。

**为什么 Sr 级**:这是"造完平台后回头审视自己平台的爆炸半径"的判断。不是等出事,是主动把"一个坏 merchant 拖垮全批"这个设计缺陷用正式 ADR 提出来改。看这份 ADR 学的是**决策文档怎么写**:选项对比、正确性证明、为什么否掉备选,而不是"我觉得应该这样"。

**学到什么程度**:读完能复述这个 ADR 的决策结构(问题→选项 A/B/C/D→为什么选 D),并能把"subject-area 粒度 vs merchant 粒度"的 blast radius 差异讲清楚。

### 3.5 ACH NULL sub_kind RCA —— UDF overload 静默 NULL ★transaction-tracing 教科书

**路径**:两个 overload `snowglobe/app/.../functions/_shared/R__0001_create-udf-...-sub-kind.sql`(2-arg,有 `us_bank_account` 分支)vs `R__0001-udf-...-sub-kind.sql`(1-arg,缺该分支);promote proc `.../stored-procedures/transactions/R__create-eventstream-to-pending-transactions-with-source-stored-procedure.sql`;health check `.../braintree_fees/health_checks/R__check_transaction_has_relative_braintree_fees.sql`;修复 worktree `.claude/worktrees/DTBTTFOUND-3246-ach-sub-kind-fix`

精华 = **一个由 SQL 函数重载解析产生的静默 NULL**,没有任何报错、异常、或明显写错的行。同名 UDF 两个 overload 都能编译、都能跑;对所有卡支付两者返回相同,所以差异在全部卡测试里隐形;只有 ACH(`us_bank_account`)命中 1-arg 版缺失的分支,CASE 无 ELSE 落空 → 返回 NULL。NULL 再静默传播:`'BT_' || NULL = NULL` → 匹配不到任何 fee category → 不生成费用,**全程不抛异常**,只表现为费用行"缺席",几天后被 health check 抓到。

最狠的一个细节(Sr 级 tracing 才能挖到):**同一条语句先算对再扔掉**。promote proc 的 `VALIDATED_CTE` 里 STANDARD_ACH 分支(L255)用**正确的 2-arg** overload 算出了 `'us_bank_account'`;但真正落库的那个 `MERGE`(L418)**用 1-arg overload 重算**同一列,把好值覆盖成 NULL。甚至同一个 MERGE 里,settlement account 查找读的是 CTE 的好值、持久化的列写的是坏值。定位这个必须顺着值走:event → CTE → MERGE 列表,光读 UDF 定义看不出来。

而费率映射本身其实**处理了** `us_bank_account`(`R__create-discount-fee-calculation...` L84 明确 `WHEN LOWER(sub_kind)='us_bank_account' THEN 'BT_US_BANK_ACCT'`)——它本来会工作,只是永远收不到值,因为 promote proc 已经把它 NULL 掉了。

**prevent-recurrence(修复的精华)**:根因不是"少了个分支",而是"存在两个会漂移的 overload——给一个加分支忘了给另一个,就静默 NULL"。修复把两个 overload 塌成**单一实现 + 可选第二参数**:

```sql
CREATE OR REPLACE FUNCTION GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND(
  PAYMENT_METHOD VARIANT, PAYMENT_INSTRUMENT_DETAIL VARIANT DEFAULT NULL )
```

`DEFAULT NULL` 让所有旧调用点(L418/426 的 1-arg、L183/255/328 的 2-arg)全部解析到**同一个含 us_bank_account 分支的 body**,重载歧义被设计掉:只有一个函数,没有任何调用点能再静默选到过期变体。

**为什么 Sr 级**:junior 会把 1-arg 版补上分支就收工;Sr 认出"两个可漂移的重载"本身才是失败模式,消灭 drift surface 而不是补一个洞。

**学到什么程度**:能完整复述这条 tracing 链(见第 4 节),并且能一眼看出"同名多重载 + 静默 NULL 传播"这个反模式,知道正解是合并成 `DEFAULT NULL` 单实现。

### 3.6 Sentry 接法 —— log4j appender + 环境化 DSN ★错误追踪集成

**路径**:`kafka-snowflake-connector/kubernetes/config.yaml.erb`(DSN)、`docker/generate-configs.sh`(启动时物化 `sentry.properties`)、`docker/log4j.properties`(appender);runbook `snowglobe/docs/runbooks/debugging_dalm.md`

精华是**摄取层(DALM / Kafka→Snowflake connector)怎么把 JVM 错误接进 Sentry**,一条干净的生产接法:

- DSN 按环境分(QA/prod 两个,都在 `braintree.sentry.io` org `o31106`,project `snowglobe` = `4507936114933760`),写在 k8s ConfigMap 模板里:

```erb
sentry_dsn = "https://...@o31106.ingest.sentry.io/2128608"   # prod override in if production_snowflake_account?
SENTRY_DSN: "<%= sentry_dsn %>"
SENTRY_ENVIRONMENT: "<%= environment %>"
```

- 容器启动脚本把 env 物化成 `sentry.properties`,并绑定应用包名做 stacktrace 归属:

```bash
echo "dsn=${SENTRY_DSN}" >> /sentry.properties
echo "stacktrace.app.packages=com.braintreepayments" >> /sentry.properties
```

- 然后 Sentry 挂成 log4j 根 appender:`log4j.rootLogger=INFO, stdout, sentry`。

**on-call 使用面**:runbook 明确写"若连续 3 次运行仍未恢复,Review Snowglobe Sentry for error patterns",并给出 project URL;pricing 侧 `BT_FEES_CALCULATED_FOR_EBB` 每日 14:00 UTC 检查会**同时发 PagerDuty 和 Sentry** 给 pricing team。

**为什么 Sr 级 / 学到什么程度**:这是可观测性三支柱里 **logs/errors** 支柱的标准落地——DSN 环境化注入(不硬编码)、log4j appender 零侵入接入、stacktrace 绑包名。学到能自己描述"一个 JVM 服务怎么把错误接进 Sentry,DSN 怎么按环境注入,on-call 怎么用 Sentry 的 error pattern 聚合定位反复出错"。fee-calc 侧 Chi 走的是 Streamlit + Datadog custom metric,Sentry 是 DALM/ingestion 层的 error tracking——两者分工要讲清。

### 3.7 Streamlit PTF Explorer —— 一次聚合查询 + 全客户端过滤 ★自建 tracing 工具的架构范式

**路径**:`PassthroughFee-HealthCheck-Dashboard/ptf_explorer.py`(92KB,21 commit 全 Chi)

精华是一个可观测性工具该有的架构:**一次聚合 query → 几千行小 frame → 之后所有交互全在客户端 pandas 做,零 warehouse 往返**。

1. **一次聚合、只取汇总**——`_build_sql(start,end,fee_days)`(L499)构一个大 CTE(`TARGET_TXN`→`FEE_ROLLUP`→`SCORED`→`GROUP BY 1..13`),返回的是按 13 个维度预聚合的组行 + `COUNT(*) AS txn_count`,不是原始交易。入口 `load_data_from_sf` `@st.cache_data(ttl=1800)` 缓存,docstring 直接写 "~1500-row DataFrame"。
2. **两层缓存**——`@st.cache_resource` 缓 Snowflake session、`@st.cache_data(ttl=1800)` 缓 query 结果;cache key 只有 (date-window, fee-window),改任何 filter 都不重查。
3. **零往返过滤**——`apply_filters` 对缓存 frame 建布尔 mask 返回子集,注释直书 "Client-side filtering (zero Snowflake calls)"。改 filter = 对 ~1.5K 行重跑 pandas,瞬时且护住 warehouse。
4. **T+0..T+60 阈值突变曲线**——`compute_curve`(L751)向量化 numpy 遍历 lag 桶,按 `txn_count` 加权算每个窗口的 pass-rate,`df_c["delta"]=pass_rate.diff()` 给出"哪天开始崩"的逐日突变。`strict` vs 放松 rule 处理 AUS/EU 的 scheme-PTF 豁免。
5. **★ Prod 验证 SQL 生成器**——最精华的一招:dashboard 用**同一个 `_build_sql`** 从当前 filter 重新生成可直接 prod 跑的 SQL,给 copy/download:

```python
sql_out = _build_sql(txn_start, txn_end, fee_days)   # 和取数用的是同一个函数
st.download_button("⬇ Download SQL", data=str(sql_out), ...)
```

因为数据加载和验证 SQL **共用一份 source of truth**,dashboard 上看到的和你能独立在 prod 跑来验证的,是可证明同一条 query——**dashboard 逻辑和验证逻辑零漂移**。

**为什么 Sr 级 / 学到什么程度**:大多数人写监控 dashboard 是"每个 filter 一次 query 打爆 warehouse";Chi 这套是"把聚合推进一次 round-trip,拉回小 frame,交互全客户端"。学到能自己按这个范式搭工具,并且理解"dashboard 和验证 SQL 共用生成器 = 消除展示与现实的漂移"这个 craft 点。还有一个 dual-mode 细节(SiS/local `_IS_SIS`,本地跑 parquet 快照免 warehouse)值得抄。

### 3.8 Terraform grant-ownership `outbound_privileges` 修复 ★基建层 7 分钟 RCA

**路径**:`snowglobe-terraform/modules/pricing/machine_learning/main.tf`(`snowflake_grant_ownership` 资源 L183/185、L192/194 带 `outbound_privileges = "REVOKE"`);commit `598750d`,DTBTTFOUND-3198

精华:release 卡住,7 分钟定位——`GRANT OWNERSHIP` on 数据库被 Snowflake 拒,因为目标角色已持依赖的 `USAGE` grant,而 `snowflake_grant_ownership` 资源缺 `outbound_privileges` → Snowflake 不肯连带处理已有依赖 grant。修复是加 `outbound_privileges = "REVOKE"`,并**确认这是全 repo 唯一缺这个属性的 ownership grant**,一次补齐。

**为什么 Sr 级 / 学到什么程度**:这是 3.5 那套 tracing 思路在 IaC 层的快速版——报错信息 → 定位依赖 grant → 找到缺失属性 → 确认爆炸半径(是不是还有别处也缺)。学到 Snowflake ownership grant 的 `outbound_privileges` 语义(有依赖 grant 时必须声明连带 REVOKE),以及"修一个之前先 grep 全 repo 看还有没有同类"的习惯。(注:module 现已从 `fee_anomalies` 更名为 `machine_learning`,以当前路径为准。)

### 3.9 Pinless 漏算重放 —— `RETRY_ERRORS` 而非直接 UPDATE ★补数据的正确姿势

**路径**:`snowglobe/app/.../oob-migrations/reprocess-pinless-bt-fees-that-were-missed-4-29-5-12.sql`;Confluence 3008530291

精华:为 2 个 merchant(共 14,434,816 rows)重算漏掉的 pinless BT fee。脚本先建备份表 `ERROR_LOGS_REPROCESS_BACKUP_PINLESS_BT_FEES_5_28_2026`,再 `CALL RETRY_ERRORS('braintree_fees_staging')` 重放,并**明确注释:不要直接 UPDATE `should_retry`,那样不 work,必须走 `RETRY_ERRORS`**——踩过坑并把知识留在脚本里。

**为什么 Sr 级 / 学到什么程度**:补生产数据最容易犯的错就是直接改状态列绕过重试机制。学到"补数据先备份 + 走既有重放通道 + 把踩过的坑写进脚本注释"这套安全补数据的肌肉记忆。

---

## 4. 知识点体系

**(a) data-quality / handshake 门禁模式**。核心是三层解耦:声明式 config(查什么)/ 通用 proc(怎么查)/ 发布式状态(能不能读)。下游只 gate 一个 `COMPLETED` 信号,不碰底层 check。幂等靠 latest-result-wins(`ROW_NUMBER()=1`),"缺失=失败"靠 `LEFT JOIN` 让 required 计数、pass 不计数,门禁纯计数比较。粒度是要提前想的架构决策(subject-area 一刀切 vs merchant-level,blast radius 差 3.4)。

**(b) 可观测性三支柱在这套栈里的落地**:
- **metrics → Datadog**:三层(基础设施 task/kafka/replication、管线 lag/freshness/error-log、业务正确性 fee-entries-missing/health-check)。手法:抗抖动窗口(`min(last_10m)`)、SLA buffer(3540<3600)、per-task carve-out 抗 flap、路由 metadata 由 metric tag 携带。
- **logs/errors → Sentry**:DALM/ingestion(Kafka connector)层,log4j appender + 环境化 DSN + stacktrace 绑包名;on-call 用 error pattern 聚合看反复出错。
- **traces → Streamlit 自建工具**:PTF Explorer 把 tracing 沉淀成工具——阈值突变曲线定位"哪天崩" → merchant 下钻 → raw rollup 看样例 → 生成 prod 验证 SQL。一次聚合 + 客户端过滤 + 单一 SQL source of truth。

**(c) Datadog / Sentry / Streamlit 分工**:Datadog = 主动 push 的指标告警(task/lag/business-correctness,连 PagerDuty);Sentry = 摄取层被动捕获的 JVM error/stacktrace(pattern 聚合);Streamlit = on-call 主动查的自助 tracing/下钻(把"翻 Datadog + 手写 SQL"变成点几下)。三者覆盖 push 告警 / 被动错误 / 主动排查三个场景。

**(d) RCA 方法论 —— 从告警定位到 SQL 工件根因**。通用链路(以 ACH 为例):

```
PagerDuty: CHECK_TRANSACTION_HAS_BRAINTREE_FEES 告警
   │  (health check: transaction 有 journal entry 但 braintree_fees 里没对应 fee;
   │   见 R__check_transaction_has_relative_braintree_fees.sql 的 MISSING LEFT JOIN + RAISE)
   ▼
锁定受影响集合:196 merchants / us_bank_account 98.9% / 100% STANDARD_ACH
   │  用 error_logs + transactions 按 merchant/sub_kind 切片
   ▼
看单笔 payment_instrument_sub_kind = NULL
   │  fee-calc 品类映射 'BT_' || NULL = NULL → 无品类 → 不生成 fee(静默,无异常)
   ▼
回溯 promote 链路(eventstream → pending transactions proc)
   │  关键:CTE(L255)用 2-arg 算对了,MERGE(L418)用 1-arg 又覆盖成 NULL —— 顺着值走才看得到
   ▼
读两个 UDF overload → 1-arg 版 CASE 缺 us_bank_account 分支 → NULL
   │  根因:overload 选错 + 1-arg 覆盖不全
   ▼
prevent-recurrence: 合并成单一 DEFAULT NULL 实现 (DTBTTFOUND-3246),消灭 drift surface
```

方法论要点:**告警 → 受影响集合切片 → 单笔字段级归因 → 回溯 promote proc → 读 UDF 定义 → 找到 overload 分叉 → 消灭失败模式(不只补洞)**。同一套思路在基建层是 7 分钟版(3.8):报错 → 定位依赖 grant → 缺失属性 → 确认爆炸半径。RCA 的 Sr 级标志是最后一步——**区分"修这个 bug"和"消灭这类 bug 能存在的条件"**(补分支 vs 合并重载;补一个 grant vs 确认全 repo 唯一)。

---

## 5. 学习锚点表

| 学习标杆 | 路径 / 锚点 | 精华一句话 |
|---|---|---|
| Datadog 三层 + 数据驱动路由 | `snowglobe-terraform/modules/datadog/monitors.tf`(`snowglobe_health_check_failed` L456-493) | 路由 metadata 跟着 metric tag 走,不写死在 monitor |
| Stream 告警 exactly-once | `snowglobe/app/.../_shared/R__process-task-metrics-alerts.sql` + DDL `V20250820143132__create-task-alert-tracking.sql` | 幂等靠 15min 冷却 `NOT EXISTS` + 单事务 claim-and-consume,不靠 DB 约束 |
| Quality-Check config 框架 | handshake `R__update-trigger-statuses.sql`、引擎 `R__populate-quality-checks.sql`、config DDL `V20251215105109__...config-table.sql` | config=契约 / proc=引擎 / TRIGGER_STATUS_V1=握手;加门禁=插一行 |
| merchant-level ADR | `snowglobe/branch_files/DTBTTFOUND-2749-.../discovery/*-dense-relational-rows.md`;Confluence 2894288991 | 造完平台回头审爆炸半径,正式 ADR 否掉 3 方案 |
| ACH UDF overload 静默 NULL RCA | 两 overload `R__0001[_/-]...sub-kind.sql`;promote proc L255(2-arg)vs L418(1-arg);修复 worktree DTBTTFOUND-3246 | 同名可漂移重载 → 静默 NULL;修复=合并成 `DEFAULT NULL` 单实现 |
| health check tripwire | `snowglobe/app/.../braintree_fees/health_checks/R__check_transaction_has_relative_braintree_fees.sql` | EXPECTED vs ACTUAL 的 MISSING LEFT JOIN,BAD_COUNT>0 则 RAISE 分页 |
| Sentry log4j 接法 | `kafka-snowflake-connector/kubernetes/config.yaml.erb` + `docker/{generate-configs.sh,log4j.properties}`;runbook `debugging_dalm.md` | DSN 环境化注入 + log4j appender + stacktrace 绑包名 |
| Streamlit PTF Explorer | `PassthroughFee-HealthCheck-Dashboard/ptf_explorer.py`(`_build_sql` L499、`load_data_from_sf` L633、`compute_curve` L751) | 一次聚合→客户端过滤;dashboard 与验证 SQL 共用生成器,零漂移 |
| Terraform grant-ownership | `snowglobe-terraform/modules/pricing/machine_learning/main.tf` L183-194;commit `598750d` DTBTTFOUND-3198 | `outbound_privileges="REVOKE"` 处理依赖 grant;修一个先 grep 全 repo |
| Pinless 安全补数据 | `snowglobe/app/.../oob-migrations/reprocess-pinless-bt-fees-...sql` | 先备份 + 走 `RETRY_ERRORS` 重放通道,别直接 UPDATE should_retry |

---

## 6. 面试怎么讲(go-to person 叙事 + 量化)

**一句话定位**:"我是 Braintree fee 管线事实上的 on-call go-to person——PagerDuty 转给我、PM 走正式表单点名路由给我、事故指挥点名我当 fix owner。这条管线一年过 $138.6B Amex volume,任何静默漏算都是真金白银,所以我把可靠性当系统建:数据质量门禁 + 三支柱可观测性 + tracing-to-RCA + 消灭失败模式的闭环。"

**四个 RCA 讲成 go-to 叙事**(每个都是"被点名 + 深度定位 + 量化 + 防复发"):

1. **ACH 生产事故(最强的深度 debug)**:"一条 PagerDuty,我自己转发到频道并当场给根因。表面是 ~196 个 merchant、~$11.3M/day 的 ACH 交易没生成 Braintree fee,全程不报错。我顺着一笔交易追:sub_kind=NULL → `'BT_'||NULL` 匹配不到品类 → 回溯 promote proc,发现同一条 MERGE 里 CTE 先用正确的 2-arg UDF 算出了值、落库的 MERGE 又用一个缺 `us_bank_account` 分支的 1-arg 重载覆盖成 NULL。根因不是少个分支,是存在两个会漂移的同名重载。我发起 consolidation 合并成单一 `DEFAULT NULL` 实现,让重载歧义在设计上不可能再发生。持续 owning 了数周。"

2. **AU Amex refund(跨团队 + go-to 直证)**:"PM 走正式 Request Help 表单,团队直接把问题点名路由给我,50+ 回复的 thread。我定位到所有 AU merchant 的 `fee_refund_policy` 都是 `partial` 从不是 `full`,导致 non-agg Amex refund fee 在 AU 从不生成——USA 1,079,627 行 vs AUS 0 行,跨 157 个 merchant。催生了修复 ticket。"

3. **DoorDash 事故(领域权威)**:"正式事故频道,指挥点名我当三个 fix owner 之一,另一位工程师在 SLA 问题上 defer 给我。我给出定性判断:T+7 是 US 内部管线 SLA,得等 Amex 把钱 settle 到我们账户才出款——把'延迟'从'内部 bug'重新定性成 upstream settlement 依赖,止住了误判方向。"

4. **Terraform 7 分钟 RCA(压力下快速定位)**:"release 卡住,我 7 分钟定位:ownership grant 被拒因为目标角色已持依赖的 USAGE grant,资源缺 `outbound_privileges`。补上后我 grep 全 repo 确认这是唯一一处缺失,一次补齐,release 当天部署。"

**平台工程信号(不止救火,还建门禁)**:"我造了 config 驱动的 Quality-Check + handshake 框架并铺到约 8 个 fee subject area——加一个新质量门禁是往 config 表插一行,不是改代码;下游只读一个 COMPLETED 握手信号。后来我识别出它 subject-area 一刀切、某域 4% 失败就 block 全部 merchant 的粒度缺陷,写了正式 ADR 推向 merchant-level。"

**自建可观测性工具(building tooling 的实证)**:"我自建了两个 Streamlit-in-Snowflake 监控 app 让团队自助排查——一次聚合查询拉回几千行,之后所有筛选/下钻全在客户端做,零 warehouse 往返;dashboard 和 prod 验证 SQL 共用同一个生成器,保证你在页面看到的和能独立去 prod 验证的是同一条 query。Datadog(指标告警)、Sentry(DALM 层错误追踪)、我的 Streamlit(主动下钻)三者分工覆盖了 push 告警 / 被动错误 / 主动排查。"

**量化弹药(被追问时抛)**:$138.6B/年 volume;ACH 196 merchants / $11.3M day / 1.05M rows;AU 1.08M vs 0 / 157 merchants;pinless 重放 14.43M rows;质量框架复用 ~8 次 / ADR 否掉 3 方案;Terraform 7 分钟。
