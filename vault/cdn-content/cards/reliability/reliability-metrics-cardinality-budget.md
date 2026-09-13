---
id: reliability-metrics-cardinality-budget
node: reliability.metrics
type: qa
---
## Q
An engineer proposes `request_path`, `user_id`, and full `cache_key` as metric labels to debug misses. What should be kept, and where should the high-cardinality context go?

## A
Keep bounded labels needed for aggregation, such as region, cache outcome, status class, and route template. Put raw path, user ID, and cache key in sampled structured logs or traces with redaction and access controls. Unbounded labels multiply time series, raise observability cost, and can destabilize the monitoring system during the incident it is meant to explain.

## Q zh
一位工程师建议把 `request_path`、`user_id` 和完整 `cache_key` 作为 metric label 来调试 miss。哪些应该保留，高 cardinality context 应放在哪里？

## A zh
只保留用于 aggregation 的 bounded label，例如 region、cache outcome、status class 和 route template。raw path、user ID 与 cache key 应进入经过 redaction 和 access control 的 sampled structured log 或 trace。unbounded label 会成倍增加 time series、提高 observability cost，并可能在本应解释 incident 时反而让 monitoring system 失稳。
