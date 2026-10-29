# Claim ledger — group U3 (Kafka + storage)

Every row was checked by reading the named source at the named tag/version (online only). Abbreviations: K = apache/kafka@4.0.0;
MY = mysql/mysql-server@mysql-8.4.0 `storage/innobase`; PG = postgres/postgres@REL_18_6 (REL_17_x where noted);
RDB = facebook/rocksdb@v10.9.1; LUC = apache/lucene@releases/lucene/10.5.2 (10.3.0 / 10.2.2 where noted);
SQ = sqlite/sqlite@version-3.54.1 or sqlite.org docs.

| card id | claim | source | how checked |
|---|---|---|---|
| uth-kafka-log-index-1-sparse-index | `.index` entry = 4-byte relative offset + 4-byte position, `ENTRY_SIZE = 8` | K:storage/.../log/OffsetIndex.java:`append`, `ENTRY_SIZE` | read |
| uth-kafka-log-index-1-sparse-index | an index entry is appended only when `bytesSinceLastIndexEntry > indexIntervalBytes` | K:storage/.../log/LogSegment.java:`append` | read |
| uth-kafka-log-index-1-sparse-index | `index.interval.bytes` default 4096 | K:server-common/.../config/ServerLogConfigs.java:`LOG_INDEX_INTERVAL_BYTES_DEFAULT` | read |
| uth-kafka-log-index-1-sparse-index | segment size default 1 GiB | K:storage/.../log/LogConfig.java:`DEFAULT_SEGMENT_BYTES` | read |
| uth-kafka-log-index-1-sparse-index | file name = 20-digit zero-padded base offset | K:storage/.../log/LogFileUtils.java:`filenamePrefixFromOffset` | read |
| uth-kafka-log-index-1-sparse-index | segments kept in `ConcurrentSkipListMap`, lookup by `floorEntry` | K:storage/.../log/LogSegments.java:`segments`, `floorSegment` | read |
| uth-kafka-log-index-1-sparse-index | lookup = largest entry <= target, then scan log from that position | K:OffsetIndex.java:`lookup`; LogSegment.java:`translateOffset` | read |
| uth-kafka-log-index-1-sparse-index | 1 GiB / 4096 = 262144 entries x 8 B = 2 MiB; 100-byte messages -> ~82 MiB | arithmetic on the constants above | derived |
| uth-kafka-log-index-2-warm-section | warm section = last 8192 bytes of the index (`warmEntries() = 8192 / entrySize()`, 1024 for the 8-byte index) | K:AbstractIndex.java:`warmEntries`, `largestLowerBoundSlotFor` | read |
| uth-kafka-log-index-2-warm-section | standard binary search touches pages that change as the index grows; produce latency can jump to ~1 s | K:AbstractIndex.java (comment above `warmEntries`) | read |
| uth-kafka-log-index-2-warm-section | in-sync follower/consumer lookups hit the newest entries | K:AbstractIndex.java (same comment) | read |
| uth-kafka-log-index-3-time-index | time index entry = 12 bytes (`ENTRY_SIZE = 12`), timestamp + relative offset | K:TimeIndex.java:`ENTRY_SIZE`, `parseEntry` | read |
| uth-kafka-log-index-3-time-index | timestamp lookup: `timeIndex().lookup` -> `offsetIndex().lookup` -> `log.searchForTimestamp` | K:LogSegment.java:`findOffsetByTimestamp` | read |
| uth-kafka-log-index-3-time-index | new index file preallocated to `roundDownToExactMultiple(maxIndexSize, entrySize)`; 10485760 and 10485756 follow from `segment.index.bytes` = 10 MiB | K:AbstractIndex.java:`createAndAssignMmap`; ServerLogConfigs `LOG_INDEX_SIZE_MAX_BYTES_DEFAULT` | read + arithmetic |
| uth-kafka-log-index-3-time-index | index is preallocated and shrunk only after rolls | K:clients/.../common/config/TopicConfig.java:`SEGMENT_INDEX_BYTES_DOC`; AbstractIndex.java:`resize` | read |
| uth-kafka-zero-copy-1-page-cache | `log.flush.interval.messages` default `Long.MAX_VALUE` | K:ServerLogConfigs.java:`LOG_FLUSH_INTERVAL_MESSAGES_DEFAULT` | read |
| uth-kafka-zero-copy-1-page-cache | 28-30 GB cache on 32 GB without GC; in-process cache duplicates page cache; object overhead doubles; cache stays warm across restart | K:docs/design.html (4.0.0), "Filesystem", pagecache paragraph | read |
| uth-kafka-zero-copy-2-sendfile | plaintext path uses `fileChannel.transferTo` | K:clients/.../common/network/PlaintextTransportLayer.java:`transferFrom` | read |
| uth-kafka-zero-copy-2-sendfile | SSL path reads file in 32768-byte chunks into a direct buffer and encrypts; no zero copy | K:clients/.../common/network/SslTransportLayer.java:`transferFrom` | read |
| uth-kafka-zero-copy-2-sendfile | traditional path = 4 copies and 2 system calls; `sendfile` leaves only the NIC copy; sendfile not used with SSL | K:docs/design.html "Efficiency" | read |
| uth-kafka-zero-copy-2-sendfile | on-disk format equals producer/consumer format | K:docs/design.html "Efficiency" | read |
| uth-kafka-zero-copy-3-batch-compress | `batch.size` default 16384, `compression.type` default none, `linger.ms` default 5 | K:clients/.../producer/ProducerConfig.java:`CONFIG` | read |
| uth-kafka-zero-copy-3-batch-compress | `linger.ms` default changed from 0 to 5 in 4.0 | K:docs/upgrade.html (4.0.0 section) | read |
| uth-kafka-zero-copy-3-batch-compress | broker decompresses to validate, writes batch compressed, consumer decompresses; per-message compression ratios are poor | K:docs/design.html "End-to-end Batch Compression" | read |
| uth-kafka-zero-copy-3-batch-compress | batching only under load when `linger.ms` is 0 | K:ProducerConfig.java:`LINGER_MS_DOC` | read |
| uth-kafka-partitioner-1-key-hash | `partitionForKey = toPositive(murmur2(serializedKey)) % numPartitions` | K:clients/.../producer/internals/BuiltInPartitioner.java:`partitionForKey` | read |
| uth-kafka-partitioner-1-key-hash | `toPositive(n) = n & 0x7fffffff` | K:clients/.../common/utils/Utils.java:`toPositive` | read |
| uth-kafka-partitioner-1-key-hash | `murmur2` fixed seed, 32-bit | K:Utils.java:`murmur2` | read |
| uth-kafka-partitioner-1-key-hash | `Math.abs(Integer.MIN_VALUE)` stays negative | Java SE `Math.abs(int)` javadoc | doc |
| uth-kafka-partitioner-1-key-hash | `partitioner.ignore.keys` exists | K:ProducerConfig.java:`PARTITIONER_IGNORE_KEYS_CONFIG` | read |
| uth-kafka-partitioner-1-key-hash | KafkaProducer uses `BuiltInPartitioner.partitionForKey` | K:KafkaProducer.java:`partition` | read |
| uth-kafka-partitioner-2-add-partitions | `hash % 6 == hash % 7` iff `hash mod 42` in 0..5, so ~1/7 stay | number theory (CRT), formula from `partitionForKey` | derived |
| uth-kafka-partitioner-2-add-partitions | formula depends only on key bytes and current partition count | K:BuiltInPartitioner.java:`partitionForKey` | read |
| uth-kafka-partitioner-3-sticky-adaptive | sticky partition switches after `stickyBatchSize` bytes, and `stickyBatchSize` = producer `batch.size` | K:BuiltInPartitioner.java:`updatePartitionInfo`; RecordAccumulator.java:`createBuiltInPartitioner` | read |
| uth-kafka-partitioner-3-sticky-adaptive | adaptive: cumulative frequency table + `Arrays.binarySearch`, shorter queues get larger weight | K:BuiltInPartitioner.java:`nextPartition`, `updatePartitionLoadStats` | read |
| uth-kafka-partitioner-3-sticky-adaptive | `partitioner.adaptive.partitioning.enable` default true; absent in 3.2.3, present in 3.3.0 | K@4.0.0 ProducerConfig.java; K@3.2.3 and K@3.3.0 ProducerConfig.java | read |
| uth-kafka-partitioner-3-sticky-adaptive | round-robin makes more, smaller batches and higher latency (sticky motivation) | KIP-480 "Motivation" (cwiki.apache.org) | doc |
| uth-kafka-compaction-1-two-pass | `SkimpyOffsetMap` entry = hash bytes + 8-byte offset; default MD5 (16 B) | K:storage/.../log/SkimpyOffsetMap.java | read |
| uth-kafka-compaction-1-two-pass | dedupe buffer default 128 MiB; load factor limit 0.9 | K:storage/.../log/CleanerConfig.java:`LOG_CLEANER_DEDUPE_BUFFER_SIZE`, defaults (0.9) | read |
| uth-kafka-compaction-1-two-pass | 128 MiB x 0.9 / 24 B = 5.03 M keys | arithmetic | derived |
| uth-kafka-compaction-1-two-pass | build offset map over dirty segments up to `firstUncleanableOffset`, then `cleanSegments` keeps records with offset >= map value; stops when map is full | K:core/.../kafka/log/LogCleaner.scala:`doClean`, `buildOffsetMap`, `shouldRetainRecord` | read |
| uth-kafka-compaction-1-two-pass | `min.cleanable.dirty.ratio` default 0.5 | K:storage/.../log/LogConfig.java:`DEFAULT_MIN_CLEANABLE_DIRTY_RATIO` | read |
| uth-kafka-compaction-2-tombstone | null value = delete marker; removed after delete retention; offsets never change and gaps are equivalent to the next offset | K:docs/design.html "Log Compaction Basics" | read |
| uth-kafka-compaction-2-tombstone | `delete.retention.ms` default 24 h | K:LogConfig.java:`DEFAULT_DELETE_RETENTION_MS` | read |
| uth-kafka-compaction-2-tombstone | `shouldRetainRecord` keeps a no-value record only while the delete horizon has not passed | K:LogCleaner.scala:`shouldRetainRecord` | read |
| uth-kafka-compaction-3-skimpy-probe | slot = hash size + 8 bytes, open addressing over one `ByteBuffer` | K:SkimpyOffsetMap.java | read |
| uth-kafka-compaction-3-skimpy-probe | probe i reads the int at byte `min(i, hashSize-4)` of the hash, plus `max(0, i - hashSize + 4)`, mod slots -> 13 hash-window probes then linear | K:SkimpyOffsetMap.java:`positionOf` | read |
| uth-kafka-compaction-3-skimpy-probe | equal hash overwrites offset; empty slot inserts | K:SkimpyOffsetMap.java:`put` | read |
| uth-kafka-replication-1-isr-hw | HW = min LEO over ISR (maximal ISR) members and the leader | K:core/.../kafka/cluster/Partition.scala:`maybeIncrementLeaderHW` | read |
| uth-kafka-replication-1-isr-hw | `replica.lag.time.max.ms` default 30000 | K:server/.../config/ReplicationConfigs.java:`REPLICA_LAG_TIME_MAX_MS_DEFAULT` | read |
| uth-kafka-replication-1-isr-hw | ISR vs majority: f+1 replicas tolerate f failures, quorum needs 2f+1 | K:docs/design.html "Replication" | read |
| uth-kafka-replication-2-acks-min-isr | `acks` default `all` in 4.0 and 3.0.0, `1` in 2.8.2 | K@4.0.0, K@3.0.0, K@2.8.2 ProducerConfig.java | read |
| uth-kafka-replication-2-acks-min-isr | `min.insync.replicas` default 1 | K:ServerLogConfigs.java:`MIN_IN_SYNC_REPLICAS_DEFAULT` | read |
| uth-kafka-replication-2-acks-min-isr | `NotEnoughReplicasException` thrown when ISR size < min ISR and `requiredAcks == -1` | K:Partition.scala:`appendRecordsToLeader` | read |
| uth-kafka-replication-2-acks-min-isr | HW not advanced when under min ISR | K:Partition.scala:`maybeIncrementLeaderHW` (`isUnderMinIsr`) | read |
| uth-kafka-replication-2-acks-min-isr | `acks=all` acknowledges once all *current* ISR members have it | K:docs/design.html "Availability and Durability Guarantees" | read |
| uth-kafka-replication-3-unclean-election | `unclean.leader.election.enable` default false; default since 0.11.0.0 | K:LogConfig.java:`DEFAULT_UNCLEAN_LEADER_ELECTION_ENABLE`; docs/design.html "Unclean leader election" | read |
| uth-kafka-replication-3-unclean-election | trade-off wording, quorum schemes have the same dilemma | K:docs/design.html "Unclean leader election" | read |
| uth-kafka-timing-wheel-1-hierarchical-wheel | default `tickMs = 1`, `wheelSize = 20` | K:server-common/.../util/timer/SystemTimer.java | read |
| uth-kafka-timing-wheel-1-hierarchical-wheel | bucket = `(expiration / tickMs) % wheelSize`; overflow wheel tickMs = interval of lower wheel | K:.../util/timer/TimingWheel.java:`add`, `addOverflowWheel` | read |
| uth-kafka-timing-wheel-1-hierarchical-wheel | buckets are doubly linked cyclic lists; insert O(1)/O(m), delete O(1), priority-queue timers O(log n) | K:TimerTaskList.java; TimingWheel.java class comment | read |
| uth-kafka-timing-wheel-1-hierarchical-wheel | purgatory uses `SystemTimer` (produce/fetch/heartbeat/join delayed operations exist) | K:server-common/.../purgatory/DelayedOperationPurgatory.java; core/.../server/DelayedProduce.scala, DelayedFetch.scala | read |
| uth-kafka-timing-wheel-2-no-tick | non-empty buckets sit in a `DelayQueue`; `advanceClock` polls it, advances to bucket expiration, flushes via `addTimerTaskEntry` | K:SystemTimer.java:`advanceClock`; TimingWheel.java:`add` | read |
| uth-kafka-timing-wheel-3-which-level | level capacity 20^k ms; placement rule `expiration < currentTime + interval` | K:TimingWheel.java:`add`; arithmetic | read + derived |
| uth-kafka-consumer-group-1-offsets-topic | key = (group, topic, partition) | K:group-coordinator/.../message/OffsetCommitKey.json | read |
| uth-kafka-consumer-group-1-offsets-topic | topic cleanup policy compact | K:group-coordinator/.../GroupCoordinatorService.java:`groupMetadataTopicConfigs` | read |
| uth-kafka-consumer-group-1-offsets-topic | partition count default 50, RF 3, retention 7 days | K:group-coordinator/.../GroupCoordinatorConfig.java:`OFFSETS_TOPIC_PARTITIONS_DEFAULT`, `OFFSETS_TOPIC_REPLICATION_FACTOR_DEFAULT`, `OFFSETS_RETENTION_MINUTES_DEFAULT` | read |
| uth-kafka-consumer-group-1-offsets-topic | `partitionFor = Utils.abs(groupId.hashCode()) % numPartitions` | K:GroupCoordinatorService.java:`partitionFor` | read |
| uth-kafka-consumer-group-1-offsets-topic | retention counts from the moment the group becomes empty | K:GroupCoordinatorConfig.java:`OFFSETS_RETENTION_MINUTES_DOC` | read |
| uth-kafka-consumer-group-2-range-vs-roundrobin | Range per topic: `n / c` each, first `n % c` consumers get one extra | K:clients/.../consumer/RangeAssignor.java class comment, `TopicAssignmentState` | read |
| uth-kafka-consumer-group-2-range-vs-roundrobin | example assignments for 2 consumers x 2 topics x 3 partitions | K:RangeAssignor.java and RoundRobinAssignor.java class comments | read |
| uth-kafka-consumer-group-2-range-vs-roundrobin | default strategy list Range + CooperativeSticky in 3.0.0 (only Range in 2.8.2) | K@3.0.0 / K@2.8.2 ConsumerConfig.java; K@4.0.0 ConsumerConfig.java | read |
| uth-kafka-consumer-group-3-rebalance | EAGER revokes all owned partitions; COOPERATIVE keeps owned ones and revoked ones are reassigned in the next rebalance | K:clients/.../consumer/ConsumerPartitionAssignor.java:`RebalanceProtocol` javadoc | read |
| uth-kafka-consumer-group-3-rebalance | KIP-848 protocol GA in 4.0; default `group.protocol` = classic; built-in server assignors uniform and range | K:docs/upgrade.html (4.0.0); ConsumerConfig.java:`DEFAULT_GROUP_PROTOCOL`; GroupCoordinatorConfig.java:`CONSUMER_GROUP_BUILTIN_ASSIGNORS` | read |
| uth-kafka-consumer-group-3-rebalance | classic: one member computes the assignment on the client | K:ConsumerPartitionAssignor.java (client-side `assign`) | read |
| uth-storage-btree-1-fanout-height | `UNIV_PAGE_SIZE_DEF = 1 << 14` = 16 KB | MY:include/univ.i | read |
| uth-storage-btree-1-fanout-height | `REC_N_NEW_EXTRA_BYTES = 5`, `REC_NODE_PTR_SIZE = 4` | MY:rem/rec.h | read |
| uth-storage-btree-1-fanout-height | fan-out ~900 and 12 M / 10 B rows are arithmetic on the constants above (16 KB / 17 B, 15 rows of 1 KB per leaf) | arithmetic, labelled estimate on the card | derived |
| uth-storage-btree-2-clustered-lookup | secondary index records contain the primary key; long PK enlarges secondary indexes; hidden 6-byte row id | dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html | read |
| uth-storage-btree-3-leaf-links | index pages on the same level form a doubly linked list via `FIL_PAGE_PREV`/`FIL_PAGE_NEXT` | MY:include/fil0types.h | read |
| uth-storage-btree-3-leaf-links | `btreeNext` climbs with `moveToParent` at the end of a leaf | SQ:src/btree.c:`btreeNext` | read |
| uth-storage-btree-3-leaf-links | table b-trees: 64-bit int keys, all data in leaves; interior pages hold keys + 32-bit child page numbers | sqlite.org/fileformat2.html "B-tree Pages" | read |
| uth-storage-lsm-1-write-path | `write_buffer_size` 64 MB; `level0_file_num_compaction_trigger` 4; `num_levels` 7; `max_bytes_for_level_multiplier` 10 | RDB:include/rocksdb/options.h, advanced_options.h | read |
| uth-storage-lsm-1-write-path | L0 files overlap and are all merged to L1; levels are sorted runs; compaction merges sorted files | RDB wiki Leveled-Compaction | read |
| uth-storage-lsm-1-write-path | `level_compaction_dynamic_level_bytes` default since 8.4; targets derived from last level | RDB wiki Leveled-Compaction | read |
| uth-storage-lsm-2-skiplist-memtable | default memtable factory `SkipListFactory`; `InlineSkipList` max_height 12, branching 4 | RDB:advanced_options.h; memtable/inlineskiplist.h | read |
| uth-storage-lsm-2-skiplist-memtable | ~1.33 pointers per entry; concurrent insert default on, skiplist only | RDB wiki MemTable | read |
| uth-storage-lsm-3-amplification | leveled WA often > 10; leveled minimises space amp at cost of read/write amp; tiered minimises write amp | RDB wiki Leveled-Compaction, Compaction, Universal-Compaction | read |
| uth-storage-lsm-3-amplification | read path: memtable, every L0 file, one file per deeper level (binary search of file ranges) | RDB wiki Leveled-Compaction | read |
| uth-storage-bloom-1-skip-file | 9.9 bits/key ~ 1% FP; `filter_policy` default `nullptr` | RDB:filter_policy.h; table.h | read |
| uth-storage-bloom-1-skip-file | filter per SST file, avoids reads for absent keys | RDB wiki RocksDB-Bloom-Filter | read |
| uth-storage-bloom-2-cache-line | 512-bit cache-line buckets, 10 bits/key, 6 probes: theoretical 0.9535%, implementation ~0.957%, legacy 1.138% | RDB:util/bloom_impl.h comment | read |
| uth-storage-bloom-2-cache-line | Ribbon: ~30% less space, 3-4x CPU, since 6.15, ~7 bits/key for 1% | RDB wiki RocksDB-Bloom-Filter; filter_policy.h | read |
| uth-storage-bloom-3-bits-vs-fp | `StandardFpRate = (1 - exp(-k/bpk))^k`; with k = ln2 * bpk this is 0.6185^bpk | RDB:util/bloom_impl.h:`StandardFpRate`; algebra | read + derived |
| uth-storage-bloom-3-bits-vs-fp | 4.9 bits -> 10%, 9.9 -> 1%, 15.5 -> 0.1% | RDB wiki RocksDB-Bloom-Filter | read |
| uth-storage-bloom-3-bits-vs-fp | 1 M keys: 9.9 bits = 1.24 MB, 15.5 bits = 1.94 MB | arithmetic | derived |
| uth-storage-wal-mvcc-1-write-ahead | commit = commit record appended to WAL; checkpoint moves WAL content back; auto checkpoint at 1000 pages; readers check WAL then DB | sqlite.org/wal.html | read |
| uth-storage-wal-mvcc-1-write-ahead | `checkpoint_timeout` default 5 min; `full_page_writes` logs the whole page on first change after a checkpoint (torn pages) | postgresql.org/docs/18/runtime-config-wal.html | read |
| uth-storage-wal-mvcc-1-write-ahead | `fullPageWrites = true` default | PG:src/backend/access/transam/xlog.c | read |
| uth-storage-wal-mvcc-2-pg-tuple | heap tuple header 23 bytes, `t_xmin`, `t_xmax`, `t_ctid` | PG:src/include/access/htup_details.h:`HeapTupleHeaderData` | read |
| uth-storage-wal-mvcc-2-pg-tuple | visibility is decided per tuple against a snapshot | PG:src/backend/access/heap/heapam_visibility.c:`HeapTupleSatisfiesMVCC` | read |
| uth-storage-wal-mvcc-2-pg-tuple | t_ctid points to this or newer version | postgresql.org/docs/18/storage-page-layout.html | read |
| uth-storage-wal-mvcc-3-innodb-undo | `DB_TRX_ID` 6 bytes, `DB_ROLL_PTR` 7 bytes pointing into undo; delete is an update with a flag; purge; commit regularly incl. read-only | dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html | read |
| uth-storage-query-exec-1-hash-join | hybrid hash join; batches always a power of two; increase doubles; inner and outer batch files | PG:src/backend/executor/nodeHashjoin.c comments | read |
| uth-storage-query-exec-1-hash-join | memory limit = `work_mem * hash_mem_multiplier` | PG:nodeHash.c:`get_hash_memory_limit` | read |
| uth-storage-query-exec-1-hash-join | `work_mem` 4 MB; `hash_mem_multiplier` 2.0 in 15+, 1.0 in 13 and 14 | postgresql.org/docs/18/runtime-config-resource.html; guc.c at REL_13_0 / REL_14_9 / REL_15_0 | read |
| uth-storage-query-exec-2-external-sort | quicksort runs + balanced k-way merge; polyphase before 15 | PG:src/backend/utils/sort/tuplesort.c header comment | read |
| uth-storage-query-exec-2-external-sort | `tuplesort_merge_order = allowedMem / (2 * BLCKSZ + MERGE_BUFFER_SIZE)`, MINORDER 6, MAXORDER 500, `MERGE_BUFFER_SIZE = BLCKSZ * 32` | PG:tuplesort.c | read |
| uth-storage-query-exec-2-external-sort | 4 MB / (2 x 8 KB + 256 KB) = 15.06 -> 15 | arithmetic | derived |
| uth-storage-query-exec-2-external-sort | high-order merges slow due to CPU cache effects; a "tape" costs a few KB | PG:tuplesort.c comments | read |
| uth-storage-query-exec-3-merge-join | cursors advance on comparison; inner mark/restore for duplicates; equality clauses only | PG:src/backend/executor/nodeMergejoin.c header comment | read |
| uth-storage-buffer-pool-1-midpoint-lru | old sublist 3/8; `innodb_old_blocks_pct` 37; `innodb_old_blocks_time` 1000 | MY:handler/ha_innodb.cc; dev.mysql.com innodb-buffer-pool + innodb-performance-midpoint_insertion | read |
| uth-storage-buffer-pool-1-midpoint-lru | new page inserted after `LRU_old` (head of old list) | MY:buf/buf0lru.cc:`buf_LRU_add_block_low` | read |
| uth-storage-buffer-pool-1-midpoint-lru | page moves to young only if first access was >= threshold ago | MY:include/buf0buf.ic:`buf_page_peek_if_too_old` | read |
| uth-storage-buffer-pool-1-midpoint-lru | scan pages accessed several times in quick succession and never again | dev.mysql.com innodb-performance-midpoint_insertion | read |
| uth-storage-buffer-pool-2-clock-sweep | `BM_MAX_USAGE_COUNT 5`; up to MAX+1 sweeps | PG:src/include/storage/buf_internals.h | read |
| uth-storage-buffer-pool-2-clock-sweep | pin increments usage count up to the cap | PG:src/backend/storage/buffer/bufmgr.c (usage count < BM_MAX_USAGE_COUNT) | read |
| uth-storage-buffer-pool-2-clock-sweep | sweep skips pinned, decrements non-zero, takes zero | PG:src/backend/storage/buffer/freelist.c:`StrategyGetBuffer` | read |
| uth-storage-buffer-pool-3-ring-buffer | seq scan strategy only if `rs_nblocks > NBuffers / 4` | PG:src/backend/access/heap/heapam.c:`initscan` | read |
| uth-storage-buffer-pool-3-ring-buffer | ring: bulkread 256 KB (17), 256 KB + IO concurrency term (18), vacuum 2048 KB, bulkwrite 16 MB | PG@REL_17_x and REL_18_6 freelist.c:`GetAccessStrategy` | read |
| uth-storage-buffer-pool-3-ring-buffer | COPY and CTAS use `GetBulkInsertState` -> `BAS_BULKWRITE` | PG:commands/copyfrom.c, createas.c; heapam.c:`GetBulkInsertState` | read |
| uth-storage-inverted-index-1-postings | block size 256, doc deltas, FOR bit packing by max value, bit set when denser, 0 bits when block is contiguous | LUC:codecs/lucene104/Lucene104PostingsWriter.java (docDeltaBuffer: FOR / bit-set branch); ForUtil.java | read |
| uth-storage-inverted-index-1-postings | block size raised from 128 to 256 in 10.4.0 | LUC:lucene/CHANGES.txt (GITHUB#15160, 10.4.0 section); backward_codecs lucene101 ForUtil `BLOCK_SIZE = 128` | read |
| uth-storage-inverted-index-2-skip-data | level 0 skip data per packed block; level 1 per 32 blocks = 8192 docs | LUC:Lucene104PostingsFormat.java (`LEVEL1_NUM_DOCS`) | read |
| uth-storage-inverted-index-2-skip-data | iterators sorted by cost, lead advances others | LUC:search/ConjunctionUtils.java, ConjunctionDISI.java | read |
| uth-storage-inverted-index-3-term-dict | block-tree .tim blocks of 25-48 entries; .tip term index | LUC:codecs/lucene103/blocktree/Lucene103BlockTreeTermsWriter.java | read |
| uth-storage-inverted-index-3-term-dict | term index is a trie from 10.3.0, instead of FST | LUC:lucene/CHANGES.txt (GITHUB#14333, 10.3.0 section); TrieBuilder.java | read |
| uth-storage-inverted-index-3-term-dict | FST compiler builds a minimal FST from sorted input | LUC:util/fst/FSTCompiler.java class comment | read |
| uth-storage-inverted-index-4-roaring-filter | cache impl: cost*100 >= maxDoc -> bit set, else `RoaringDocIdSet` | LUC:search/LRUQueryCache.java:`cacheImpl` | read |
| uth-storage-inverted-index-4-roaring-filter | block 2^16, array if <= 2^12, inverse array if > 2^16 - 2^12, else bitset; empty blocks null | LUC:util/RoaringDocIdSet.java | read |
| uth-storage-inverted-index-4-roaring-filter | 4096 shorts = 8192 B = 65536 bits | arithmetic | derived |
