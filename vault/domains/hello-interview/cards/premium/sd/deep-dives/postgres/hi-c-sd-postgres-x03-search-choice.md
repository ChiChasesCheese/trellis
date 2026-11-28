---
id: hi-c-sd-postgres-x03-search-choice
node: sd.deep-dives.postgres.exam
type: qa
step: 3
---
## Q
**PostgreSQL · 搜索：PostgreSQL 还是 Elasticsearch**｜考点 · 必会

一个博客平台有 800 万篇文章，需求 A：关键词搜索加按相关度排序；需求 B：输入错别字也能命中、按作者和标签做分面统计、一边输入一边出提示。分别用什么？

## A
- **A：PostgreSQL 内置全文搜索。** 800 万在"数千万文档"内表现良好；给 `tsvector` 列建 GIN 索引，支持词干、排序、多语言；数据和事务在同一个库里，没有同步问题。
- **B：Elasticsearch。** 模糊匹配、分面搜索、边输入边搜索是它的强项，PostgreSQL 内置能力不足。
- **引入的代价：** 需要把数据同步到搜索引擎，两边会短暂不一致，要运维一个集群。
- **原则：** 先内置、再外置，出现具体无法满足的需求才加组件。
