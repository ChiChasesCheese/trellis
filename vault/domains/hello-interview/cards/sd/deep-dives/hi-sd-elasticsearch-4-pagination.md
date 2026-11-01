---
id: hi-sd-elasticsearch-4-pagination
node: sd.deep-dives.elasticsearch
type: qa
step: 4
---
## Q
**分页：from/size、search_after 与 PIT**｜系统设计 · 深入技术

Elasticsearch 的三种分页方式分别是什么？深分页为什么慢，如何保证翻页过程中视图一致？

## A
**from/size。** 最简单，但深分页（超过约 1 万条）很贵：每次请求集群都要取回并排序前面所有文档。

**search_after。** 用上一页最后一条的排序值当边界，只取排在其后的，不用收集再跳过前面的页。只能向前翻，客户端要保存最后一条的排序值，且需要含 `_id` 这类唯一字段当平局决胜。它只是书签，不是磁盘地址。

**PIT 游标。** 翻页期间有文档增删改，结果可能漏掉或重复。把 PIT（point in time）与 search_after 配合：先建 PIT 得到 id，翻页都带上它，结束时关闭，视图一致，代价是额外开销。
