---
id: security-sessions-vs-jwt
node: security.authn.tokens
type: qa
---
## Q
Server-side sessions vs JWTs: what does each trade away, and which one makes "log out this user now" hard?

## A
- **Sessions**: opaque id, state in a server store (Redis/DB). Instant revocation — delete the row — but every request costs a store lookup, and the store is shared infrastructure to scale.
- **JWTs**: claims signed into the token; any service verifies locally, no lookup, great for cross-service auth. But they are valid until expiry — **revocation is the hard part**: you need short lifetimes plus a denylist or key rotation, which quietly reintroduces the server-side state JWTs promised to remove.

## Q zh
服务端会话 vs JWT：各交易什么，哪个让「现在登出这个用户」难？

## A zh
- **会话**：不透明 id，状态在服务器存储（Redis/DB）。即时撤销 — 删除行 — 但每个请求花费存储查找，存储是共享基础设施以扩展。
- **JWT**：声明签到 token；任何服务本地验证，无查找，对跨服务认证很好。但他们有效直到过期 — **撤销是难部分**：你需短生命周期加黑名单或 key 轮换，悄悄重新引入服务端状态 JWT 承诺移除。
