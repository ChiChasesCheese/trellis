---
nodes: [reliability.resilience.containment]
url: https://sre.google/sre-book/addressing-cascading-failures/
tags: [canonical]
---
# Addressing Cascading Failures (Google SRE Book, ch. 22)

The definitive chapter on how overload spreads — one overloaded server dies,
its load lands on the survivors, and the fleet collapses in a wave — and the
containment toolkit: load shedding, graceful degradation, and why you may
have to turn the whole service off to turn it back on.

**Extract on read:**
- The cascade mechanic: retries + failover concentrate load on whatever is still alive.
- Shed load early (queue caps, per-client quotas) and degrade quality before availability.
- Recovery from a death spiral: reduce load below capacity, restart cold — capacity planning must include restart cost.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/addressing-cascading-failures/)

## Archived copy
![[google-sre-cascading-failures-clip]]
%% trellis:end %%
