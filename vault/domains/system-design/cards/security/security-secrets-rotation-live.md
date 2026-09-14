---
id: security-secrets-rotation-live
node: security.authz
type: qa
---
## Q
How do you rotate a database password or a JWT signing key without restarting services or dropping a single request?

## A
Never flip atomically — rotate with an **overlap window** where two versions are valid:

- **Consumed secrets** (DB passwords): create the new credential *alongside* the old (two-user or dual-password scheme), let clients hot-reload it (watch the secret mount / re-fetch on auth failure / short Vault leases that force re-fetch), then revoke the old only after telemetry shows zero use.
- **Signing keys**: publish old + new public keys in JWKS with `kid`s; **sign with new, verify with both** until every token signed by the old key has expired, then drop it.

Design rule: any service that can only read its secrets at boot has made rotation an outage — build reload in from day one.

## Q zh
怎样轮换数据库密码或 JWT 签名 key 而不重启服务或丢失单个请求？

## A zh
绝不原子翻转 — 用**重叠窗口**轮换两个版本有效：

- **消费秘密**（DB 密码）：新凭证创建*在老的旁* （两用户或双密码方案），让客户端热重载（监视秘密挂载 / 认证失败时重获取 / 强制重获取的短 Vault 租约），仅在遥测显示零使用后撤销老。
- **签名 key**：在 JWKS 发布老 + 新公钥带 `kid`；**用新签名，用两个验证**直到老 key 签署的每个 token 过期，然后丢弃。

设计规则：只能启动时读秘密的任何服务使轮换成故障 — 从第一天构建重载。
