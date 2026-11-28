---
id: hi-c-sd-elasticsearch-x08-es-or-db
node: sd.deep-dives.elasticsearch.exam
type: qa
step: 8
---
## Q
**Elasticsearch · 5 万条与 5 亿条商品，各用什么搜**｜考点 · 必会

两个场景：A 小店 5 万个商品，关键词搜索，每天更新几十次；B 平台 5 亿个商品，要拼写容错、相关性排序、按品牌和价格分面。分别选 Postgres 全文检索还是 Elasticsearch？理由？

## A
- **A：** Postgres 的全文索引（GIN）就够了：数据量不到约 10 万，没有额外的同步组件，运维简单，数据一致。先试 `ILIKE` 或 `tsvector`，不够再换。
- **B：** Elasticsearch。需要分片水平扩展、模糊搜索、相关性打分、聚合做分面，这些正是它擅长的。代价是要通过 CDC 同步、承担最终一致，并运维一套集群。
- **判断依据：** 数据规模、检索复杂度、对一致性的要求、愿意承担的运维成本。
- **加分：** 不要一开始就说"用 Elasticsearch"，而是先说简单方案及升级信号。
