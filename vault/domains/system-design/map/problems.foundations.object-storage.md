%% trellis:begin %%
# Object Storage (S3)
*Design Problems / Building Blocks & Warm-ups*

Buckets and immutable blobs at exabyte scale: metadata service, placement, erasure coding, durability math.

**Requires:** [[domains/system-design/map/storage.object|Object Storage & Separation]]

## Readings
- [[solution-object-storage|设计题解：对象存储（Object Storage，S3-class）]]
- [[src-aws-s3-durability-object-storage|Data protection in Amazon S3]]
- [[src-aws-s3-performance-object-storage|Best practices design patterns: optimizing Amazon S3 performance]]
- [[src-aws-s3-qfacts-object-storage|Amazon S3 quick facts (multipart upload core specifications)]]
- [[src-azure-storage-paper-object-storage|Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency]]
- [[src-backblaze-drive-stats-object-storage|Backblaze Drive Stats for 2025]]
- [[src-crush-paper-object-storage|CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data]]
- [[src-usenix-f4-object-storage|f4: Facebook's Warm BLOB Storage System]]
- [[src-usenix-haystack-instagram|Finding a Needle in Haystack: Facebook's Photo Storage]]

## Drills
- [[design-object-storage|Drill: Design an object storage system (S3-class)]]

## Cards (8)
1. [[problems-object-storage-metadata-shard-count-from-prefix-throughput]]
2. [[problems-object-storage-put-replaces-whole-object]]
3. [[problems-object-storage-crush-no-central-lookup-table]]
4. [[problems-object-storage-wide-ec-more-durable-than-triple-replication]]
5. [[problems-object-storage-multipart-atomic-completion]]
6. [[problems-object-storage-tombstone-then-compaction-gc]]
7. [[problems-object-storage-sequential-key-prefix-hotspot]]
8. [[problems-object-storage-10x-metadata-shards-4096]]
%% trellis:end %%

## Notes
