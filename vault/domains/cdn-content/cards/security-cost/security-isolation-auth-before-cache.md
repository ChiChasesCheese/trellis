---
id: security-isolation-auth-before-cache
node: security-cost.isolation
type: qa
---
## Q
A cache key includes `tenant_id`, so an engineer proposes looking up the cache before verifying the caller belongs to that tenant. Is the order safe?

## A
No. A user-controlled tenant identifier is routing input, not authorization proof. Authenticate and authorize the canonical tenant scope before constructing or reading the private cache partition, then derive the key from trusted identity. Otherwise an attacker can request another tenant's key even though entries are perfectly partitioned.

## Q zh
cache key 包含 `tenant_id`，因此一位工程师建议在验证 caller 是否属于该 tenant 前先查 cache。这个顺序安全吗？

## A zh
不安全。user-controlled tenant identifier 只是 routing input，不是 authorization proof。必须先根据 canonical tenant scope 完成 authenticate 和 authorize，再构造或读取 private cache partition，并从 trusted identity 派生 key。否则即使 entry 完美 partition，attacker 仍可请求另一个 tenant 的 key。
