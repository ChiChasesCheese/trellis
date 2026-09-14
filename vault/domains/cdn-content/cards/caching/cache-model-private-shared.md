---
id: cache-model-private-shared
node: caching.model
type: qa
---
## Q
A personalized HTML response may be stored in the user's browser but must never be reused for another user at a CDN. Which cache policy expresses that?

## A
Use `Cache-Control: private` with an intentional freshness/revalidation policy. `private` permits a private user-agent cache but forbids shared caches from storing the response. Do not rely on the presence of cookies alone: cache eligibility must be explicit, and authenticated/personalized variants need a reviewed key or a shared-cache bypass.

## Q zh
personalized HTML 可以存入用户 browser，但绝不能被 CDN 复用于其他用户。什么 cache policy 能表达这一点？

## A zh
使用 `Cache-Control: private`，再配合明确的 freshness/revalidation policy。`private` 允许 private user-agent cache 存储，却禁止 shared cache 存储。不要只依赖 cookie 是否存在：cache eligibility 必须显式，authenticated/personalized variant 需要经过审查的 key，或者绕过 shared cache。
