%% trellis:begin %%
# File Sync (Dropbox/Google Drive)
*Design Problems / Media, Files & Collaboration*

Chunking, deduplication, delta sync, conflict handling and metadata consistency across devices.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/storage.object|Object Storage & Separation]], [[domains/system-design/map/distributed.consistency|Consistency Models]]

## Readings
- [[solution-file-sync|设计题解：文件同步系统（File Sync / Dropbox & Google Drive）]]
- [[src-dropbox-file-sync|Streaming File Synchronization]]
- [[src-dropbox-magic-pocket-file-sync|Scaling to exabytes and beyond]]
- [[src-hellointerview-file-sync|Design Dropbox]]

## Drills
- [[design-file-sync|Drill: Design a file sync service like Dropbox or Google Drive]]

## Cards (8)
1. [[problems-file-sync-delta-sync-bandwidth-reduction]]
2. [[problems-file-sync-cross-user-dedup-savings]]
3. [[problems-file-sync-block-content-addressed-model]]
4. [[problems-file-sync-cdc-vs-fixed-chunking]]
5. [[problems-file-sync-optimistic-concurrency-conflict]]
6. [[problems-file-sync-cursor-log-vs-merkle-tree]]
7. [[problems-file-sync-dedup-confirmation-side-channel]]
8. [[problems-file-sync-e2e-encryption-dedup-tradeoff]]
%% trellis:end %%

## Notes
