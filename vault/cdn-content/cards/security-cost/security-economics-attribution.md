---
id: security-economics-attribution
node: security-cost.economics
type: qa
---
## Q
How should a multi-tenant CDN attribute cost without putting tenant ID on every Prometheus metric?

## A
Keep operational metrics low-cardinality, then emit sampled or aggregated usage records keyed by authenticated tenant into a billing/analytics pipeline. Reconcile totals with provider bills and preserve dimensions such as region, bytes, requests, transform class, and cache outcome. Cost allocation needs auditable records, but the real-time monitoring path should not carry unbounded tenant cardinality.

## Q zh
multi-tenant CDN 如何归因 cost，同时避免把 tenant ID 放到每个 Prometheus metric 上？

## A zh
保持 operational metric low-cardinality，再把按 authenticated tenant 聚合或 sampled 的 usage record 发送到 billing/analytics pipeline。将总量与 provider bill reconcile，并保留 region、byte、request、transform class 和 cache outcome 等 dimension。cost allocation 需要可审计 record，但 real-time monitoring path 不应承载 unbounded tenant cardinality。
