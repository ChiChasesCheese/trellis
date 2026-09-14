---
id: reliability-retryable-errors
node: reliability.resilience.retries
type: qa
---
## Q
Classify which failures are worth retrying and which are not — and explain why a *timeout* is the hardest case.

## A
- **Retry**: connection refused / reset / DNS failure *before* the request was sent (nothing executed), `503`, `429` (obey `Retry-After`), gRPC `UNAVAILABLE` / `RESOURCE_EXHAUSTED`, and read-only requests that failed anywhere.
- **Never retry**: deterministic client errors — `400`, `401`, `403`, `404`, `422`, gRPC `INVALID_ARGUMENT` / `PERMISSION_DENIED`. The same request will fail identically; retrying only burns budget and hides the bug.
- **Timeout / `502` / `504` on a write is ambiguous**: you cannot distinguish "never arrived" from "succeeded, response lost". Blind retry risks a double charge; giving up risks losing a completed order the user thinks failed.

The fix is to remove the ambiguity, not to guess: send an **idempotency key** so the server can recognize the retry and replay the original outcome. Then every write becomes retryable by construction — "retryable" is a property you design in, not one you discover in the error code.

## Q zh
分类哪些故障值得重试哪些不是——解释为什么*timeout*是最难的情况。

## A zh
- **Retry**：连接被拒绝 / 重置 / DNS 故障*之前*请求被发送（没有执行），`503`，`429`（遵守`Retry-After`），gRPC`UNAVAILABLE` / `RESOURCE_EXHAUSTED`，读取-仅请求在任何地方失败。
- **永不重试**：确定性客户端错误——`400`，`401`，`403`，`404`，`422`，gRPC`INVALID_ARGUMENT` / `PERMISSION_DENIED`。相同请求会相同地失败；重试只烧预算并隐藏错误。
- **Timeout / `502` / `504`在写上是模糊的**：你无法区分"永不到达"从"成功，响应丢失"。盲目重试风险双重收费；放弃风险丢失用户认为失败的完成订单。

修复是移除模糊，而不是猜测：发送**幂等性键**所以服务器可以识别重试并重放原始结果。然后每个写因构造而变得可重试——"可重试"是你设计的属性，不是你在错误代码中发现的。
