---
id: reliability-metric-cardinality
node: reliability.observability
type: qa
---
## Q
An engineer adds `user_id` as a label on a request-latency metric. Why does this melt the metrics system, and where does that data belong instead?

## A
Time-series stores keep **one series per unique label combination**. An unbounded label (user id, request id, URL with ids) multiplies cardinality into millions of series — memory, ingest, and query cost all scale with series count, not sample count.

Rule: metric labels must be **low-cardinality and bounded** (endpoint, status class, region). Per-user/per-request detail belongs in **structured logs or trace attributes**, which are built for high-cardinality search.

## Q zh
工程师在请求延迟指标上添加`user_id`作为标签。为什么这熔化了指标系统，那个数据属于哪里？

## A zh
时间序列存储为每个唯一标签组合保持**一个序列**。无界标签（用户 id、请求 id、带 id 的 URL）乘以基数为数百万个序列——内存、摄入和查询成本都按序列数缩放，不是样本数。

规则：指标标签必须是**低基数且有界**（端点、状态类、区域）。每用户/每请求细节属于**结构化日志或跟踪属性**，这是为高基数搜索构建的。
