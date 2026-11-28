---
id: mlp-hm-team-au-refund
node: hm.teamwork
type: qa
step: 1
---
## Q
**跨团队：AU 退款费**｜经理面与行为面

“Tell me about a time you worked with another team to solve a problem.” 也可能是：“你怎么向非技术的同事解释技术问题？”

## A
用澳洲 Amex 退款费这件事。它同时答跨团队和向非技术方解释，因为你给产品经理的是一份人人能复跑的证据。

- **情境：** 产品经理走正式求助流程，说澳洲商户看不到 Amex 退款费（商户被退款时对应的手续费条目）。三个团队来回 50 条回复，最后点名到你。
- **做法：** 不查组织架构，查数据：六个月内美国约 108 万行退款费、澳洲 0 行，涉及 157 个澳洲商户。
- **根因：** 是配置不是代码：每个澳洲商户的定价计划里 `fee_refund_policy = partial`，而退款费逻辑只在 `full` 时触发。而且这早于平台迁移，不是我们引入的回归。
- **结果：** 写成带查询的结论，让对方自己复跑，当天结束讨论，变成一张功能票。

**英文答法。**
- A PM escalated that **Australian merchants** weren't seeing Amex refund fees; it bounced through three teams in a **fifty-reply thread** before reaching me.
- I pulled the data, not the org chart: **over a million** refund-fee rows in the US over six months, **zero** in Australia.
- The cause was **configuration, not code**: every AU schedule had `fee_refund_policy = partial`, and the logic only fires on `full`. It **predated our migration**.
- I wrote it up **with the exact query** so they could re-run it; the thread ended that day and became a tracked feature.

**追问。**
- **How did you explain it to a non-technical person?** One number they could verify: US million rows, Australia zero, plus the query to re-run.
- **What if you weren't sure?** A second fee kind came up in the same thread; I said **not sure yet**, gave a layered hypothesis, and a senior engineer confirmed it.
- **Why does "predates the migration" matter?** It turns blame into a shared fact.
