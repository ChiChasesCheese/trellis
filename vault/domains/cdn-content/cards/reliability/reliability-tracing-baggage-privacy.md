---
id: reliability-tracing-baggage-privacy
node: reliability.tracing
type: qa
---
## Q
An engineer wants to put full URL, tenant name, and cache key into OpenTelemetry baggage so every downstream span can use them. What is wrong with this plan?

## A
Baggage propagates across process boundaries and can become both a privacy leak and per-request bandwidth/cardinality tax. Propagate only small, allowlisted routing context that downstream logic truly needs. Put diagnostic attributes on the relevant span, hash or classify sensitive values, and enforce size limits at ingress.

## Q zh
一位工程师想把完整 URL、tenant name 和 cache key 放进 OpenTelemetry baggage，让每个 downstream span 都能使用。这个方案有什么问题？

## A zh
baggage 会跨 process boundary 传播，可能同时造成 privacy leak，以及每个 request 的 bandwidth/cardinality tax。只传播 downstream logic 真正需要的、很小且 allowlisted 的 routing context。把 diagnostic attribute 放在相关 span 上，对 sensitive value 做 hash 或 classification，并在 ingress 强制 size limit。
