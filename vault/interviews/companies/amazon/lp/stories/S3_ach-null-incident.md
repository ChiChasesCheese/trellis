# S3 · ACH 费用 NULL 传播事故（最难的 bug · fail loudly）

> 来源：`core/stories/S3 ACH 费用 NULL 传播事故.md`（status: verified）。
> 主 LP：**Dive Deep · Ownership · Insist on the Highest Standards · Have Backbone**；副：Customer Obsession · Bias for Action · Earn Trust · Deliver Results。
> 一句话：*"A health check I'd built paged us because fees were silently missing; I found a NULL-propagation bug in a function overload in minutes and then removed the whole class of bug."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| ~196 商户 · ~$11.3M/天 GMV | 受影响范围（口播 "roughly two hundred merchants, on the order of ten million dollars a day"） |
| ~99,700 笔 settled 费 + ~5,500 笔 discount 费缺失；累计 ~1.79M pending 行 | 缺失规模 |
| 100% us_bank_account · 100% STANDARD_ACH | 切片结果 |
| 起始 2026-07-15（standard-ACH 灰度 M2） | 事故在灰度阶段 |
| 告警每日 13:30 CT | 检查调度 |
| 根因定位："几分钟内" | 口播只说 a few minutes |
| e2e 没抓到的 4 个原因 | postmortem |

## 2. 60–90 秒口播版（≈ 200 词）

> A daily health check I'd built — "every settled transaction has its Braintree fee" — paged the on-call. I forwarded the page to myself and had the root cause in the thread within a few minutes.
>
> Scoping showed that a hundred percent of the missing fees were bank-account transactions on the new standard-ACH path: about two hundred merchants, roughly ten million dollars a day. The fee calculation builds the pricing category as `'BT_' || payment_instrument_sub_kind`. For these transactions the sub-kind was `NULL`, and in SQL, concatenating `NULL` gives `NULL`, so no category matched and no fee was written — silently, no exception. The reason: one function had two overloads, and the shared final `MERGE` called the one-argument version, which had no bank-account branch, and overwrote the correct value.
>
> There was pressure to add ACH to the check's exclusion list. I put the numbers in writing: the check was right and the fees were really missing. A teammate landed the stopgap first. I owned the root cause, the postmortem, and the hardening: one function with a defaulted parameter, a versioned migration that drops the old signature, and an end-to-end test that spans promotion through fee generation. The rule I pushed: an unmappable instrument must fail loudly, not emit nothing.

## 3. 2 分钟版（≈ 330 词）

> **Trigger.** At 1:30 pm Central the check "every settled transaction has its Braintree fee" paged. I wasn't the assignee; I forwarded it to myself.
>
> **Scoping.** I sliced the missing fees: 100 percent were `us_bank_account`, 100 percent standard ACH, around two hundred merchants and ten million dollars a day. Then one transaction: `payment_instrument_sub_kind` was `NULL`. The fee code derives the category as `'BT_'` concatenated with the sub-kind, and `NULL` concatenation yields `NULL` in SQL. No category, no discount fee, no settled fee, and no error. I ruled out a timing lag with a time series — zero percent coverage at every age bucket — and ruled out a stream bypass because the promoted rows did reach fee staging, 30 of 30. A control group — fast ACH, where the field was populated — had fees.
>
> **Root cause.** Walking back through the promote procedure: a CTE used the two-argument overload and got it right, then the final `MERGE` used the one-argument overload, whose `CASE` had no bank-account branch, and overwrote the field with `NULL`.
>
> **Decisions.** First, don't suppress the check — someone suggested excluding ACH. I wrote the numbers down and kept it. Second, the postmortem listed four reasons our end-to-end tests missed it: they asserted routing but not fee generation; the fixture used a card payload so the field was never `NULL` in test; sub-kind wasn't asserted on pending rows; nothing spanned promotion to fee calculation. Third, after the stopgap a teammate landed, I did the structural fix: one function with a defaulted second parameter, a versioned migration to `DROP` the old signature — because deleting the file doesn't remove the deployed object — and I removed the dynamic selection of the implementation.
>
> **Principle.** Silent `NULL` propagation is a property of SQL, so the fix is a rule at the seam: an unmappable instrument must fail loudly. If fees needed correcting, you fix forward with a backfill, not a rollback.

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Dive Deep** (P) | "The alert said fees were missing; the answer was in one function overload." | 切片 → 单笔 → 回溯 → 读两个重载；排除时序/stream 的证据 | — |
| **Ownership** (P) | "I wasn't the assignee; I forwarded the page to myself and stayed with it through the postmortem and the structural fix." | 止血之后继续 own：postmortem、重载合并、DROP | 说成止血 PR 是我的 |
| **Insist on the Highest Standards** (P) | "A stopgap fixes one case; I wanted the bug class impossible." | 单函数 + versioned DROP + e2e；fail loudly | — |
| **Have Backbone** (P) | "There was a proposal to add ACH to the exclusion list. I said no, with the numbers." | 不压掉检查；把数字写下来 | 这是「顶住压力」，没有「disagree and commit」后半 |
| **Customer Obsession** (S) | "Two hundred merchants weren't being charged correctly — silently." | 商户侧影响；fix forward 需要纠正分录 | 没有客户反馈数据，别编 |
| **Bias for Action** (S) | "I forwarded the alert to myself and had the answer in the thread within minutes." | 速度来自对 promote 链路的全局图景 | — |
| **Earn Trust** (S) | "The postmortem includes why our own tests missed it." | 四个 e2e 缺口，包括我自己的责任 | — |

## 5. 追问（≥5）

1. **What did you decide vs. the team?** → 判定检查是对的、费用真丢；不加排除名单；写下数字。
2. **Which part was yours?** → 根因、postmortem、overload consolidation、legacy DROP；**止血 PR 是队友的**（"I owned the RCA and the hardening; the stopgap landed first"）。
3. **Backfill?** → 灰度阶段队友原话「大概不需要 backfill」；**不说我 backfill 了**；方法论：fix forward + backfill if needed，计费里错误状态已被下游消费，需要更正分录而非回滚。
4. **Why didn't tests catch it?** → 四点：只断言路由；fixture 用卡 payload；pending 行不断言 sub_kind；没有跨 promote→fee 的测试；补了 e2e。
5. **How do you prevent the class of bug?** → fail loudly；NULL 拼接是 SQL 语言属性，修接缝不修调用点；单函数默认参数使新分支选不到不完整实现。
6. **Why delete via versioned migration?** → 删掉 `R__` repeatable 文件不会删已部署对象。
7. **How did you size the blast radius?** → 起初的 blast-radius 估算属于另一份复盘 S10，**不要混**。
8. **Impact on merchants / money actually lost?** → 【待 Chi 补：缺失费用最终是否 backfill、对商户/收入的实际影响】

## 6. 证据边界

止血 PR 不是我的；事故发生在灰度（standard-ACH M2）；不说「我 backfill 了」。证据：Slack 事故线程 2026-07-29、复盘 2026-08-11；Confluence 3029344728、3052036330；PR #3390 / #3490。

## 7. Senior 升级点（bar = senior）

当前档位：**mechanism（fail loudly、versioned DROP、e2e）与 ownership beyond task 已到 senior**；**influence 部分是缺口**：「有人建议把 ACH 加入排除名单」是最好的 Backbone 素材，但对方是谁、你怎么说服的没有细节。
- 【待 Chi 补：提出排除 ACH 的人是什么角色（同级/资深/PM）？你的原话是什么？最后谁拍板？（senior 档要求"对更资深的人说不并给出数据"）】
- 【待 Chi 补：postmortem 在哪个会上读过？有几个团队参加？后来其他团队有没有采用你写的 e2e 模式或 fail-loudly 规则？】
- 【待 Chi 补：灰度阶段缺费用的 ~$11.3M/天 GMV 最终是否补账、由谁、花了多久（Deliver Results 的结尾）】
- 升级句：把 "I fixed an overload bug" 改成 "I removed the mechanism that allowed this bug class and wrote down why our tests couldn't see it."
