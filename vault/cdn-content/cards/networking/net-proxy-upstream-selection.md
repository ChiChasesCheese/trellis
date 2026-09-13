---
id: net-proxy-upstream-selection
node: networking.proxies
type: qa
---
## Q
An edge randomly routes every miss across all origins. Why can that hurt both latency and availability?

## A
Random routing ignores region distance, health, capacity, cache/storage locality, and failure domains. Select from healthy eligible upstreams using latency/capacity-aware policy, bound per-upstream concurrency, and fail over only within a deadline. Keep routing metadata observable; otherwise retries can repeatedly hit the same degraded dependency or overload the surviving region.

## Q zh
edge 把每个 miss 随机路由到所有 origin。为什么这会同时损害 latency 与 availability？

## A zh
random routing 忽略 region distance、health、capacity、cache/storage locality 与 failure domain。应从健康且 eligible 的 upstream 中按 latency/capacity-aware policy 选择，限制 per-upstream concurrency，并只在 deadline 内 failover。routing metadata 必须可观测，否则 retry 可能反复命中同一 degraded dependency，或压垮 surviving region。
