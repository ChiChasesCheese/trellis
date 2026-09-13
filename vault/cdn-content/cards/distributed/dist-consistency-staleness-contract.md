---
id: dist-consistency-staleness-contract
node: distributed.consistency
type: qa
---
## Q
Product updates replicate asynchronously across regions. What must the API promise instead of saying merely “eventually consistent”?

## A
Define an observable staleness contract: which operations require read-after-write, the maximum acceptable propagation lag for public reads, whether sessions need monotonic reads, and what happens during partitions. Carry a version/generation so clients and caches can reject older data when necessary. “Eventually” has no deadline and cannot drive alerts, rollback, or product behavior.

## Q zh
product update 在 region 间异步 replication。API 不应只说 “eventually consistent”，而必须承诺什么？

## A zh
定义可观察的 staleness contract：哪些操作需要 read-after-write、public read 可接受的最大 propagation lag、session 是否需要 monotonic read，以及 partition 时的行为。携带 version/generation，使 client 和 cache 在必要时拒绝更旧数据。“Eventually” 没有 deadline，无法驱动 alert、rollback 或 product behavior。
