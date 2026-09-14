---
id: security-poisoning-normalization
node: security-cost.poisoning
type: qa
---
## Q
The CDN normalizes `%2F` differently from the origin router. Why is this more than a cache-hit-ratio issue?

## A
Two raw requests can collapse to one cache key while the origin selects different resources, or one origin resource can appear under multiple security policies. That disagreement enables key confusion, poisoning, and authorization bypass. Define one canonicalization contract for path, query, host, duplicate fields, and percent encoding; reject ambiguous forms and test the same corpus at every parser boundary.

## Q zh
CDN 与 origin router 对 `%2F` 的 normalization 不同。为什么这不只是 cache-hit-ratio 问题？

## A zh
两个 raw request 可能 collapse 到同一个 cache key，但 origin 却选择不同 resource；或者同一个 origin resource 可能出现在不同 security policy 下。这种不一致会导致 key confusion、poisoning 和 authorization bypass。应为 path、query、host、duplicate field 与 percent encoding 定义统一 canonicalization contract，reject ambiguous form，并在每个 parser boundary 用同一 corpus 测试。
