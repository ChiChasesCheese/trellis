---
id: delivery-shadow-side-effects
node: delivery.shadow
type: qa
---
## Q
You mirror production cache-miss requests to a new implementation. What must be disabled or isolated before calling this shadow mode?

## A
Suppress externally visible side effects: no live cache writes, purge, billing, analytics duplication, user response, or origin mutation. Use isolated storage and credentials, preserve cancellation and privacy rules, and mark shadow traffic so dependencies can measure and limit it. A copy that can change production state is a second writer, not a shadow.

## Q zh
你把 production cache-miss request mirror 到新 implementation。在称其为 shadow mode 前，必须 disable 或 isolate 什么？

## A zh
必须禁止 externally visible side effect：不能写 live cache、执行 purge、产生重复 billing/analytics、返回 user response 或修改 origin。使用 isolated storage 和 credential，保留 cancellation 与 privacy rule，并标记 shadow traffic，让 dependency 能测量和限制它。能改变 production state 的 copy 是 second writer，不是 shadow。
