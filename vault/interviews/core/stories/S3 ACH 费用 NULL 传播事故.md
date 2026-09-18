---
title: S3 · ACH 费用 NULL 传播事故
aliases:
  - S3
  - ACH NULL 事故
  - CHECK_TRANSACTION_HAS_BRAINTREE_FEES
tags:
  - interview/story
  - stack/sql
  - stack/production
  - stack/observability
answers: [Q3, Q9, Q15]
stacks: [TS08, TS10]
status: verified
---

# S3 · ACH 费用 NULL 传播事故（最难的 bug · on-call · fail loudly）

> [!abstract] 一句话
> 我建的健康检查报警"结算交易没有费用"，我把告警转给自己、几分钟内在线程里给出根因：新路径的 bank-account 交易带着 `NULL` sub-kind 进了交易表，`'BT_' || NULL = NULL` 匹配不到任何品类，费用**静默**不生成；根源是同一个 UDF 的两个重载，共享的 `MERGE` 用了没有 bank-account 分支的那个。写了 postmortem（含 e2e 为何没抓到的四个原因），然后把双重载设计整体移除。

## 1. 事故链

```
告警 CHECK_TRANSACTION_HAS_BRAINTREE_FEES（每日 13:30 CT）
  → 切片：100% us_bank_account · 100% source_type = STANDARD_ACH · ~200 merchants · ~$10M/day
  → 单笔：payment_instrument_sub_kind = NULL
  → 费用计算：product category = 'BT_' || sub_kind → NULL → 无品类 → 不写 discount / settled 费，无异常
  → 回溯 promote procedure：CTE 用 2 参重载算对了，最终 MERGE 用 1 参重载又覆盖成 NULL
  → 1 参重载的 CASE 没有 us_bank_account 分支
```

证据表：对照组（快速到账 ACH，sub_kind 有值）费用正常；按"promote 后天数"分桶覆盖率全为 0% → 排除时序滞后；promoted 行确实到达 fee staging（30/30）→ 是下游映射抑制，不是 stream 绕过。

## 2. 我做的决定

- **不压掉检查**：有人建议把 ACH 加进排除名单；我把数字写下来，判定检查是对的、费用是真丢了。
- **postmortem 写清 e2e 为什么没抓到**：只断言路由不断言费用；fixture 用的是信用卡 payload 所以字段在测试里从不为 NULL；pending 行断言不含 sub_kind；没有任何测试跨"promote → 费用生成"。补了跨越这条链的 e2e。
- **止血之后做结构性修复**（我负责的 hardening）：单一函数 `(PAYMENT_METHOD, PAYMENT_INSTRUMENT_DETAIL DEFAULT NULL)`；**versioned migration `DROP` 掉旧的单参签名**（删掉 `R__` 文件不会删已部署对象）；移除动态 `SUB_KIND_EXPR` 选择，新分支不可能再选到不完整的实现。
- 原则：**an unmappable instrument must fail loudly, not emit nothing**——`NULL` 拼接静默返回 `NULL` 是 SQL 语言属性，修的是接缝上的规则，不是某一处调用。

## 3. 量级与口径

~196 merchants · ~$11.3M/day GMV · ~99,700 笔 settled 费 + ~5,500 笔 discount 费缺失 · 累计 ~1.79M pending 行 · 起始 2026-07-15（standard-ACH 灰度 M2）。

> [!warning] 证据边界
> - 止血 PR 不是我的（stopgap 由队友合入）；我的是根因、postmortem、overload consolidation 与 legacy DROP。说 "I owned the RCA and the hardening; the stopgap landed first."
> - 事故发生在灰度阶段，队友原话"大概不需要 backfill"；**不说** "我 backfill 了"。说 "fix forward with a backfill *if* needed" 作为方法。
> - 起初的 blast-radius 估算属于另一份复盘（[[S10]]），不要混。

## 4. English · 首答（90 s）

> A daily health check I'd built — "every settled transaction has its Braintree fee" — paged the on-call. I forwarded the page to myself and had the root cause in the thread within a few minutes.
>
> The scoping query showed 100 percent of the missing fees were bank-account transactions on the new standard-ACH path — roughly two hundred merchants, on the order of ten million dollars a day of volume. Walking back through the stages: the fee calculation derives the pricing category as `'BT_' || payment_instrument_sub_kind`. For this population sub-kind was `NULL`, and in SQL `NULL` concatenation yields `NULL`, so the category matched nothing and no fee row was produced — silently. Why was it `NULL`? The pending-transactions procedure had two overloads of the same UDF; the shared final `MERGE` re-derived the field with the one-argument overload, which had no bank-account branch, overwriting the correct value the branch-specific logic had already computed.
>
> I wrote the postmortem: the evidence tables — a control group with the field populated had fees, a time series showing zero percent coverage at every age so it wasn't a lag — and the four specific reasons our end-to-end tests missed it, including a fixture that used a card payload for an ACH event. Then I owned the hardening: a stopgap first, then I removed the two-overload design entirely — one function with a defaulted second parameter, a versioned migration to drop the legacy signature so no future branch can pick the incomplete one — plus the e2e test that spans promotion to fee generation.

## 5. English · 追问版

- **What did you decide, versus the team?** → "I made the call that the check was right and must not be suppressed — the fees were genuinely missing. There was pressure to add ACH to the exclusion list. I put the numbers in writing and the check stayed."
- **How did you avoid the same class of bug?** → "The principle I pushed: an unmappable payment instrument must fail loudly, not emit nothing. Silent `NULL` propagation is a SQL-language property, so the fix is a rule at the seam, not a patch at the call site."
- **Backfill?** → "Fix forward with a backfill rather than roll back — in billing the wrong state has already been consumed downstream, so you need a correcting entry, not a reversal."
- **Why didn't tests catch it?** → "Four reasons, all in the postmortem: routing was asserted but never fee generation; the fixture used a card payload so the field was never `NULL` in test; sub-kind wasn't asserted on pending rows; and nothing spanned promotion to fee calculation. I added that e2e."

## 6. 用在哪

- 回答：[[Answers#Q3]] 最难 bug · [[Answers#Q9]] 无授权影响他人 · [[Answers#Q15]] go-to person
- 场景题：夜间管线算错一部分客户（scope by data → walk back → one hypothesis → fix forward）
- 技术栈：[[08-observability-oncall|TS08]]（"数据错了但任务全绿"）· [[10-correctness-idempotency|TS10]]
- 相邻：[[S1]]（上游管线）· [[S8]]（另一次快速 RCA）· [[S10]]（推翻自己数字的复盘）

## 7. 证据锚点

Slack 事故线程 2026-07-29 / 复盘 2026-08-11；Confluence 3029344728（事故复盘）、3052036330（overload consolidation）；PR #3390 / #3490；Jira DTBTTFOUND-3246。
