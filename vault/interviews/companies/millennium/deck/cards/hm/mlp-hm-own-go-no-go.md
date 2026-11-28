---
id: mlp-hm-own-go-no-go
node: hm.ownership
type: qa
step: 3
---
## Q
**主动踩刹车：go/no-go**｜经理面与行为面

“Tell me about a time you pushed back or decided not to ship something.” 也可能问：“你怎么决定什么该做、什么不该做？”

## A
用实习生留下的费用异常检测器。主动做事容易讲，主动停下来更难，也更像资深工程师的判断。

- **情境：** 实习生离职前留下一个只在 QA 跑过的机器学习异常检测器。QA 有 6 个合成商户，生产有一万八千个商户，高峰一天约 7.6 亿行。
- **判断：** 逐行用 numpy 推理的服务方式在生产必然超时，而 QA 永远暴露不了。
- **你的做法：** 先分清离职会丢什么，只有分析师的人工标注不可再生，所以先导出；再分两阶段：第一阶段只上确定性规则（`|amount| = rate × qty + fixed`，纯 SQL），第二阶段模型重训和推理重构放在 go/no-go 门后；冻结 Slack 告警和 CI/CD，直到门给出 go。
- **原则：** 按风险调整后的价值排优先级，不按沉没成本。

**英文答法。**
- I inherited an **ML anomaly detector** that had only run in QA: **six synthetic merchants** versus **eighteen thousand** in production.
- Per-row inference would **time out** at up to about **760 million rows** on a peak day, and QA could never show it.
- I wrote a **go/no-go assessment**: first saved the analyst labels, the only irreplaceable part; then **Phase 1** ships only the deterministic rule as **pure SQL**.
- **Phase 2**, the model retrain and serving redesign, sits behind an explicit gate. I'd rather stop a project than ship one that pages the team at 3 a.m.

**追问。**
- **Why not just keep building?** Sunk cost isn't a reason; I rank by **risk-adjusted value**.
- **What was the biggest risk?** Inference scale first, then unknown precision, then alert volume: a 99.5% threshold on hundreds of millions of rows means millions of alerts a day.
- **How long would it take?** Two to three months to production-trustworthy, which is why it sits behind a gate.
