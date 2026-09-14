---
id: async-log-throughput-design
node: async.log
type: qa
---
## Q
A single Kafka broker on spinning disks can move hundreds of MB/s — and a consumer replaying three days of backlog barely disturbs live traffic. Which design choices make the log this fast on cheap hardware?

## A
- **Sequential I/O only**: producers append to the tail of the active segment; consumers read contiguous runs. No random seeks, no per-message B-tree/index updates — the access pattern is the one disks (and SSDs) are best at.
- **The OS page cache is the cache**: recent segments sit in kernel memory, so tail-reading consumers are served from RAM; the broker keeps little heap state and restarts warm.
- **Zero-copy handoff**: `sendfile()` ships bytes page-cache → NIC without copying through user space — the broker never even parses message payloads on the read path.
- **Batching end to end**: producers send compressed record batches; the broker stores the batch as-is; consumers fetch in large chunks — amortizing syscalls, network round trips, and compression.
- **Dumb broker, cheap consumers**: no per-message delivery state or ack bookkeeping — a consumer is just an offset, so lagging or replaying consumers cost sequential reads, not broker bookkeeping.

Contrast: a broker doing per-message acks, redelivery tracking, and random-access deletes (classic queue) pays index writes per message — which is why logs win on raw throughput.

## Q zh
一台跑在机械磁盘上的 Kafka broker 能搬运每秒几百 MB——一个回放三天积压的消费者也几乎不干扰实时流量。哪些设计选择让 log 在廉价硬件上跑得这么快？

## A zh
- **只做顺序 I/O**：生产者追加到活跃 segment 的尾部；消费者读连续区段。没有随机寻道，没有每条消息的 B-tree/索引更新——这正是磁盘（和 SSD）最擅长的访问模式。
- **操作系统 page cache 就是缓存**：最近的 segment 驻留在内核内存里，追尾读的消费者直接从 RAM 拿数据；broker 自身几乎不持有堆内状态，重启后缓存还是热的。
- **零拷贝（zero-copy）交接**：`sendfile()` 把字节从 page cache 直送网卡，不经过用户态拷贝——读路径上 broker 甚至不解析消息体。
- **端到端批处理**：生产者发送压缩的记录批；broker 原样存储整批；消费者大块拉取——把系统调用、网络往返和压缩的成本摊薄。
- **笨 broker、廉价消费者**：没有每条消息的投递状态或 ack 簿记——一个消费者只是一个 offset，所以滞后或回放的消费者花的是顺序读，不是 broker 的记账开销。

对比：做每条消息 ack、重投递跟踪和随机删除的 broker（经典队列）要为每条消息付索引写——这就是 log 在裸吞吐上取胜的原因。
