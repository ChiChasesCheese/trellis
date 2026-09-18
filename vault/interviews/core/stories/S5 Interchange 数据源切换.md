---
title: S5 · Net Settlement 与 interchange 数据源切换
aliases:
  - S5
  - Net Settlement
  - Interchange 数据源切换
tags:
  - interview/story
  - stack/sql
  - stack/distributed-systems
  - stack/cicd
answers: [Q2, Q5, Q8, Q10, Q17, Q21, Q22, Q23]
stacks: [TS03, TS06, TS09, TS10]
status: partial
---

# S5 · Net Settlement 与 interchange 数据源切换（技术决策 + 零回归迁移）

> [!abstract] 一句话
> Net Settlement 是 Braintree 把大商户迁到收单行每日净额直连的多季度项目（gross → net，出款 T+X → T+1，释放约 $450M/月的垫付）。我拥有其中**费用侧最硬的一块**：把信用卡 interchange 的取数源从收单行的 transaction 视图切到更早到达的 settlement 视图——先字段级 discovery，再用生产查询本身做影子核对，然后 toggle 默认关、逐环境放开。

## 1. 背景

pass-through 费用（interchange / scheme / chargeback / auth / non-tran）全部来自收单行的 transaction 视图；该视图有时在出款 cutoff 之后才填好，费用赶不上当天净额。占比最大的信用卡 interchange 需要换到 settlement 视图。

## 2. 决策：静态拆分，不是更聪明的 fallback

- **A**：把已有的"哪个视图有数就用哪个"动态 fallback 做得更聪明——它已经有 sticky 状态、三个 CTE、条件选源，维护负担在涨。
- **B（选）**：按费用类型**静态划分职责**——interchange 固定走 settlement，其余固定留 transaction / auth / non-tran；整体由一个 feature toggle 控制。理由："in a revenue path the source of truth should be a fact, not a runtime decision."

## 3. 验证：同一份 SQL 既做验证又做生产

| 阶段 | 做法 | 结果 |
|---|---|---|
| Discovery | 两侧归一化成同一 shape，`FULL OUTER JOIN` + `EQUAL_NULL` 逐字段落布尔 | 字段一致率 **>99.9%**；**0.07%** 不匹配全是单侧当日才有的记录（时序，非冲突）；两个可解释差异：`FEE_SEQUENCE_CODE`、`ALT_DISPUTE_ID` |
| 切换前 | 把即将上线的生产查询改成 `count(*)` 跑当天全量 | TRANS 13,737,670 vs SETTLE 13,768,430 → **+0.224%**，可接受 |
| 发布 | `INSERT INTO SYSTEM_TOGGLES (…, FALSE)` 默认关 → sandbox/preprod 开 → 监控 → 生产 | **deploy ≠ release** |

> 0.07% 与 0.224% 是**两个不同性质**的数字（字段一致率 vs 记录数差异），不要混用。

## 4. procedure 里的四层手法（TS09 / TS10 的核心素材）

```sql
MERGE INTO FISERV_PASS_THROUGH_FEES_STAGING AS S USING (
  SELECT CONCAT_WS('_', 'INTERCHANGE', SETTLE.INVOICE_NR) AS UNIQUE_IDENTIFIER, …
  FROM …SETTLE_BTFISERV_V1 SETTLE
  JOIN …CLX_TRIGGER_STATUS_V1 T ON SETTLE.RECORD_DT = DATE(T.PROCESS_DATE,'yyyyMMdd')
  WHERE IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE('JOURNAL_TRANSACTIONS', …)
    AND T.SUBJECT_AREA='Settlement' AND T.STATUS='Completed'
    AND SETTLE.PRDT_CD_ORG != '00006'          -- Amex 走自己的管线
) AS X
ON EQUAL_NULL(S.UNIQUE_IDENTIFIER, X.UNIQUE_IDENTIFIER)
   AND S.CREATED_AT > DATEADD(MONTH, -1, :LOOKUP_DATE)   -- 窗口化 ON
WHEN NOT MATCHED THEN INSERT (…);
```

1. **幂等 MERGE**，合成键 = 前缀 + 发票号；任务每小时重跑不重复计费——幂等在数据的唯一性里，不在外部状态机。
2. **窗口化 `ON`**：目标表只增不清理，等值条件会扫全部历史；加一个月窗口让 zone map 剪枝，扫描量恒定。代价：超过一个月才重处理的同一记录会绕开去重——可解释的、写在注释里的风险敞口。
3. **trigger-status JOIN**：上游没校验完这个 JOIN 一行不返回——"上游可信"从文档约定变成硬约束（[[S2]] 的消费侧）。
4. **商户级 feature gate + 网络排除**：迁移开关（task 级）× 商户是否已切新记账（商户级）× 不该出现在这条支路的记录（Amex）——灰度里的多层闸门。

旧 task 反向改造：toggle 开时显式排除 interchange——两个 task 行为互补，同一时刻只有一边产出 interchange，**靠 source filtering 而不是 MERGE 去重防双计**。任务窗口 `CRON 15 6-9 * * * America/Chicago` 是按 settle 视图实际就绪时间 [5:30, 8:15] EST 反推的。

## 5. 量级与口径

Net Settlement：$55B+ 增量 TPV 的前提 · ~$450M/月 float · 2 年+ 的 epic 链（P1 进行中）。切换：13.7M 行 / +0.224% / >99.9% 字段一致。

> [!warning] 证据边界
> - Epic 的 owner of record 不是我；说 "I own the fee side / the interchange track inside the net-settlement program"，**不说** "唯一 owner"。
> - 生产开关在一次 migration 里被设为 **prod 关、preprod 开**；灰度执行细节没有记录。说 "shipped dark, enabled in pre-prod, then production" 与 "deploy and release are two separate steps"，**不说** "merchant by merchant"、"两周"、"零回归"。
> - $55B / $450M 是项目级业务数字，不是我的管线产出。

## 6. English · 首答（90 s）

> Our pass-through fees — interchange, scheme, chargeback — all came from the acquirer's transaction-level view, and that view sometimes wasn't populated until after the daily disbursement cutoff, so fees missed the net-settlement window. I owned switching the biggest category, credit interchange, to the settlement view, which arrives earlier.
>
> Option A was to make the existing "whichever view has data" fallback logic smarter. Option B was a static split by fee type — interchange from settlement, everything else stays — behind a feature toggle. I chose B: the fallback had already grown sticky state and three CTEs, and in a revenue path I want the source of truth to be a fact, not a runtime decision.
>
> Before switching I did a discovery pass — a `FULL OUTER JOIN` with `EQUAL_NULL` field by field, over ninety-nine-point-nine percent parity, and every difference explained — then a pre-cutover run of the **production query itself as `count(*)`** over a day's data, about fourteen million rows, within a fraction of a percent. Validation and production share the same SQL, so there's no "validated one thing, shipped another."
>
> The procedure stacks four techniques: an idempotent `MERGE` on a synthetic key built from the invoice number; a **time-windowed `ON` clause** so the merge only scans the last month of an ever-growing staging table — that keeps the zone-map pruning intact; a `JOIN` on the trigger-status table so we never read a settlement day that hasn't passed quality checks; and a merchant-level feature gate plus an Amex exclusion, because Amex has its own pipeline. The old task was modified to exclude interchange only when the toggle is on, so the two paths are complementary and can never double-count. Shipped dark: merged with the toggle off, enabled in pre-prod, then production — deploy and release are two separate steps.

## 7. English · 追问版

- **Trade-off of the time window?** → "If the same record is reprocessed more than a month later it bypasses dedup — a deliberate, documented risk in exchange for bounded scan cost. The invariant is written next to the clause."
- **Why not dual-write?** → "The two tasks are gated by one toggle in opposite directions — that *is* the mutual exclusion. Dual-write without an explicit exclusion condition is how you double-charge."
- **Reusable?** → "The backfill SQL became the team's CDC table-backfilling template."
- **Postgres side?** → "Pricing schedules live in Postgres (OLTP, system of record for rates, unique constraints, atomic header + N fee rows); Snowflake is where we aggregate across tens of billions of rows. They sync by an application-level idempotent upsert; conflicts surface as `FAILED_PRECONDITION`. Net settlement in Postgres is one flag on the pricing schedule."

## 8. 用在哪

- 回答：[[Answers#Q2]] [[Answers#Q5]] [[Answers#Q8]] [[Answers#Q10]] [[Answers#Q17]] [[Answers#Q21]] [[Answers#Q22]] [[Answers#Q23]]
- 场景题：零停机换 source of truth · 两系统对不上 · 安全发布一次财务计算变更
- 技术栈：[[03-snowflake-warehouse|TS03]] · [[06-cicd-progressive-delivery|TS06]] · [[09-sql-data-modeling|TS09]] · [[10-correctness-idempotency|TS10]]
- 相邻：[[S2]]（握手的生产者）· [[S10]]（同一项目里的复盘）

## 9. 证据锚点

PR #1615（+634）、#1939（toggle prod 关）、#1833（CDC 回填模板）；Confluence 2698298357（discovery）、2747965111（implementation）、2747848324（template）；Jira DTBTTFOUND-2461 / 2640；代码级拆解见本机 `raw/code/03-net-settlement-and-interchange.md`。
