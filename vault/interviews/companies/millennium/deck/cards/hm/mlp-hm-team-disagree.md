---
id: mlp-hm-team-disagree
node: hm.teamwork
type: qa
step: 2
---
## Q
**意见不同：revert 还是条件分支**｜经理面与行为面

“Tell me about a time you disagreed with a decision. What did you do?”

## A
用 Amex 出款延迟事故里的修法分歧。分歧是技术性的，你用论据而不是资历。

- **情境：** 一家大型 marketplace 商户报告约 400 万美元 Amex 出款“不见了”，开了正式事故频道，指挥点名你是三位修复负责人之一。
- **第一个贡献：** 资深同事说自己不了解美国聚合 Amex 的 SLA（服务时限），交给你。你说清 T+7 是内部管线 SLA，并且只有 Amex 把钱结算到我们账户后才出款，这样把预期内的延迟和真正的回归分开。
- **第二个贡献：** 回归是一次为欧盟合规改生效日期的变更，把美国出款日推后一天。快办法是 revert（撤销改动），你主张在表函数里加区域条件，让欧盟和美国语义独立，小组选了这个。
- **边界：** 你是三位负责人之一；部署由同事完成。三天关闭。

**英文答法。**
- A large marketplace merchant reported about **four million dollars** of Amex payouts missing; I was one of **three owners** of the fix.
- First I settled the **SLA**: T+7 is our internal pipeline SLA, and we only disburse **after Amex settles the funds to us** — expected latency versus a real regression.
- The regression was an **effective-date change for EU compliance** that shifted US payouts by a day. Reverting was fast; I argued for a **region conditional** in the table function so EU and US keep independent semantics.
- The group chose it; incident closed in **three days**.

**追问。**
- **Why not revert?** It would undo the EU compliance change and couple the two regions again; the conditional is more robust.
- **Did you deploy it?** No, teammates deployed; my piece was the SLA call and the fix direction.
- **How do you handle disagreement in general?** Put the boundary and evidence on the table first; most conflict is a misunderstanding about where the boundary is.
