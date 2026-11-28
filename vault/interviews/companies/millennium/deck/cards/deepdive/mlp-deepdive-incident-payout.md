---
id: mlp-deepdive-incident-payout
node: deepdive.incidents
type: qa
step: 4
---
## Q
**出款延迟事故里你的部分**｜项目深挖

“Tell me about an incident where several people owned the fix. What did you contribute?”

## A
这一题重点是多人事故里你拿哪一块。

- **事故：** 大型 marketplace 商户报告约 400 万美元 Amex 出款“不见了”，开了正式事故频道，三位工程师负责修复，你是其中之一。
- **你的第一块，SLA：** 同事说他没有美国聚合 Amex SLA 的背景，请你定。你给的结论：T+7 是内部管线的 SLA，我们只在 Amex 把钱结算到我们账户之后才出款。这样把预期内的延迟和真正的回归分开。
- **你的第二块，修法方向：** 回归是一次为欧盟合规改生效日期的变更，把美国出款日推后约一天。你主张在表函数里加区域条件，而不是撤销。
- **不是你的：** 部署由两位同事完成；事故三天关闭。

**英文答法。**
- A marketplace merchant said about **four million dollars** of Amex payouts were missing; I was **one of three owners** of the fix.
- My first piece was the **SLA**: **T+7 is our internal pipeline SLA**, and we disburse only after Amex settles funds to us.
- My second piece was the **fix direction**: a **region conditional** instead of a revert, so EU and US semantics stay independent.
- Teammates deployed it; the incident closed in **three days**.

**追问。**
- **Root cause?** An effective-date change for EU compliance shifted US payout dates by about a day.
