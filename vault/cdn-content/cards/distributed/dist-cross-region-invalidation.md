---
id: dist-cross-region-invalidation
node: distributed.cross-region
type: qa
---
## Q
A purge message is lost during a regional partition. How should the region converge after reconnecting?

## A
Do not rely solely on ephemeral broadcast. Persist purge generations or an append-only invalidation log, let each region checkpoint its position, and replay missed entries after reconnect. Cache reads compare artifact generation against durable tag/path state so a delayed delete cannot resurrect stale content. Monitor consumer lag and support snapshot repair when the retained log no longer covers the gap.

## Q zh
regional partition 期间一条 purge message 丢失。region 重连后应如何 converge？

## A zh
不能只依赖 ephemeral broadcast。持久化 purge generation 或 append-only invalidation log，让每个 region checkpoint position，重连后 replay 漏掉的 entry。cache read 比较 artifact generation 与 durable tag/path state，使 delayed delete 不能复活 stale content。监控 consumer lag；当 retained log 已无法覆盖 gap 时，支持 snapshot repair。
