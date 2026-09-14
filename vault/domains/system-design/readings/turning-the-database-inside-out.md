---
nodes: [analytics.derived, async.streaming, async.log]
url: https://martin.kleppmann.com/2015/03/04/turning-the-database-inside-out.html
tags: [canonical, talk]
---
# Turning the Database Inside-Out (Kleppmann)

The talk/essay that reframes caches, indexes, and materialized views as
derived, recomputable projections of an event log — the mental model behind
the whole `analytics.derived` node and half of modern streaming architecture.

**Extract on read:**
- Why "cache invalidation is hard" is a symptom of hand-maintained derived state.
- Materialized views maintained by stream processors instead of app code.
- Where this breaks down: read-your-writes against async views.

Related cards: [[async-cdc-mechanism]], [[async-materialized-view-refresh]]

%% trellis:begin %%
## Source
[Open the original ↗](https://martin.kleppmann.com/2015/03/04/turning-the-database-inside-out.html)

## Archived copy
![[turning-the-database-inside-out-clip]]
%% trellis:end %%
