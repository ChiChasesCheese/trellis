---
nodes: [async.delivery.exactly-once]
url: https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
tags: [canonical]
---
# Exactly-once Semantics is Possible: Here's How Apache Kafka Does it (Neha Narkhede)

The engineering long-form behind Kafka's EOS, by one of Kafka's creators. It is
the concrete answer to the "exactly-once is impossible" argument: not a delivery
guarantee, but a composition of an idempotent producer, atomic multi-partition
writes, and offsets committed inside the same transaction.

**Extract on read:**
- Idempotent producer = PID + monotonic sequence number per partition, so broker-side dedup kills retry duplicates.
- Transactions make "consume → process → produce → commit offset" one atomic unit via the transaction coordinator and markers.
- `read_committed` consumers and why EOS only holds inside Kafka — the moment you write to an external sink you are back to idempotence.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)

## Archived copy
![[confluent-exactly-once-kafka-clip]]
%% trellis:end %%
