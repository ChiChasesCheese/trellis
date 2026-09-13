---
id: content-ppr-stream-failure
node: content.ppr
type: qa
---
## Q
The static shell has been sent, then one dynamic PPR hole fails. Why must failure handling be scoped to the hole?

## A
The response status and shell are already committed, so the server cannot replace the entire response with a clean error page. The dynamic boundary needs its own fallback/error UI, timeout, cancellation, and telemetry. Other holes should continue streaming independently. This is partial failure by construction: a slow recommendation must not delay or invalidate the shared shell, cart, or unrelated content.

## Q zh
static shell 已发送，随后一个 dynamic PPR hole 失败。为什么 failure handling 必须限制在该 hole 内？

## A zh
response status 和 shell 已 committed，server 无法再用完整 error page 替换整条响应。dynamic boundary 必须拥有自己的 fallback/error UI、timeout、cancellation 和 telemetry。其他 hole 应继续独立 streaming。这就是结构化 partial failure：slow recommendation 不能延迟或使 shared shell、cart 或无关内容失效。
