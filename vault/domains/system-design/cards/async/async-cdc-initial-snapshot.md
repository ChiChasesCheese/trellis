---
id: async-cdc-initial-snapshot
node: async.streaming.cdc
type: qa
---
## Q
You turn on CDC for a table that already has 500M rows. How do you get the existing data plus ongoing changes without loss or inconsistency?

## A
**Snapshot + WAL handoff**: record the current log position (LSN/GTID), read a consistent snapshot of the table, then stream the WAL **from the recorded position**. Rows changed during the snapshot appear twice (snapshot version, then change event) — safe because CDC consumers must be idempotent upserters anyway.

Naive alternatives fail: WAL-only misses all pre-existing rows; dump-then-tail-from-"now" loses changes made during the dump.

At 500M rows a blocking snapshot is impractical — modern connectors (Debezium) do **incremental snapshots**: chunked key-range reads interleaved with live streaming, deduplicated via watermarks, resumable mid-way.

## Q zh
你为一个已有 500M 行数据的表开启 CDC。如何获得现有数据和持续变化，同时避免数据丢失或不一致？

## A zh
**快照 + WAL 交接**：记录当前日志位置（LSN/GTID），读取表的一致性快照，然后从记录的位置开始 stream WAL。快照期间修改过的行会出现两次（快照版本，然后是变更事件）— 这是安全的，因为 CDC consumer 必须是幂等的 upsert 操作。

朴素的替代方案都失败了：只使用 WAL 会错过所有已存在的行；dump 之后再从"现在"开始追尾会丢失 dump 期间发生的变化。

在 500M 行的情况下，阻塞式快照不实用 — 现代连接器（Debezium）使用**增量快照**：分块的 key-range 读取与实时流互相交错，通过 watermark 去重，可以从中途恢复。
