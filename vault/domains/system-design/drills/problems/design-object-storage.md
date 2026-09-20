---
nodes: [problems.foundations.object-storage, storage.object]
tags: [problem]
---
# Drill: Design an object storage system (S3-class)

Design the object storage service itself — buckets and immutable blobs at exabyte
scale — not an application that merely calls one. Target: 1 exabyte of logical data,
about 3.8 trillion objects, peak 2,314,815 GET requests/second, with buckets that can
hold billions of keys.

**Constraints to state and honor**
- Whole-object PUT semantics only: no in-place partial writes.
- Durability target on the order of a millionth-of-a-percent-per-year loss probability
  per stripe or better, under an explicitly stated failure model (state the AFR
  assumption and whether failures are treated as independent).
- DELETE must return immediately; physical space reclamation is asynchronous.
- A single-bucket List operation must not be assumed to complete in one call at
  billions of keys.

**Grading points**
- Computes the metadata service's minimum shard count from a real per-key-prefix
  throughput ceiling and peak QPS, rather than asserting "the metadata service needs
  sharding" without a number
  ([[problems-object-storage-metadata-shard-count-from-prefix-throughput]]).
- States that PUT replaces the whole object atomically and traces the consequence for
  both in-place appends and large-object upload design
  ([[problems-object-storage-put-replaces-whole-object]], [[storage-object-vs-filesystem]]).
- Chooses a placement scheme (CRUSH-style deterministic hashing over a cluster map)
  that avoids storing an explicit node list per object, and explains why this matters
  when capacity is added ([[problems-object-storage-crush-no-central-lookup-table]]).
- Computes annual stripe-loss probability for at least two schemes (e.g. triple
  replication vs. a wide erasure code) under a stated independent-failure model, and
  correctly attributes the durability difference to the absolute failure-tolerance
  count rather than the raw storage multiplier
  ([[problems-object-storage-wide-ec-more-durable-than-triple-replication]]).
- Designs multipart upload so that concurrent GETs never observe a partially-uploaded
  object, and explains what CompleteMultipartUpload's atomicity actually buys
  ([[problems-object-storage-multipart-atomic-completion]], [[storage-multipart-ranged-io]]).
- Explains why DELETE only writes a tombstone and what reclaims physical space, sizing
  the reclamation workload at scale rather than treating it as free
  ([[problems-object-storage-tombstone-then-compaction-gc]]).
- Identifies that a sequential/monotonic key prefix creates a write hot spot regardless
  of total shard count, and states the fix
  ([[problems-object-storage-sequential-key-prefix-hotspot]]).
- States what changes structurally (not just "add more machines") at 10x traffic,
  including the shard-routing layer itself
  ([[problems-object-storage-10x-metadata-shards-4096]]).

**Solution**: [[solution-object-storage]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
