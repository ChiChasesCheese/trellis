You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "async.queues": ["<id shown first>", "…"],
  "async.log": ["<id shown first>", "…"],
  "async.delivery.guarantees": ["<id shown first>", "…"],
  …
}

## async.queues — Message Queues
Queues vs pub-sub, backpressure, consumer scaling, and when async is the wrong call.
- `async-broker-selection` Q: Kafka vs RabbitMQ vs Pulsar: which workload picks which, and why?
  A: - **RabbitMQ (queue semantics)**: task distribution — per-message ack, redelivery to any consumer, routing/priority/delay features, consumer count not tied to p
- `async-competing-consumers-ordering` Q: Why do competing consumers on a classic queue destroy message ordering even though the queue is FIFO — and what are the fixes when per-entity order matters?
  A: FIFO only governs *dispatch*. With N consumers, messages for the same entity run **concurrently** (msg 2 can finish before msg 1), and a nack/redelivery re-enqu
- `async-queue-backpressure` Q: A queue's depth is growing without bound. Why is "the queue absorbs it" not an answer, and what are your options?
  A: An unbounded queue converts an overload failure into a *latency* failure: messages still get processed, but hours late, and the backlog hides that consumers can
- `async-queue-vs-pubsub` Q: When do you choose a work queue (competing consumers) over pub/sub fan-out?
  A: - **Work queue**: each message is a *task* that exactly one consumer should perform (send email, resize image). Consumers compete; adding consumers increases th
- `async-retry-delay-implementation` Q: Your consumer needs retries with backoff (5s, 1m, 10m), but the broker delivers immediately. How is delayed retry actually implemented, and what does it cost you?
  A: - **Kafka**: no native delay — use **tiered retry topics** (`orders-retry-5s`, `-1m`, `-10m`); a failed message is republished to the next tier, whose consumer 
- `async-when-async-is-wrong` Q: Name three signals that making an operation asynchronous (via a queue) is the wrong call.
  A: - The caller **needs the result to proceed** (auth check, price quote, inventory reservation shown to the user) — you'd just rebuild synchronous RPC with extra 

## async.log — The Log & Kafka
The append-only log as system of record; partitions, consumer groups, offsets, retention.
- `async-consumer-groups-offsets` Q: In a Kafka consumer group, when should you commit offsets relative to processing, and what does each choice cost you?
  A: - **Commit after processing** → at-least-once: a crash between process and commit replays messages, so downstream must be idempotent. This is the default correc
- `async-consumer-lag-monitoring` Q: "Consumer lag" is the first metric on any Kafka dashboard. Define it precisely, explain what a steadily growing lag tells you, and give the response options in order.
  A: **Lag = log-end offset (latest produced) − committed consumer offset, summed or maxed per partition.** It measures how far behind reality the consumer's view is
- `async-log-backfill-reprocessing` Q: You need to rebuild a derived store by reprocessing 90 days of a Kafka topic. What makes this operationally safe, and what two limits do you hit?
  A: Start a **new consumer group** at the earliest offset (or a timestamp via offset-for-time lookup) — offsets are per-group, so production consumers are untouched
- `async-log-compaction` Q: How does Kafka log compaction work, what does a compacted topic guarantee, and what is it for?
  A: A background cleaner rewrites old log segments, keeping **only the latest record per key**; a `null` value is a **tombstone** that marks the key for deletion (r
- `async-log-ordering-partitions` Q: What ordering does Kafka actually guarantee, and how do you use that to keep per-entity ordering at scale?
  A: Ordering is guaranteed **only within a partition** — there is no total order across a topic. - Choose the **partition key = entity id** (user id, account id, or
- `async-log-throughput-design` Q: A single Kafka broker on spinning disks can move hundreds of MB/s — and a consumer replaying three days of backlog barely disturbs live traffic. Which design choices make the log this fast on cheap hardware?
  A: - **Sequential I/O only**: producers append to the tail of the active segment; consumers read contiguous runs. No random seeks, no per-message B-tree/index upda
- `async-log-vs-queue` Q: What does an append-only log (Kafka) give you that a traditional broker queue (RabbitMQ/SQS) fundamentally cannot?
  A: **Replay.** A queue deletes messages on ack; the log retains them for a retention window (or forever with compaction), and consumers just track offsets. That en
- `async-rebalancing-protocols` Q: A consumer group of 50 members hiccups every deploy: all consumption stops for seconds. What causes the pause, and what are the modern mitigations?
  A: **Eager rebalancing** is stop-the-world: any membership change makes *every* member revoke *all* partitions, rejoin, and wait for reassignment — a full pause pl

## async.delivery.guarantees — Delivery Guarantees
At-most-once vs at-least-once, ordering scope, dead-letter queues and poison pills.
- `async-delivery-semantics-cloze` Q: Delivery semantics follow from when you ack: acking **before** processing gives {{c1::at-most-once}} (crash loses the message), acking **after** processing gives {{c2::at-least-once}} (crash causes redelivery), and "exactly-once" in practice means {{c3::at-least-once delivery plus idempotent (deduplicating) processing}}.
- `async-dlq-poison-pill` Q: When should a message go to a dead-letter queue, and what two things must you decide about the messages that land there?
  A: Move a message after **N failed attempts with backoff** when the failure is *non-transient* (malformed payload, business rule violation) — retrying a poison pil
- `async-exactly-once-myth` Q: An interviewer asks: "Can a message broker give you exactly-once delivery?" What is the correct senior answer?
  A: No — **exactly-once *delivery* is impossible** over an unreliable network: if the ack is lost, the sender cannot distinguish "processed, ack lost" from "never p
- `async-loss-vs-duplicate-asymmetry` Q: Between at-most-once and at-least-once delivery, production systems overwhelmingly build on at-least-once and engineer away the duplicates. What asymmetry between losing a message and duplicating one justifies that default?
  A: The two failures are not symmetric in **detectability and repairability**: - **A duplicate arrives** — it's an event you can see, carry an id on, and neutralize
- `async-redelivery-causes` Q: Your consumer code is bug-free and the broker is healthy. Name the concrete events that still cause the same message to be processed twice — and the one that means two consumers run it *at the same time*.
  A: - **Ack/offset commit lost** — you processed, then the ack or commit didn't land (crash, network drop, broker leader change). The broker re-delivers. - **Lease 
- `async-stale-event-ordering` Q: Your handler is idempotent and the topic is keyed by entity, yet a profile occasionally reverts to an old address. Why isn't idempotency enough, and what is the fix?
  A: Per-partition ordering only holds for the **stream as stored**, not for the order your handler *observes*. Any of these re-orders events for one key: a failed m

## async.delivery.exactly-once — Effectively Exactly-Once
Idempotent producers, transactional consume-process-produce, and why end-to-end exactly-once is a composition, not a feature.
- `async-eos-boundary-choice` Q: Broker transactions or a transactional outbox? State the rule for choosing, and one place people wrongly assume broker EOS extends.
  A: The rule follows from **where the atomic boundary can physically be** — a transaction only spans one system: - **System of record is the broker** (consume → tra
- `async-eos-sink-determinism` Q: A Flink job runs with exactly-once checkpointing and writes each result to Postgres. What are the only two sink designs that make the end-to-end result exactly-once, and what silently breaks both?
  A: On recovery the job rewinds to the last checkpoint and **re-emits** everything after it, so the sink must absorb the replay: - **Idempotent sink** — an upsert o
- `async-idempotent-producer` Q: Kafka's idempotent producer: what mechanism deduplicates, and which duplicates does it NOT eliminate?
  A: The broker assigns each producer a **producer id (PID)**; the producer stamps every batch with a **per-partition sequence number**. On a retry, the broker sees 
- `async-kafka-transactions-eos` Q: How does Kafka achieve exactly-once for a consume-transform-produce pipeline (Kafka Streams), and where does the guarantee stop?
  A: The producer opens a **transaction** that atomically commits both the **output records** and the **input consumer offsets** (offsets are just writes to an inter
- `async-producer-retry-reordering` Q: A Kafka producer with retries enabled and multiple in-flight batches can silently {{c1::reorder writes within a partition}} — batch 1 fails and is retried *after* batch 2 already landed. The fix is the {{c2::idempotent producer}}, whose per-partition sequence numbers let the broker reject out-of-sequence batches, preserving order with up to {{c3::5}} in-flight requests; the old folklore fix of `max.in.flight=1` traded away throughput for the same guarantee.

## async.streaming.cdc — CDC & Event Sourcing
Change data capture mechanics, initial snapshots, log compaction, and event sourcing as a contrast.
- `async-cdc-initial-snapshot` Q: You turn on CDC for a table that already has 500M rows. How do you get the existing data plus ongoing changes without loss or inconsistency?
  A: **Snapshot + WAL handoff**: record the current log position (LSN/GTID), read a consistent snapshot of the table, then stream the WAL **from the recorded positio
- `async-cdc-mechanism` Q: How does log-based CDC (e.g. Debezium) capture changes, and why is it preferred over the application publishing events itself or polling the table?
  A: It **tails the database's replication log** (WAL/binlog) and emits every committed row change, in commit order per key, into a stream. - vs **app publishes**: C
- `async-command-vs-event` Q: In an event-sourced system, why must "ReserveSeat" (a command) and "SeatReserved" (an event) be different things, and at which exact moment does one become the other?
  A: - A **command** is a *request* that may be rejected: it must be validated against current state (seat still free? balance sufficient?) and represents intent, no
- `async-compacted-topic-bootstrap` Q: Team A bootstraps every new CDC consumer with the snapshot-plus-log-position dance; team B just points new consumers at offset 0 of a compacted changelog topic. What lets team B skip the snapshot, and what two properties must their change events have?
  A: Log compaction keeps **at least the latest record per key** forever, so the compacted topic *is* a full copy of the current dataset plus recent history — readin
- `async-event-sourcing-vs-cdc` Q: Event sourcing and CDC both give you "a stream of changes." What is the fundamental distinction, and when do you pick each?
  A: - **Event sourcing**: domain events (`OrderCancelled`) are the **source of truth**, written first, expressing *intent*; current state is a derived projection. T

## async.streaming.processing — Stream Processing
Event time vs processing time, windows and watermarks, stream joins, and fault-tolerant state.
- `async-event-time-watermarks` Q: In stream processing, why window on event time instead of processing time, and what problem do watermarks solve?
  A: **Processing time** windows depend on when data *arrived* — a delayed producer or a replay shifts events into the wrong window and results become non-reproducib
- `async-late-event-policy` Q: Your streaming job's watermark says the 12:00–12:05 window is complete and its aggregate is emitted — then a mobile client that was in a tunnel uploads three events stamped 12:03. What are your options for these stragglers, and what does each one cost downstream?
  A: Three policies, in increasing order of downstream burden: - **Drop them** (and count them in a metric): the emitted result is final and downstream stays simple 
- `async-materialized-view-refresh` Q: You keep a denormalized read model (search index, cache, analytics table) fed from a change stream. How do you (a) keep it fresh and (b) fix it when it's wrong?
  A: - **Fresh**: a stream consumer applies each change; freshness = consumer lag, which you monitor as *lag age* (seconds behind), not message count. Writes must be
- `async-stream-joins` Q: Stream-stream join vs stream-table join: how does each maintain state, and what goes wrong with each?
  A: - **Stream-stream** (clicks ⋈ impressions): both sides are buffered in a **windowed state store**; each arrival probes the other side's buffer. Failure mode: th
- `async-streaming-state-recovery` Q: A stream job has been running for a month, holding large windowed aggregates in memory, when a worker dies. Restarting from scratch would mean replaying a month of input. How do frameworks like Flink make recovery cheap, and what's special about how a consistent snapshot is taken while the stream keeps flowing?
  A: **Periodic checkpoints of operator state + input positions.** Recovery = restore the last completed checkpoint's state, rewind the source to the offsets recorde
- `async-window-types` Q: The four stream window types: a **tumbling** window has {{c1::a fixed length and no overlap — every event belongs to exactly one window (e.g. 1-minute buckets)}}. A **hopping** window has {{c2::a fixed length but advances by a smaller hop, so windows overlap and each event lands in several (e.g. 5-minute windows every 1 minute, for smoothed aggregates)}}. A **sliding** window contains {{c3::all events within some interval of each other, with boundaries set by the events themselves rather than a fixed grid}}. A **session** window {{c4::has no fixed length at all — it groups an entity's burst of activity and closes after a gap of inactivity (timeout), so its span differs per key}}.
