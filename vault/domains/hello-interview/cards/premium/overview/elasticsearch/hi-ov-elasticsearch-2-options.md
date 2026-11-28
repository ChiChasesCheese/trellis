---
id: hi-ov-elasticsearch-2-options
node: sd.deep-dives.elasticsearch
type: qa
step: 2
tags: [通览]
---
## Q
**Elasticsearch · 能力一览**｜通览

Elasticsearch 有哪些核心能力和机制？各用来做什么，要注意什么？

## A
**13 项能力。**
- **映射：** 定字段类型，text 分词、keyword 整值；决定能搜什么；多余字段占内存。
- **查询：** match、bool、nested；全文与过滤；结果按 _score 排。
- **版本检查更新：** if_seq_no 加 if_primary_term；防并发覆盖；冲突要重试。
- **地理搜索：** geo_point 与 geo_shape，BKD 树；附近与区域；要声明类型。
- **三种分页：** from/size，search_after，PIT 游标；翻页；深页贵，search_after 只能向前。
- **节点角色：** 主、数据、协调、摄取；各管一摊；一台可兼多职。
- **分片与副本：** 切数据并拷贝；扩容量与吞吐；协调节点汇总。
- **不可变段：** 写批量成段，后台合并；写快、好缓存；更新贵，要合并。
- **倒排索引：** 词映射到文档；关键词查找；占额外空间。
- **doc values：** 列式存字段；排序与聚合；另占存储。
- **查询规划：** 按统计先取短列表；省时间；靠统计。
- **近实时：** refresh 默认 1 秒；写完稍后可搜；搜索最终一致。
- **同步：** CDC 从主库灌入；保持一致；漂移是常见 bug。

**一句话定位。** 擅长读多的复杂检索；当主库、高频更新或强一致时，换数据库。
