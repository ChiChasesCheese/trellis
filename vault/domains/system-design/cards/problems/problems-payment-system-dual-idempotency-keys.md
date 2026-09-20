---
id: problems-payment-system-dual-idempotency-keys
node: problems.commerce.payment-system
type: qa
step: 2
tags: [grown]
---
## Q
In a payment system that calls out to a PSP (payment service provider), why does a single client-generated idempotency key at the API layer fail to prevent double charges, and what second key closes the gap?

## A
A client-side idempotency key only protects the "client to our API" hop: it lets a retried `POST /charges` return the cached response instead of re-executing. But if our process crashes after calling the PSP and before recording the result, the recovery path sees no record and can only blindly re-call the PSP. The fix is a second, independent idempotency key passed to the PSP itself on every outbound call — even if our own state is lost, replaying the same PSP-side key returns the PSP's already-processed result instead of charging again. The two keys protect two different network hops.

## Q zh
在一个需要调用 PSP（支付服务商）的支付系统设计中，为什么仅在 API 层用一个客户端生成的幂等键无法防止重复扣款？还需要哪个第二层的键来补上这个缺口？

## A zh
客户端幂等键只保护"客户端到我们 API"这一段：它让重试的 `POST /charges` 直接回放缓存响应而不重新执行。但如果我们的进程在调用 PSP 之后、记录结果之前崩溃，恢复逻辑看不到任何记录，只能盲目重新调用 PSP。解法是在每次对外调用时额外传一个独立于我们自己的、给 PSP 侧使用的幂等键——即使我们自己的状态丢失，重放同一个 PSP 侧键也会返回 PSP 已经处理过的结果，而不是二次扣款。两个键分别保护两段不同的网络跳。
