---
id: security-abuse-key-amplification
node: security-cost.abuse
type: qa
---
## Q
An attacker varies meaningless query parameters to force unlimited cache misses and object creation. What controls stop this amplification?

## A
Allowlist only representation-changing query fields in the canonical key, normalize bounded values, and reject or ignore the rest. Add admission policy, per-tenant unique-key quotas, miss/concurrency limits, object-size caps, and origin protection. Monitor key cardinality and bytes admitted, not only request rate; one request can create an expensive persistent object.

## Q zh
attacker 改变无意义 query parameter，制造无限 cache miss 和 object creation。哪些 control 能阻止这种 amplification？

## A zh
在 canonical key 中只 allowlist 会改变 representation 的 query field，对 bounded value 做 normalization，并 reject 或 ignore 其他 field。增加 admission policy、per-tenant unique-key quota、miss/concurrency limit、object-size cap 和 origin protection。监控 key cardinality 与 admitted byte，而不只是 request rate；一个 request 就可能创建昂贵且持久的 object。
