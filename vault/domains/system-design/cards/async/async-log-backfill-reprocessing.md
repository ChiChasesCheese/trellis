---
id: async-log-backfill-reprocessing
node: async.log
type: qa
---
## Q
You need to rebuild a derived store by reprocessing 90 days of a Kafka topic. What makes this operationally safe, and what two limits do you hit?

## A
Start a **new consumer group** at the earliest offset (or a timestamp via offset-for-time lookup) — offsets are per-group, so production consumers are untouched, and the rebuild writes to a *new* target that you cut over atomically ([[async-materialized-view-refresh]]).

Limits:
- **Retention**: the data must still exist — long replay windows are why **tiered storage** (old segments offloaded to object storage) matters; replay reads then pull from S3, slower but without bloating broker disks.
- **Read throughput**: a backfill can saturate broker I/O and page caches used by live consumers — throttle it (quotas) or read from tiered/offloaded segments.

Also ensure historical events are still *decodable*: schema-registry compatibility is what makes 90-day-old bytes readable by today's code.

## Q zh
你需要通过重处理 Kafka topic 的 90 天数据来重建一个派生存储。什么使这在操作上是安全的，你会遇到什么两个限制？

## A zh
启动**一个新 consumer group**，从最早的 offset（或通过 offset-for-time 查询的时间戳）— offset 是 per-group 的，所以生产 consumer 不受影响，重建写入一个*新*目标，你可以原子性地切换。

限制：
- **保留**：数据必须仍然存在 — 长重放窗口是为什么 **tiered storage**（旧 segment 卸载到对象存储）重要的；重放读然后从 S3 拉取，更慢但不会膨胀 broker 磁盘。
- **读吞吐量**：回填可能饱和 broker I/O 和被实时 consumer 使用的页面缓存 — 限制它（quota）或从分层/卸载 segment 读取。

同时确保历史事件仍然是*可解码的*：schema-registry 兼容性是使 90 天前的字节被今天的代码读取的原因。
