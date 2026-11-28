---
id: hi-c-sd-elasticsearch-n06-update-docs
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 6
---
## Q
**Elasticsearch · 更新文档：覆盖、乐观并发、部分更新**｜摘要 · 必会

整文档 PUT 有什么风险？怎么避免覆盖别人的修改？`_update` 解决什么？

## A
- **整文档 `PUT /books/_doc/<id>`：** 要提供完整文档。风险是并发时，另一个进程同时在改，你会覆盖它的更改。
- **版本检查（乐观并发控制）：** 更新时带上上一次读到的 `if_seq_no` 和 `if_primary_term`（写入响应里就有），只有文档没被改过才更新，否则返回版本冲突，客户端可以处理冲突并重试。
- **`POST /books/_update/<id>`：** 只传要改的字段（`{"doc": {"price": 14.99}}`），不必先取回整个文档。Elasticsearch 是分布式、异步、并发的，请求可能发往多个节点、乱序到达，显式指定更新语义才能保证行为符合预期。
- **面试用处：** 这些机制是 API 设计题可以借鉴的写法。
