---
nodes: [analytics.warehouse, storage.object]
url: https://iceberg.apache.org/spec/
tags: [reference]
---
# Apache Iceberg Table Format (spec + docs)

The open table format that made "lakehouse" concrete: ACID snapshots,
schema evolution, and time travel implemented as metadata layers over
dumb object storage. Read the spec's overview plus the docs' "How Iceberg
works" pages; the details generalize to Delta Lake and Hudi.

**Extract on read:**
- Snapshot isolation via immutable manifest trees + one atomic pointer swap.
- Why partition evolution is possible when partitioning is metadata, not paths.
- Compaction and the small-files problem every log-structured system shares.

%% trellis:begin %%
## Source
[Open the original ↗](https://iceberg.apache.org/spec/)

## Archived copy
![[iceberg-table-format-clip]]
%% trellis:end %%
