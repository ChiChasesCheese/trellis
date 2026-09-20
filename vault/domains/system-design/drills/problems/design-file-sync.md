---
nodes: [problems.media.file-sync, distributed.consistency]
tags: [problem]
---
# Drill: Design a file sync service like Dropbox or Google Drive

Design the sync path for a cloud file storage product: a user edits a file on one device
and every other device on that account — plus every collaborator on a shared folder —
converges on the new content, even after devices have been offline and edited
independently.

**Constraints to state and honor**
- 50M DAU generating roughly 50MB of new or changed data each per day; files range up to
  tens of GB.
- Peak metadata write traffic around 90K QPS, fanning out to roughly 3 online devices per
  user.
- A localized edit to a large file must not re-upload the whole file.
- Concurrent offline edits to the same file must never silently lose one side's changes.
- Semantic merging of document contents (OT/CRDT) and E2E-encryption key management are
  out of scope.

**Grading points**
- Models storage as content-addressed blocks referenced by ordered lists in immutable
  version records, rather than each version owning private bytes ([[problems-file-sync-block-content-addressed-model]]).
- Quantifies the bandwidth win of block-level delta sync against full-file re-upload
  instead of asserting that chunking "saves traffic" ([[problems-file-sync-delta-sync-bandwidth-reduction]]).
- Explains why fixed-size chunking cascades hash invalidation on mid-file insertions and
  what content-defined chunking costs to fix it ([[problems-file-sync-cdc-vs-fixed-chunking]]).
- Detects concurrent edits with optimistic concurrency control on a parent version id and
  preserves both sides as a conflicted copy instead of last-write-wins ([[problems-file-sync-optimistic-concurrency-conflict]]).
- Designs multi-device catch-up as a cursor-based append-only change log and can argue
  why that is equivalent to, but simpler than, a Merkle-tree directory diff ([[problems-file-sync-cursor-log-vs-merkle-tree]]).
- Quantifies cross-user deduplication's storage saving and names the confirmation-of-a-file
  side channel it introduces, with a scoping mitigation ([[problems-file-sync-cross-user-dedup-savings]], [[problems-file-sync-dedup-confirmation-side-channel]]).
- States the consistency contract explicitly — eventual consistency across devices,
  read-your-writes on the originating device — rather than hand-waving "it syncs" ([[distributed-consistency-ladder]], [[distributed-read-your-writes]]).
- Handles a hot shared folder (hundreds of collaborators) and says what happens when the
  push channel or a metadata shard fails, including whether it degrades to polling.
- Names what breaks at 100x if end-to-end encryption becomes the default ([[problems-file-sync-e2e-encryption-dedup-tradeoff]]).

**Solution**: [[solution-file-sync]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
