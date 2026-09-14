---
id: delivery-flags-safe-default
node: delivery.flags
type: qa
---
## Q
The feature-flag service times out while a new cache-key policy is at 10%. What should the data plane do?

## A
Use a locally cached, versioned decision with an explicit expiry and a predeclared safe default; never block every request on the control plane. For a correctness-sensitive cache-key change, the default should normally select the proven old policy or bypass shared caching, not guess the new value. Emit the fallback reason and active config version so degraded behavior is visible.

## Q zh
新的 cache-key policy rollout 到 10% 时，feature-flag service timeout。data plane 应该怎么做？

## A zh
使用 locally cached、versioned 的 decision，并设置明确 expiry 与预先声明的 safe default；绝不能让每个 request 等待 control plane。对于 correctness-sensitive cache-key change，default 通常应选择已验证的旧 policy 或 bypass shared caching，而不是猜测新值。记录 fallback reason 和 active config version，让 degraded behavior 可见。
