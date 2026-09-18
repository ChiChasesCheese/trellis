---
title: S10 · 退款费 billing-terms 复盘
aliases:
  - S10
  - billing-terms 复盘
  - To net or not to net
tags:
  - interview/story
  - stack/sql
  - integrity
answers: [Q3, Q8, Q19]
stacks: [TS09, TS10]
status: verified
---

# S10 · 退款费 billing-terms 复盘（推翻自己的数字 · 定量推理）

> [!abstract] 一句话
> 一家大型电商商户切到 net settlement 后，部分退款费带着旧的 MONTHLY billing terms 出来。我第一版 blast-radius 查询给出约 196K 行 / 61 商户 / $11K；在任何人据此行动之前我重审谓词，发现它没有检查"新定价计划在费用创建时已存在"——很多行的计划是几个月后回填的，写入时本来就是对的。加上 `schedule.created_at <= fee.created_at`，真实范围是 **21,923 行 / 30 商户 / $5,854**。根因是退款费路径复制了 credit 的历史 `pricing_schedule_id`，而不是在费用创建时解析生效计划；顺带发现上游一个 1.5 小时的"计划写入滞后"脆弱点，一处修复覆盖两者。

## 1. 谓词是怎么错的

| 版本 | 谓词 | 结果 |
|---|---|---|
| 第一版 | credit 的计划是 monthly ∧ 费用创建当天商户生效计划是 daily/net ∧ 生成的 billing_terms 仍是 MONTHLY | 196,274 行 / 61 商户 / $11,123 |
| **修正** | + `ps_curr.created_at <= bf.created_at`（新计划在费用创建时物理存在） | **21,923 行 / 10,330 credits / 30 商户 / $5,854.52** |

为什么爆炸半径天然收敛：切换后新 credit 自动拿到 NET 计划 id，bug 不再累积；只有"切换前积压了大量退款费、切换后才补跑"的商户（那家电商：216 行、延迟 214 天）影响大。1,062 个切到 NET 的美国商户里只有 5 个产生了 bug 费用。

## 2. 两个叠加的脆弱点

1. **下游**：退款费管线复用 credit 的历史 `pricing_schedule_id`，而不是在费用创建时调 `EFFECTIVE_PRICING_SCHEDULE(maid, date)`。
2. **上游**：`EFFECTIVE_PRICING_SCHEDULE` 按查询时刻数据库里**物理存在**的计划解析——某商户的 NET 计划在交易流处理完当天 credit 之后 1 小时 32 分才写入，credit 被永久打上旧计划。批量上线时这种滞后可能是系统性的。

让下游在费用创建时重新解析生效计划，两个都缓解。

## 3. 讲法

- "I'd rather retract my own number in public than have a remediation sized off a bad predicate."
- 定量推理的可审计性：每条断言配一个可复跑的查询；`GET_BILLING_TERMS` 纯数据驱动、无国家硬编码——先排除"美国特判"这类错误假设。

> [!warning] 证据边界
> 不点商户名（"a large e-commerce merchant"）。$ 数字来自 `SUM(ABS(amount))/100`，口径明确。

## 4. English · 首答（60 s）

> After a large e-commerce merchant moved to net settlement, some refund fees came out tagged with the old monthly billing terms. My first blast-radius query said about two hundred thousand fee rows across sixty merchants. Before anyone acted on it I re-examined the predicate and found it was wrong: it didn't check that the new pricing schedule existed at fee-creation time — many of those rows had schedules backdated months later and were correct when written. Adding `schedule.created_at <= fee.created_at` took the real scope to about twenty-two thousand rows, thirty merchants, under six thousand dollars.
>
> The root cause was the refund-fee path copying the credit's historical `pricing_schedule_id` instead of resolving the effective schedule at fee time. Along the way I found a second, upstream fragility — a pricing schedule written to the database an hour after the transaction stream had already stamped the day's credits — and showed one fix covers both. I'd rather retract my own number in public than have a remediation sized off a bad predicate.

## 5. 用在哪

- 回答：[[Answers#Q3]]（定量部分）· [[Answers#Q8]] 衡量价值 · [[Answers#Q19]] 失败与成长（外部批评版的替代）
- 场景题：两系统对不上一个数字
- 技术栈：[[09-sql-data-modeling|TS09]] · [[10-correctness-idempotency|TS10]]
- 相邻：[[S5]]（同一项目）· [[S3]]（另一次 RCA）· [[S4]]

## 6. 证据锚点

Confluence 2946204146（含完整 SQL 附录）；Jira DTBTTFOUND-2925 / 2944 / 3044；PR #2246 / #2689 / #2753 / #2763 / #2966（TEMU/SHEIN 退款费回填：191,191 笔 sales → 382,382 fee 行等）。
