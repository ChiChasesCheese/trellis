---
id: correctness-idempotency-response-replay
node: correctness.idempotency
type: qa
---
## Q
On an idempotency-key hit, why must the server replay the **stored response** rather than re-execute the handler "since it's idempotent anyway"?

## A
Re-execution can **diverge** from the original run: prices, FX rates, fees, or risk rules may have changed; generated values (ids, timestamps) differ; and referenced state may have moved on (the order it read is now cancelled). The client would see two *different* answers to the same request — breaking the contract that a retry is indistinguishable from the first attempt.

So the key record stores the **full response (status + body)** written when the operation completes, and every subsequent hit returns those bytes verbatim (Stripe model). Re-execution is only safe for truly deterministic, side-effect-free reads — which don't need idempotency keys at all.

## Q zh
在幂等性 key 命中时，为什么服务器必须重放**存储的响应**而不是重新执行处理器"既然它已经幂等"？

## A zh
重新执行可能**偏离**原始运行：价格、汇率、费用或风险规则可能改变；生成值（id、时间戳）不同；引用的状态可能演进（读到的订单现在已取消）。客户端会看到对同一请求的两个*不同*答案 — 破坏"重试与首次尝试无法区分"的契约。

所以 key 记录存储**完整响应（状态 + 响应体）**，在操作完成时写入，每次后续命中原文返回这些字节（Stripe 模型）。重新执行仅对真正确定性、无副作用的读安全 — 这类读根本不需要幂等性 key。
