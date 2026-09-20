---
title: Kafka Message Delivery Guarantees
source: https://docs.confluent.io/kafka/design/delivery-semantics.html
published: '2026-08-12'
site: Confluent Documentation
clipped: '2026-09-20'
---

# Kafka Message Delivery Guarantees

# Kafka Message Delivery Guarantees[](#ak-message-delivery-guarantees)

Apache Kafka® is an open-source distributed streaming system used for stream processing, real-time data pipelines, and data integration at scale.

This topic describes the semantic guarantees Kafka provides for message delivery between producers, brokers, and consumers. It also describes how Kafka supports exactly once delivery semantics, which is a key feature of Kafka that enables you to build reliable, fault-tolerant applications.

## Semantic guarantees[](#semantic-guarantees)

[Kafka Producer Design](producer-design.html#producer-design) and [Kafka Consumer Design: Consumers, Consumer Groups, and Offsets](consumer-design.html#consumer-design) helped you understand how producers and consumers work,
but you should also understand the semantic guarantees Apache Kafka® provides between the broker and
producers and consumers.
Semantic guarantee refers to how the broker, producer and consumer agree to share messages.
There are three types of message sharing:

- At most once: Messages are delivered once, and if there is a system failure, messages may be lost and are not redelivered.
- At least once: This means messages are delivered one or more times. If there is a system failure, messages are never lost, but they may be delivered more than once.
- Exactly once: This is the preferred behavior in that each message is delivered once and only once. Messages are never lost or read twice even if some part of the system fails.

These semantics offer tradeoffs between latency and message durability. You will need to choose the semantic that makes sense for your application context.

Also, note that many systems claim to provide exactly once delivery semantics, but this might not always what you think it is. For example, these system may not account for cases where a consumer or producer outside of the system has failed.

In contrast, Kafka’s semantics are straight-forward. When publishing a message
Kafka considers the message *committed* to the log. After a message is committed it
will not be lost as long as least one broker that has a replication of the partition with that
message remains “alive”.

The next sections describe producer and consumer delivery in terms of these delivery semantics. These sections assume the broker is always lossless.

## Producer delivery[](#producer-delivery)

- **At most once** - For the lowest latency, messages can be sent asynchronously in a “fire and forget” way, meaning
the producer does not wait for any acknowledgement that messages were received, or for more latency, but less
risk of message loss, the producer can wait for acknowledgment from the leader broker. In either case, messages
are delivered once, and if there is a system failure, messages may be lost and are
not redelivered.
- **At least once** - In this semantic, if a producer expects but fails to receive a response indicating that a message was committed,
it will resend the message. This provides at-least-once delivery semantics since the
message may be written to the log again during resending if the original request had succeeded.
Since version 0.11.0.0, the Kafka producer provides an idempotent option for configuring message delivery.
The idempotent delivery option guarantees that resending a message will not result in
duplicate entries in the log, and that log order is maintained. To achieve this, the broker assigns each producer an ID and
deduplicates messages using a sequence number that is sent by the producer with every message.
- **Exactly once** - Starting with version 0.11.0.0, producers can utilize transactional delivery.
This means a producer can request acknowledgment that messages were received and successfully
replicated, and if it resends a message, it resends with idempotency, meaning existing messages
are overwritten rather than duplicated. This comes with higher latency, but the most durability.
In order to enable transactional guarantees, consumers should also be configured appropriately.

Confluent Tip

For an explanation of these concepts from one of Confluent’s cofounders, watch the Data Durability and Availability Guarantees video module.

## Consumer receipt[](#consumer-receipt)

Next, you should understand message semantics from the point-of-view of the consumer. Each message in a topic partition has a sequential identifier called an offset. All replicas of a partition have the same log with the same offsets, and the consumer controls its position in this log. If the consumer fails and another consumer needs to take over reading from this partition, the new consumer needs to know what offset it should start at. The consumer has a few options for how it reads messages and updates its current position:

- **At most once** - In this case, a consumer reads a set of messages, saves its position in the log,
and then processes the messages. If the consumer process crashes after saving its position, but before saving the output of its
message processing, the consumer that takes over processing would start at the saved position
and the messages prior to that position would not be processed.
This is*at-most-once* semantics for the consumer, because in a failure, messages may not be processed.
- **At least once** - This means a consumer reads a set of messages, processes the messages, and
then saves its position. In this case, if the consumer process crashes after processing messages, but before saving its
position, the new process that takes over may process some messages a second time.
Note that in this case, you can assign messages a primary key, so that updates are idempotent,
meaning that if the message is received twice, it just overwrites the existing record
with the same message data.
- **Exactly once** - When consuming from a Kafka topic and producing to another topic such as in a Kafka Streams application,
Kafka leverages transactional producer capabilities added in version 0.11.0.0 to achieve exactly once semantics.
The consumer’s position is stored as a message in a topic, so offset data
in written to Kafka in the same transaction as when processed data is written to the output topics.
If the transaction is aborted, the consumer’s position reverts to its old value and you can specify whether output topics are visible to other consumers
using the`isolation_level` property. For the default isolation level,`read_uncommitted` ,
all messages, even ones in aborted transactions, are visible to consumers.
In`read_committed` ,  the consumer only reads messages from committed transactions.When writing to an external system, it can be challenging to coordinate the data the consumer is receiving and the consumer’s position in the data. Typically, this might be done with a two-phase commit, storing the consumer position, and then storing the consumed data. In contrast, Kafka stores the position in the same place it stores the consumed data. For example, a Connect connector populates data in Hadoop Distributed File System (HDFS) along with the offsets of the data it reads so that it is guaranteed that both data and offsets are updated, or neither is.

## Exactly once support[](#exactly-once-support)

Kafka supports exactly-once delivery in  [Kafka Streams](/platform/current/streams/overview.html) and uses transactional
producers and consumers to provide exactly-once delivery when transferring and processing data between Kafka
topics.

To enable exactly-once delivery for other consumer and producer systems, you can use the automatic offset management
that [Kafka Connect API](/platform/current/connect/javadocs/javadoc/index.html) offers.

Otherwise, by default Kafka guarantees at-least-once delivery. You can implement at-most-once delivery by disabling retries on the producer and committing offsets in the consumer before processing a batch of messages.

Confluent Tip

For an explanation of how transactions enable exactly once message semantics for producers and consumers, watch the Transactions video module.
