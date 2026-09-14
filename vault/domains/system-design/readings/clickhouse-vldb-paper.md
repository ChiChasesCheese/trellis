---
nodes: [analytics.olap]
url: https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf
tags: [paper]
---
# ClickHouse — Lightning Fast Analytics for Everyone (VLDB 2024)

A modern, readable account of how a real column store is built end to end:
on-disk column layout, per-column codecs, sparse primary indexes instead of
B-trees, and a vectorized/compiled execution engine. Far more concrete than a
textbook chapter, with the measurements to justify each choice.

**Extract on read:**
- Why columns beat rows for scans: only touched columns are read, and same-type runs compress far better (delta, double-delta, LZ4/ZSTD).
- Sparse primary index + granules + data skipping indexes — an OLAP store prunes blocks, it does not point-lookup rows.
- Vectorized execution over batches of column values, and the merge-tree write path (immutable parts, background merges) that makes it possible.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf)

## Archived copy
![[clickhouse-vldb-paper-clip]]
%% trellis:end %%
