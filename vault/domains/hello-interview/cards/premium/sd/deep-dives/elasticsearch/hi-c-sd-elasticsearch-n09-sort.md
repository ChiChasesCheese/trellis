---
id: hi-c-sd-elasticsearch-n09-sort
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 9
---
## Q
**Elasticsearch · 排序：字段、脚本、嵌套、相关性**｜摘要 · 必会

怎么排序？默认按什么排？嵌套字段排序要注意什么？

## A
- **基本排序：** `sort` 参数，可多字段，如价格升序再发布日期降序。
- **脚本排序（Painless）：** 按计算出的值排序；例如按八折价排序，结果其实与按原价排序相同，真实使用时没必要。脚本要对每个文档计算，有开销。
- **嵌套字段：** 要用 nested sort 并指定 `path`，保证排序值来自同一个嵌套对象；用 `mode` 选 `max` 等聚合方式，如按最高评论评分排序。
- **相关性：** 不指定排序时按 `_score` 相关性排序，可配置；默认打分算法是 BM25，是 TF-IDF（词频—逆文档频率）的改进版。值得花十分钟了解。
