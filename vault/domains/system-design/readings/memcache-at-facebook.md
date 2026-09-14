---
nodes: [caching.invalidation, caching.placement]
url: https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala
tags: [canonical, paper]
---
# Scaling Memcache at Facebook (NSDI '13)

The definitive real-world paper on cache invalidation and placement at
extreme scale — leases against stampedes and stale sets, invalidation
pipelines off the database log, and regional cache tiers.

**Extract on read:**
- Leases: one flight per missed key, solving both thundering herd and stale-set races.
- Invalidations driven from the DB commit log (McSqueal), not from application code.
- Placement layers: web-server local cache → regional pools → cross-region replicas, each with its own consistency debt.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala)

## Archived copy
![[memcache-at-facebook-clip]]
%% trellis:end %%
