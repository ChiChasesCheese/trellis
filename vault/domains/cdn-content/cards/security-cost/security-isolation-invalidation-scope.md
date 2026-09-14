---
id: security-isolation-invalidation-scope
node: security-cost.isolation
type: qa
---
## Q
A tenant updates its private document. What must the invalidation design guarantee besides freshness?

## A
The purge identifier and authorization must be scoped to that tenant and representation namespace, so one tenant cannot evict or enumerate another's keys. Propagate invalidation to every tier that can serve the object, but avoid logging raw private paths or signed tokens. Verify with cross-tenant negative tests: update A, then prove B's content and availability are unchanged.

## Q zh
一个 tenant 更新 private document。除了 freshness，invalidation design 还必须保证什么？

## A zh
purge identifier 和 authorization 必须限定在该 tenant 与 representation namespace 内，防止一个 tenant evict 或 enumerate 另一个 tenant 的 key。把 invalidation 传播到所有可能返回该 object 的 tier，但不要记录 raw private path 或 signed token。用 cross-tenant negative test 验证：更新 A 后，证明 B 的 content 和 availability 不变。
