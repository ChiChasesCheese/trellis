---
nodes: [storage.relational.indexing]
url: https://postgrespro.com/blog/pgsql/4161516
tags: [canonical]
---
# Indexes in PostgreSQL — 4 (Btree) (Egor Rogov)

One article that takes you from B-tree page layout to the planner's actual
choices, with real EXPLAIN output at every step. Where a book site makes you
navigate, this hands you the whole mechanism — and it is specific enough that
the leftmost-prefix rule stops being a rule you memorize.

**Extract on read:**
- Structure: internal pages route, leaf pages are a sorted doubly-linked list — which is why one index serves equality, range, sort, and min/max.
- Multicolumn indexes are sorted by the tuple of columns: a condition on the first column narrows the scan, one on the second only filters it.
- Index-only scans and the visibility map; plus the cost side — every index is extra write amplification and bloat to vacuum.

%% trellis:begin %%
## Source
[Open the original ↗](https://postgrespro.com/blog/pgsql/4161516)

## Archived copy
![[postgres-btree-internals-clip]]
%% trellis:end %%
