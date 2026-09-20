---
nodes: [problems.social.tinder]
url: https://medium.com/tinder-engineering/geosharded-recommendations-part-3-consistency-2d2cb2f0594b
---
# Geosharded Recommendations Part 3: Consistency

值得读：系列第三篇讲的是候选人文档跨地理分片迁移时的一致性问题（比如用户切换定位后
要从旧分片移到新分片），这是本题"用户移动后 feed 怎么处理"这一深入探讨的直接依据。
比多数题解文章更具体的地方是给出了两个可落地的机制——用 Kafka 按 key 分区保证同一用户
的多次迁移事件按顺序处理，以及用 Elasticsearch 的 Get API（而非 Reindex API）强制
refresh 后再迁移，避免近实时搜索的 buffer/refresh/flush 语义带来的中间态。
