---
id: hi-c-sd-key-technologies-b02-search-sync
node: sd.in-a-hurry.key-technologies.beyond
type: qa
step: 2
---
## Q
**关键技术 · 搜索索引与主库怎么保持同步**｜拓展 · 加分

商品数据在 Postgres，搜索走 Elasticsearch。怎么让索引跟上主库？为什么不建议双写？

## A
- **索引只是派生数据：** 主库是事实来源（source of truth），搜索索引可以丢了重建。
- **双写的问题：** 应用先写库再写索引，中间一步失败或两个请求交错，两边就不一致，且无人察觉。
- **更稳的做法：** 用变更数据捕获（CDC，读数据库日志把变更变成事件流）或事务性发件箱（outbox），把变更发到队列 / 流，再由消费者幂等地更新索引；消费者崩了可以重放。
- **取舍：** 索引相对主库有延迟（最终一致）；Elasticsearch 写入后默认约 1 秒才对搜索可见（refresh 间隔），所以"刚发的帖子搜不到"是预期行为，要在需求里说明可接受的延迟。
