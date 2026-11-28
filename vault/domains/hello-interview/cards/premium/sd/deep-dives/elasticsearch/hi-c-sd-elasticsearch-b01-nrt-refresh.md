---
id: hi-c-sd-elasticsearch-b01-nrt-refresh
node: sd.deep-dives.elasticsearch.beyond
type: qa
step: 1
---
## Q
**Elasticsearch · 为什么写入后不是立刻可搜：refresh、flush、translog**｜拓展 · 加分

写入一个文档后多久可见？崩溃了会不会丢？

## A
- **近实时（near real-time）：** 新文档先进内存缓冲，同时记入事务日志（translog）。要等到 refresh 才生成可搜索的新段，默认每 1 秒一次（`refresh_interval`），所以"写完立刻搜不到"是预期行为。
- **flush：** 把内存里的数据真正落盘提交为 Lucene 的持久提交点，并清理 translog。
- **持久性：** 默认每个写请求都会 fsync translog（`index.translog.durability: request`），崩溃后可重放；改成异步 fsync 更快，但可能丢最近几秒。
- **批量导入时：** 常把 `refresh_interval` 调大甚至关闭，写完再手动刷新，换取吞吐。
- **面试用处：** 回答"为什么搜不到刚写的数据"，以及"搜索是最终一致"的具体来源。
