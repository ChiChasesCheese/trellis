---
nodes: [storage.internals]
url: https://www.benstopford.com/2015/02/14/log-structured-merge-trees/
tags: [canonical]
---
# Log Structured Merge Trees (Ben Stopford)

Builds the LSM-tree from first principles by asking what is wrong with writing
into a B-tree, then adds each mechanism — memtable, sorted files, compaction,
bloom filters — only once the previous step has visibly failed. Twenty minutes
for the whole B-tree-vs-LSM argument.

**Extract on read:**
- B-trees write in place and therefore pay random I/O per update; LSMs buffer in memory and flush sequentially, trading it for read work later.
- Compaction as the knob: levelled vs size-tiered moves cost between write amplification, read amplification, and space amplification — you pick two.
- Bloom filters and sparse indexes are what keep an LSM read from touching every level.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.benstopford.com/2015/02/14/log-structured-merge-trees/)

## Archived copy
![[lsm-vs-btree-stopford-clip]]
%% trellis:end %%
