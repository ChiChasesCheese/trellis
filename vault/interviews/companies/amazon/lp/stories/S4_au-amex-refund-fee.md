# S4 · AU Amex 退款费（用一条查询结束 50 条回复）

> 来源：`core/stories/S4 AU Amex 退款费.md`（status: verified）。
> 主 LP：**Customer Obsession · Dive Deep · Earn Trust**；副：Are Right A Lot · Have Backbone · Ownership。
> 一句话：*"A product manager's escalation bounced through three teams for 50 replies; I ended it the same day with one query anyone could re-run."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| 50 条回复 / 3 个团队 | 路由到我之前的线程 |
| 美国 ~1,079,627 行退款费 · 英国 294 · 澳洲 **0** | 六个月，`NON_AGGREGATED_TRANSACTION_FEE_REFUND` 按国家 |
| 157 个 AU 商户 · 288 万笔 AU non-agg Amex 销售 | 同一查询 |
| 所有 AU 商户 `fee_refund_policy = partial`（或 none），退款费逻辑只在 `full` 触发 | 根因：配置，非代码 |
| 早于平台迁移（predates the migration） | 定性 |
| 时间 2026-08-03 → 08-17；Jira DTBTTFOUND-3269 / 3310 | 锚点 |
| 当天结束线程，转成功能票 "REFUND_FEE calculation pipeline in Snowglobe" | 结果 |

## 2. 60–90 秒口播版（≈ 170 词）

> A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. It bounced across three teams for about fifty replies before it was routed to me as the person who knows that domain.
>
> I pulled the data instead of the org chart. Over six months there were more than a million refund-fee rows in the US and zero in Australia, across about a hundred and fifty merchants. The root cause was configuration, not code: every Australian merchant's pricing schedule had the refund policy set to `partial`, and the refund-fee logic only fires on `full`. I also showed it predated our platform migration, so it wasn't a regression we introduced.
>
> I wrote it up with the exact query so the PM and the other team could re-run it themselves. It ended the thread the same day and became a tracked feature to build the refund-fee pipeline properly. In the same thread a second, unrelated fee kind came up; I said I wasn't sure, laid out a layered hypothesis, and a senior engineer confirmed it. I'd rather say "not sure yet" with a plan than guess.

## 3. 2 分钟版（≈ 260 词）

> **Situation.** Through the formal Request-Help process, a PM asked why Australian merchants couldn't see Amex refund fees. Three teams, fifty replies, each pointing at the others: data, config, or logic. I was named because I had context on both Australian Amex transactions and Braintree fees.
>
> **Approach.** I treated it as a data question. I counted refund-fee rows by country over six months: about 1.08 million in the US, 294 in Great Britain, zero in Australia, even though there were around 2.88 million Australian non-aggregated Amex sales across 157 merchants. So it wasn't low volume.
>
> **Root cause.** I looked at the pricing schedules: every Australian merchant had `fee_refund_policy` of `partial`, never `full`, and refund fees are only generated on `full`. Config, not code. Then I checked history: the upstream payout service had never produced refund fees for Australian direct Amex. The only thing that changed in our migration was the reporting. That sentence — "it predates the migration" — turned a blame thread into a shared fact.
>
> **Action.** I wrote the conclusion with the queries inline so the PM and the other team could re-run them. A second question came up, an Australia-only `refund` fee kind. I said I wasn't certain, gave a layered hypothesis and how I'd verify it, and a senior engineer confirmed I was right.
>
> **Result.** The thread ended the same day and a feature ticket was opened to build the refund-fee pipeline in our platform. What I took from it: when a disagreement is really a knowledge asymmetry, hand everyone the same evidence instead of arguing about ownership.

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Customer Obsession** (P) | "Australian merchants weren't getting the refund fees they were due, and nobody on three teams owned finding out why." | 客户（AU 商户 + PM）的痛；回到证据；变成正式功能票 | 没有商户补偿数字，别编 |
| **Dive Deep** (P) | "I didn't read the org chart, I read the data: a million rows versus zero." | 按国家拉数 → 定位到 `fee_refund_policy` → 证明早于迁移 | — |
| **Earn Trust** (P) | "I put the exact query in the write-up so the other team could check my claim themselves." | 可复跑证据；对第二个问题坦承 not sure + 计划 | — |
| **Are Right, A Lot** (S) | "I said I wasn't sure yet and gave a hypothesis I could be wrong about." | 分层假设，被资深同事确认 | 不说「我从来不错」 |
| **Have Backbone** (S) | "Three teams were pointing at each other; I said, with the numbers, it's config and it predates us." | 不接受「是迁移的锅」的叙事 | 不是 disagree-and-commit |
| **Ownership** (S) | "It wasn't my ticket; I owned the answer." | 不属于我的问题我仍给出结论 | 不说「PM 让我做」，说 routed to me as the person who knows that domain |

## 5. 追问（≥5）

1. **How did you know it wasn't a regression?** → 上游出款服务从来没为 AU direct-Amex 发过退款费；变的只是报表口径。
2. **Why did you pull data rather than discuss?** → 争论源于领域知识不对称；数据让所有人当场可验证。
3. **What was the second issue?** → AU-only `refund` fee kind；我说不确定、给分层假设；资深同事确认。
4. **What did you do for the merchants in the meantime?** → 【待 Chi 补：是否有临时补偿/手工修复；没有就如实说「没有，已立功能票」】
5. **What if the data had contradicted your guess?** → 方法不变：结论由查询给出，不由我给出；【待 Chi 补：你最初的假设是什么、被数据推翻了哪一半（如果有的话——被问「错的假设」时需要真实细节）】
6. **Who owns the new feature?** → 【待 Chi 补：feature ticket 的 owner 与排期】
7. **How big is the money?** → 【待 Chi 补：AU 漏掉的退款费金额量级】

## 6. 证据边界

不点名同事；不说「PM 让我做」；Slack #service-pricing 2026-08-03 → 08-17。

## 7. Senior 升级点（bar = senior）

当前档位：**cross-team influence without authority 已是 senior 级**（50 条回复、三个团队、证据说服）；**缺 outcome 与 mechanism**：目前停在「结束了争论、立了票」。
- 补 mechanism：【待 Chi 补：写完后有没有把"按国家/配置拉数"的查询存成团队 runbook / 看板，下一次类似问题能自助？】
- 补 impact：【待 Chi 补：AU 漏掉的退款费金额量级；feature ticket 后来是否排期/上线】
- 补 ambiguity：【待 Chi 补：线程里谁最初主张"是迁移的锅"，你如何在不得罪人的前提下纠正？】
- 升级句：「I turned a blame thread into a shared fact, and I left a query anyone can re-run.」
