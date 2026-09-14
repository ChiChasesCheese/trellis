---
id: storage-document-vs-relational
node: storage.nosql
type: qa
---
## Q
When does a document store (MongoDB-style) genuinely beat relational, and what access pattern signals you chose wrong?

## A
Document wins when data is naturally an **aggregate read/written as a unit** — the whole document loads in one op, schema varies per record, and locality beats joins (e.g. a product page, a user profile with embedded settings).

Warning signs you chose wrong: queries that constantly reach **across** documents (many-to-many relationships, cross-entity analytics) — you end up doing joins in application code, or duplicating data and hand-rolling consistency.

Note the gap has narrowed: Postgres `jsonb` covers many "flexible schema" cases inside a relational engine.

## Q zh
文档存储（MongoDB 风格）什么时候真正胜过关系型，什么访问模式信号说明你选错了？

## A zh
当数据自然是一个**聚合体被作为一个单位读写**时文档胜出——整个文档在一次操作加载，schema 按记录变化，局部性胜过 join（例如产品页、带嵌入设置的用户个人资料）。

选错的警告信号：查询不断跨越**文档**（多对多关系、跨实体分析）——你最后在应用代码中做 join，或复制数据并手动滚动一致性。

注意间隙已缩小：Postgres `jsonb` 在关系引擎内覆盖许多"灵活 schema"情况。
