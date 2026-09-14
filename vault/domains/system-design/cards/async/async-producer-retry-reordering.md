---
id: async-producer-retry-reordering
node: async.delivery.exactly-once
type: cloze
---
A Kafka producer with retries enabled and multiple in-flight batches can silently {{c1::reorder writes within a partition}} — batch 1 fails and is retried *after* batch 2 already landed. The fix is the {{c2::idempotent producer}}, whose per-partition sequence numbers let the broker reject out-of-sequence batches, preserving order with up to {{c3::5}} in-flight requests; the old folklore fix of `max.in.flight=1` traded away throughput for the same guarantee.

## zh
启用了重试和多个在途批次的 Kafka 生产者可能无声地 {{c1::重新排序 partition 内的写入}} — batch 1 失败并在 batch 2 已经落地*之后*被重试。修复是 {{c2::幂等生产者}}，其 per-partition 序列号让 broker 拒绝序列号不正确的批次，通过最多 {{c3::5}} 个在途请求保持顺序；旧的民间修复 `max.in.flight=1` 为了相同的保证而牺牲吞吐量。
