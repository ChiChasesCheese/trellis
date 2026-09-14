---
id: correctness-reconciliation
node: correctness.ledger
type: qa
---
## Q
Your ledger has idempotency keys, an outbox, and zero-sum checks. Why do you still run reconciliation against the payment processor, and what does the job actually do?

## A
Because those patterns protect *your* writes — they can't see the **external world disagreeing**: charges that succeeded at the processor after you recorded a timeout-failure, fees and FX applied on their side, chargebacks, or plain bugs on either end. Reconciliation is the safety net that catches what every other control missed.

The job: ingest the processor's **settlement report**, match line-items to ledger entries (by processor id / idempotency key), and bucket every mismatch — **missing ours** (they have it, we don't), **missing theirs**, **amount/state mismatch** — into a workqueue with an owner and an aging SLA. Match rate and unresolved-break age are the health metrics; run it daily at minimum.

## Q zh
你的账本有幂等性 key、outbox 和零和检查。为什么还要针对支付处理方跑对账，工作实际做什么？

## A zh
因为那些模式保护*你的*写 — 它们看不到**外部世界不同意**：处理方成功但你记录超时失败的扣款，他们那边用的手续费和 FX，退单，或任一端的纯 bug。对账是安全网，抓住其他所有控制遗漏的。

工作：摄入处理方的**清算报告**，匹配行项到账本分录（按处理方 id / 幂等性 key），将每个不匹配分桶 — **我们缺少**（他们有我们没），**他们缺少**、**金额/状态不匹配** — 进一个有所有者和老化 SLA 的工作队列。匹配率和未解断差年龄是健康指标；至少日运。
