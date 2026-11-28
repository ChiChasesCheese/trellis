---
id: hi-c-sd-proximity-search-x08-es-moving
node: sd.deep-dives.proximity-search.exam
type: qa
step: 9
---
## Q
**邻近搜索 · 用 Elasticsearch 存实时司机位置**｜考点 · 追问

有人建议把司机位置存到 Elasticsearch 的 geo_point 字段，每个司机每 4 秒更新。这样合适吗？

## A
- **底层：** Elasticsearch 的地理字段用 BKD 树，段文件基本是写一次不再修改。
- **更新的实际代价：** 更新一个文档等于标记旧文档删除、写入新文档，进入新的段，之后还要靠段合并才能回收；大量位置更新带来持续的段创建与合并，写放大严重。
- **规模：** 100 万司机 / 4 秒 = 25 万次更新每秒，远超合适范围；搜索可见性还有刷新延迟（默认约 1 秒）。
- **更合适：** 司机的实时位置放内存键值存储（Redis geo 或 H3 格子索引），Elasticsearch 用来存相对静态的数据，如商家、地点。
- **例外：** 位置变化很少、数据量不大时可以用。
