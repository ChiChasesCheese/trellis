---
id: hi-c-sd-change-data-capture-n05-derived-index
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 5
---
## Q
**变更数据捕获 · 保持派生索引同步**｜摘要 · 必会

为什么搜索索引是 CDC 的理想用例？它出问题时怎么恢复？

## A
- **为什么合适：** Elasticsearch 不是真相来源，只是 Postgres 内容的可搜索投影。
- **允许滞后：** 价格变更晚一两秒出现在搜索里没关系，Postgres 全程是正确的。
- **自愈：** 索引损坏或严重偏差，就删掉，从 Postgres 重建，再接着处理新变更。
- **架构：** Postgres → CDC → Kafka → 索引服务写入 Elasticsearch。
- **推论：** 只要下游只关心状态，写两遍相同的最终状态也无害（幂等），CDC 的至少一次投递就够用。
