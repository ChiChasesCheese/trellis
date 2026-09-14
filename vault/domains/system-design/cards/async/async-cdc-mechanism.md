---
id: async-cdc-mechanism
node: async.streaming.cdc
type: qa
---
## Q
How does log-based CDC (e.g. Debezium) capture changes, and why is it preferred over the application publishing events itself or polling the table?

## A
It **tails the database's replication log** (WAL/binlog) and emits every committed row change, in commit order per key, into a stream.

- vs **app publishes**: CDC can't miss or invent events — it sees exactly what committed, even writes from other code paths, migrations, or manual fixes.
- vs **polling**: no missed intermediate states, no `updated_at` race, deletes are captured, and latency is sub-second instead of poll-interval.

Cost: events are row-level and schema-shaped, not intent-shaped — you often re-derive domain meaning downstream (or use the outbox pattern for intent events).

## Q zh
基于日志的 CDC（例如 Debezium）如何捕获变化，为什么相比应用自己发布事件或轮询表更好？

## A zh
它**追尾数据库的复制日志**（WAL/binlog），将每个已提交的行变化按 key 的提交顺序发出到流中。

- vs **应用发布**：CDC 不会错过或发明事件 — 它看到的是确切的已提交内容，包括其他代码路径、数据迁移或手工修复的写入。
- vs **轮询**：不会错过中间状态、没有 `updated_at` race、删除被捕获、延迟是亚秒级而不是轮询间隔。

代价是事件是行级别的、按数据库 schema 形成，而不是按意图形成 — 你通常需要在下游重新推导领域含义（或使用 outbox 模式获得意图事件）。
