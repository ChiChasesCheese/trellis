---
id: problems-payment-system-timeout-as-unknown
node: problems.commerce.payment-system
type: qa
step: 4
tags: [grown]
---
## Q
In a payment system, a call to authorize a charge through the PSP times out. Why is blindly retrying the mutating call the wrong default, and what should happen instead?

## A
A timeout is ambiguous: the request may never have reached the PSP (safe to retry), or the PSP may have already processed it and only the response was lost (retrying would charge twice). Blindly retrying assumes the PSP's own idempotency protection will always catch the duplicate, which silently fails if its dedup window has expired or the call didn't carry a PSP-side idempotency key. The correct default is to treat the timeout as unknown: call the PSP's status/query endpoint with the original reference to find the true outcome, and only then decide whether to retry, mark complete, or mark failed.

## Q zh
在支付系统中，一次向 PSP 发起的授权调用超时了。为什么盲目重试这个有副作用的调用是错误的默认做法？正确的做法是什么？

## A zh
超时是有歧义的：请求可能从未到达 PSP（安全重试），也可能 PSP 已经处理完成、只是响应丢失了（重试会造成二次扣款）。盲目重试假设 PSP 自己的幂等保护总能拦住重复请求，但如果它的去重窗口已过期，或这次调用根本没带 PSP 侧幂等键，这个假设会静默失效。正确的默认做法是把超时当作"未知"：用原始引用号调用 PSP 的查询接口问清楚真实结果，再据此决定重试、标记完成还是标记失败。
