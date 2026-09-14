---
nodes: [distributed.consistency]
url: https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
tags: [canonical]
---
# Dynamo: Amazon's highly available key-value store

The original production paper for leaderless replication, tunable quorums, vector clocks, sloppy quorum, hinted handoff, and read repair.

**Extract on read:**
- Availability during partitions creates versions that must later reconcile.
- `N`, `R`, and `W` are operational choices surrounded by membership and failure assumptions.
- Version metadata is what lets the system distinguish stale and concurrent values.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store)
%% trellis:end %%
