---
title: How Discord Stores Trillions of Messages
source: https://discord.com/blog/how-discord-stores-trillions-of-messages
author: Bo Ingram
published: '2023-03-06'
site: discord.com
clipped: '2026-09-20'
---

# How Discord Stores Trillions of Messages

## Our Cassandra Troubles

We stored our messages in a database called cassandra-messages. As its name suggests, it ran Cassandra, and it stored messages. In 2017, we ran 12 Cassandra nodes, storing billions of messages.

At the beginning of 2022, it had 177 nodes with trillions of messages. To our chagrin, it was a high-toil system — our on-call team was frequently paged for issues with the database, latency was unpredictable, and we were having to cut down on maintenance operations that became too expensive to run.

What was causing these issues? First, let’s take a look at a message.

The CQL statement above is a minimal version of our message schema. Every ID we use is a [Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake), making it chronologically sortable. We partition our messages by the channel they’re sent in, along with a bucket, which is a static time window. This partitioning means that, in Cassandra, all messages for a given channel and bucket will be stored together and replicated across three nodes (or whatever you’ve set the replication factor).

Within this partitioning lies a potential performance pitfall: a server with just a small group of friends tends to send orders of magnitude fewer messages than a server with hundreds of thousands of people.

In Cassandra, reads are more expensive than writes. Writes are appended to a commit log and written to an in memory structure called a memtable that is eventually flushed to disk. Reads, however, need to query the memtable and potentially multiple SSTables (on-disk files), a more expensive operation. Lots of concurrent reads as users interact with servers can hotspot a partition, which we refer to imaginatively as a “hot partition”.  The size of our dataset when combined with these access patterns led to struggles for our cluster.

When we encountered a hot partition, it frequently affected latency across our entire database cluster. One channel and bucket pair received a large amount of traffic, and latency in the node would increase as the node tried harder and harder to serve traffic and fell further and further behind.

Other queries to this node were affected as the node couldn’t keep up. Since we perform reads and writes with quorum consistency level, all queries to the nodes that serve the hot partition suffer latency increases, resulting in broader end-user impact.

Cluster maintenance tasks also frequently caused trouble. We were prone to falling behind on compactions, where Cassandra would compact SSTables on disk for more performant reads. Not only were our reads then more expensive, but we’d also see cascading latency as a node tried to compact.

We frequently performed an operation we called the “gossip dance”, where we’d take a node out of rotation to let it compact without taking traffic, bring it back in to pick up hints from Cassandra’s hinted handoff, and then repeat until the compaction backlog was empty. We also spent a large amount of time tuning the JVM’s garbage collector and heap settings, because GC pauses would cause significant latency spikes.
