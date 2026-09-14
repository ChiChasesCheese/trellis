---
id: net-http-safe-idempotent
node: networking.http-semantics
type: qa
---
## Q
A gateway wants to automatically retry a timed-out request. Why is checking only `GET` versus `POST` too crude?

## A
Retry safety depends on **method semantics plus application behavior**. Safe methods should not change state; idempotent methods can be repeated with the same intended effect, but a broken `GET` may mutate and a `POST` may be protected by an idempotency key. Retry only when no response was committed, the operation is known repeatable, and the deadline/budget permits it.

## Q zh
gateway 想自动 retry 一个 timeout 请求。为什么只看 `GET` 还是 `POST` 太粗糙？

## A zh
retry safety 取决于 **method semantics 加 application behavior**。safe method 不应改变状态；idempotent method 重复执行应保持同一预期效果，但错误实现的 `GET` 可能写状态，而 `POST` 也可能受 idempotency key 保护。只有在响应尚未 commit、操作已知可重复且 deadline/budget 允许时才 retry。
