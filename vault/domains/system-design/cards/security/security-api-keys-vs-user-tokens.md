---
id: security-api-keys-vs-user-tokens
node: security.authz
type: qa
---
## Q
API keys vs user tokens: what does each identify, and why must a multi-tenant API never authorize on the key alone?

## A
- **API key**: identifies an **application/tenant** — long-lived, no user context, ideal for server-to-server calls, metering, and rate limiting per customer. Store only a hash; support rotation with overlapping validity.
- **User token** (OAuth access token): identifies a **user (and scopes)** — short-lived, carries the actual authority to act on that user's data.

A key alone tells you *who is calling*, not *on whose behalf*. Authorizing tenant-scoped data by key without checking the acting user's rights is the classic **confused deputy** / BOLA vulnerability.

## Q zh
API key vs 用户 token：各标识什么，为什么多租户 API 绝不能仅在 key 上授权？

## A zh
- **API key**：标识**应用/租户** — 长生命周期，无用户上下文，理想用于服务间调用、计量、按客户速率限制。仅存哈希；支持重叠有效性的轮换。
- **用户 token**（OAuth access token）：标识**用户（和 scope）** — 短生命周期，携带作用于那个用户数据的实际权限。

key 单独告诉你*谁在调用*，不是*代表谁*。不检查表演用户权限而按 key 授权租户范围数据是经典**混淆代理** / BOLA 漏洞。
