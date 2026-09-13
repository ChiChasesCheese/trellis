---
nodes: [distributed.routing]
url: https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/
tags: [canonical]
---
# Maglev: A Fast and Reliable Software Network Load Balancer

Google's production paper connecting consistent hashing, routing-table convergence, connection affinity, failure handling, and commodity-fleet scale.

**Extract on read:**
- Why every router needs the same deterministic backend-selection table.
- How consistent hashing limits remapping when membership changes.
- Why connection affinity and rapid failover pull routing in opposite directions.

%% trellis:begin %%
## Source
[Open the original ↗](https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/)
%% trellis:end %%
