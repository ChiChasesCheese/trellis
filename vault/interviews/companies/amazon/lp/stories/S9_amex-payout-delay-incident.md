# S9 · Amex 出款延迟事故（事故指挥里的领域权威）

> 来源：`core/stories/S9 Amex 出款延迟事故.md`（status: verified）。
> 主 LP：**Customer Obsession**；副：Dive Deep · Have Backbone · Earn Trust · Deliver Results · Ownership · Insist on the Highest Standards。
> 一句话：*"A large marketplace merchant reported about four million dollars of Amex payouts 'missing'; I was named one of three fix owners and separated expected latency from the real regression."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| ~$4M Amex 出款"不见了" | 商户报告 |
| 三位 fix owner 之一 | 指挥点名 |
| T+7 = 内部管线 SLA（美国 aggregated Amex） | 我给出的定性 |
| 6/23 一次 Agg-Amex effective-date 改动（为 EU 合规）把 US 出款日推后 ~1 天 | 真实根因 |
| 事故 2026-07-06 → 07-09 关闭，三天 | 时间线 |

## 2. 60–90 秒口播版（≈ 175 词）

> A large marketplace merchant reported roughly four million dollars of Amex payouts "missing," and a formal incident channel spun up. The incident commander named me one of three engineers who own the fix.
>
> I made two contributions. First, the SLA. A senior teammate said he didn't have context on US aggregated-Amex SLAs and deferred to me. I established that T+7 is our internal pipeline SLA for the US, and that we only disburse after Amex settles funds to our account. That separated expected latency from a real regression, which stopped the argument about whether we had breached anything.
>
> Second, the regression itself. A change made for EU compliance to an effective date had shifted US disbursement dates by a day. Reverting was the fast option. I argued for the robust one: a region conditional in the table function, so EU and US keep independent semantics. The group chose it. The fix was deployed by two teammates and the incident closed in three days.

## 3. 2 分钟版（≈ 265 词）

> **Customer impact.** A large marketplace merchant reported about four million dollars of Amex payouts they couldn't find; their phrasing was that it looked like seven days to pay out over a weekend. A formal incident channel opened.
>
> **My role.** The commander named three fix owners; I was one, for the Amex payout logic I knew best.
>
> **The first contribution — the boundary.** The most expensive thing in the room wasn't a bug, it was disagreement about where the line was: was this a breach? A senior engineer said he had no context on US aggregated-Amex SLAs and deferred to me. I said: seven days is our internal pipeline SLA for the US, and we only disburse after Amex settles the money to us. That separated "slower than the merchant expected" from "something regressed."
>
> **The second — the fix direction.** The commander reported that an effective-date change on June 23, made for EU compliance, had pushed US disbursement dates out about a day. The options were revert plus backfill, or a US/EU condition inside the table function. I argued for the conditional because it keeps EU and US semantics independent so the next compliance change doesn't re-break the other region. The group preferred it as more robust.
>
> **Result.** Two teammates deployed the fix; the incident closed July 9, three days after opening. I'm clear about my share: I was one of three owners; my piece was the SLA determination and the fix direction.
>
> **Learning.** In multi-owner incidents, take the part where you're the authority, state it plainly, and argue for the robust fix over the fast one.

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Customer Obsession** (P) | "A merchant told us four million dollars of payouts were missing; the first job was to tell them whether that was true." | 以商户的预期为起点；区分延迟 vs 回归 | 没有商户反馈数据，别编 |
| **Dive Deep** (S) | "The question wasn't 'is it slow'; it was 'what is the SLA, and what changed on June 23.'" | 内部 SLA 与上游到账的边界；effective-date 改动 | — |
| **Have Backbone** (S) | "Reverting was the fast option; I argued against it." | 主张 region conditional 而不是 revert；强调 robust | 不是 disagree-and-commit，且"group chose it" |
| **Earn Trust** (S) | "A senior engineer deferred to me, so I made sure what I said was precise and checkable." | 不越界；只说自己权威的那块 | — |
| **Deliver Results** (S) | "Three days from incident open to close." | 07-06 → 07-09 | 部署是同事做的 |
| **Ownership** (S) | "I was one of three owners and I took the piece I was the authority on." | 明确划线 | 声称"我修好了" |

## 5. 追问（≥5）

1. **What exactly did you do vs. the others?** → "one of three owners; my piece was the SLA determination and the fix direction"；修复由另两位同事落地部署。
2. **How did you know T+7 is the internal SLA?** → 【待 Chi 补：这个 SLA 的出处（设计文档/runbook）以及你如何确认"只在 Amex 结算到账后才出款"】
3. **Why region conditional over revert?** → revert 会把 EU 合规改动一起撤；条件分支让 EU/US 语义独立；代价：UDTF 里多一个分支和需要的测试 【待 Chi 补：测试怎么覆盖】。
4. **Did the merchant get their money?** → 【待 Chi 补：最终出款/是否补偿；$4M 是延迟不是丢失】
5. **What changed afterward so this wouldn't repeat?** → 【待 Chi 补：事故后有无 action item（如 effective-date 变更的 region 测试、SLA 文档化）；旧稿说"上游时序不是故障"是错的，别说】
6. **Whose PR caused it?** → 本组的一个 PR；不点名。说 "an effective-date change we made for EU compliance"。
7. **How did you handle disagreement in the channel?** → 把边界讲清，冲突自然消解；不去挤部署环节。

## 6. Senior 升级点（bar = senior）

当前档位：**cross-team + domain authority 是 senior 级**；缺 **mechanism**（事故后改了什么）与 **disagree-and-commit** 的完整版本。
- 【待 Chi 补：事故复盘里你推动的 action item（SLA 文档、effective-date 变更的双区域测试、告警）】
- 【待 Chi 补：有没有人主张 revert？是谁（角色）？你如何论证、结果是否被采纳？如果你的意见被否决，你如何执行了别人的决定——这正是 LP13 要的故事】
- 升级句：「I argued for the fix that keeps EU and US semantics independent, and I made the SLA boundary something everyone could repeat.」
