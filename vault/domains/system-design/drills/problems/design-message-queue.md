---
nodes: [problems.foundations.message-queue, async.log, async.delivery.guarantees]
tags: [problem]
---
# Drill: Design a distributed message queue like Apache Kafka

Design a Kafka-class distributed message queue as shared infrastructure: an unbounded
number of producers write to named topics, an unbounded number of independent consumer
groups each read the same data at their own pace and can replay from any historical
offset, and the system must survive individual broker failures without losing committed
data. Size the design for a clickstream topic with 300M DAU producing 200 events/user/day.

**Constraints to state and honor**
- Peak write QPS ~2,777,778 messages/sec (400-byte messages, 4x average); 7-day
  retention; replication factor 3 (504TB storage for this one topic).
- Ordering is guaranteed only within a single partition, never globally.
- The largest downstream consumer group needs up to ~600 parallel consumer instances
  at peak.
- Default delivery semantics are at-least-once; the design must support upgrading to
  idempotent/effectively-once producer behavior without changing the wire protocol.

**Grading points**
- Sizes partition count from two independent lower bounds -- write throughput and the
  largest consumer group's parallelism -- and takes the larger, explaining why
  repartitioning later breaks a key's prior ordering guarantee
  ([[problems-message-queue-partition-count-two-lower-bounds]]).
- Chooses a pull-based consumer model over broker push and explains why this makes
  backpressure inherent to the protocol rather than a bolted-on mechanism
  ([[problems-message-queue-pull-based-consumer-model]], [[async-queue-backpressure]]).
- Uses an ISR (in-sync replicas) replication model instead of majority quorum, and can
  state why it needs only f+1 replicas for f-failure tolerance instead of 2f+1, plus the
  min.insync.replicas / unclean-leader-election trade-off when the ISR shrinks
  ([[problems-message-queue-isr-quorum-f-plus-1-tradeoff]]).
- Explains why a consumer falling behind the page-cache-covered window degrades not just
  its own read latency but write latency for every producer on that broker, by competing
  for the same disk I/O as the leader's sequential writes
  ([[problems-message-queue-page-cache-consumer-lag-cliff]]).
- Contrasts eager (stop-the-world) consumer group rebalancing with incremental
  cooperative rebalancing, and can cite the concrete stabilization-time and throughput
  gap between them ([[problems-message-queue-cooperative-rebalancing-stabilization]],
  [[async-rebalancing-protocols]]).
- Distinguishes log compaction from time/size-based retention and picks the right one
  per topic use case -- event stream vs authoritative latest-state store
  ([[problems-message-queue-log-compaction-vs-time-retention]], [[async-log-compaction]]).
- Diagnoses a hot-partition scenario caused by key skew and explains why adding more
  partitions does not fix it, only re-routing the hot key does
  ([[problems-message-queue-hot-partition-key-skew]]).
- States a concrete 10x evolution path (tiered storage) when broker-local storage
  capacity becomes the binding constraint, and can contrast it with a
  storage/serving-separated architecture like Pulsar/BookKeeper
  ([[problems-message-queue-tiered-storage-10x-evolution]]).
- Distinguishes at-least-once (the default), idempotent producer dedup, and end-to-end
  exactly-once, and states which one is a property of this queue alone versus a
  composition with the downstream sink ([[async-delivery-semantics-cloze]],
  [[async-exactly-once-myth]]).

**Solution**: [[solution-message-queue]] -- attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
