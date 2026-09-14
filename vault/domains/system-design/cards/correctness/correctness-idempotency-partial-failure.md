---
id: correctness-idempotency-partial-failure
node: correctness.idempotency
type: qa
---
## Q
A payment handler claims its idempotency key, calls the card processor, then crashes before recording the result. The key is stuck "in-progress". What must recovery do?

## A
The processor may or may not have charged — so neither blind retry nor blind fail is safe.

- Attach a **lease/expiry** to the in-progress state; a stuck key past its lease goes to a **recovery step**, not straight to re-execution.
- Recovery **queries the downstream by ITS idempotency key** ("did charge X happen?") — possible only if you persisted the downstream key *before* the outbound call.
- Then finish deterministically: record the found result, or safely re-issue with the **same** downstream key so the processor dedups.

Rule: every external call inside an idempotent handler needs its own pre-persisted idempotency key — that's what makes the crash window recoverable ([[correctness-idempotency-concurrent-retries]]).

## Q zh
支付处理器声称了幂等性 key，调用卡处理器，然后在记录结果前崩溃。key 卡在"in-progress"。恢复必须做什么？

## A zh
处理器可能扣过款也可能没扣 — 所以盲目重试和盲目失败都不安全。

- 给 in-progress 状态附加**租期/过期时间**；超过租期的卡顿 key 进**恢复步骤**，不直接重新执行。
- 恢复**用其幂等性 key 查询下游**（"扣款 X 发生了吗？"）— 仅当你在出站调用前持久化了下游 key 才可能。
- 然后确定性完成：记录找到的结果，或用**相同**下游 key 安全地重新发起，处理器去重。

规则：幂等性处理器内的每个外部调用都需要自己的预先持久化幂等性 key — 这就是使崩溃窗口可恢复的原因（[[correctness-idempotency-concurrent-retries]]）。
