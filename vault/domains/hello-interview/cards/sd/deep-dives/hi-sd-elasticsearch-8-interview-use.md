---
id: hi-sd-elasticsearch-8-interview-use
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 8
---
## Q
**面试里怎样用 Elasticsearch 与它的边界**｜系统设计 · 深入技术

面试中引入 Elasticsearch 时通常怎样接入？有哪些必须说明的限制，什么时候根本不需要它？

## A
**接法。** 通常用变更数据捕获（CDC）把权威数据库（Postgres、DynamoDB）的变更同步到 Elasticsearch。

**限制。**
- 别当主数据库：它首先是搜索引擎，早期版本在一致性和持久性上有问题，需要持久化的数据放别处
- 为读多设计：写多就考虑缓冲；把点赞数、曝光数这类高频变化字段放进去会让它吃力
- 最终一致：结果可能陈旧，容忍不了就换方案
- 不是关系库：尽量反规范化，让结果由 1 到 2 次查询得到
- 要保证与源数据同步，漂移是常见 bug 来源

**不需要。** 文档少于约 10 万或变化少时，主库直接查询（如 Postgres 全文索引）往往足够，先证明不够再上。
