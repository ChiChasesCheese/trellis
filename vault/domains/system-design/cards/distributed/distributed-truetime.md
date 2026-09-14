---
id: distributed-truetime
node: distributed.time.clocks
type: cloze
---
Spanner's TrueTime API returns not a timestamp but {{c1::an interval [earliest, latest] bounding the true time (uncertainty from GPS/atomic clock sync, typically a few ms)}}. To make timestamp order match real-time order, a transaction {{c2::commit-waits: holds its result until `latest` of its commit interval has passed}}, guaranteeing every later-starting transaction gets a strictly greater timestamp — this is how Spanner achieves external consistency (strict serializability) across datacenters, paying clock uncertainty as write latency.

## zh
Spanner 的 TrueTime API 返回的不是一个时间戳，而是{{c1::一个区间 [earliest, latest]，把真实时间限制在里面（不确定性来自 GPS/原子钟同步，通常是几毫秒）}}。为了让时间戳的顺序和真实时间的顺序一致，一个事务会{{c2::commit-wait：一直扣住自己的结果，直到它提交区间的 `latest` 那个时刻已经过去}}，这保证了任何更晚开始的事务都会拿到严格更大的时间戳——这正是 Spanner 能在跨数据中心的场景下实现外部一致性（严格可串行化）的方式，代价是把时钟的不确定性变成了写延迟。
