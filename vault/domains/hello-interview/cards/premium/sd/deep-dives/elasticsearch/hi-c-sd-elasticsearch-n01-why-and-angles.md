---
id: hi-c-sd-elasticsearch-n01-why-and-angles
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 1
---
## Q
**Elasticsearch · 什么时候需要专用搜索引擎，要从哪两个角度学**｜摘要 · 必会

数据库已经能做全文检索时，为什么还要 Elasticsearch？面试里该从哪两个角度准备它？

## A
- **什么时候：** 数据库（如带全文索引的 Postgres）能解决很多检索问题；当规模或复杂度上去，要排序、过滤、相关性排名、分面（faceting，统计各类别的数量）这类组合需求时，才请出专用系统。Elasticsearch 是最有名的搜索引擎，几乎没有它搞不定的检索类题目。
- **角度一，怎么用：** 创业公司或偏产品架构的面试里，会用就是一件趁手的工具。用过的人可以跳过。
- **角度二，底层怎么工作：** 它是分布式系统工程的集大成者，里面的思想在搜索之外也能用。有的面试官会让你假装没有 Elasticsearch，自己讲出顶层概念，基础设施偏重的岗位（尤其云公司）更常见。
