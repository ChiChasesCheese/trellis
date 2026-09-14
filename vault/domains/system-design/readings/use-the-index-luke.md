---
nodes: [storage.relational.indexing]
url: https://use-the-index-luke.com/
tags: [canonical, book]
---
# Use The Index, Luke! (Markus Winand)

The one-stop free book on SQL indexing done right — B-tree mechanics,
composite-index column order, covering indexes, and why ORMs quietly defeat
your indexes. Nothing else teaches the leftmost-prefix rule this well.

**Extract on read:**
- B-tree lookup = tree walk + leaf scan; what each index column position buys.
- Composite index column order: equality columns first, then range; one index serves many queries.
- Index-only scans (covering indexes), and the write/space tax every index charges.

%% trellis:begin %%
## Source
[Open the original ↗](https://use-the-index-luke.com/)

## Archived copy
![[use-the-index-luke-clip]]
%% trellis:end %%
