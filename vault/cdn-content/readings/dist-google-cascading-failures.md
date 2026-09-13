---
nodes: [distributed.overload]
url: https://sre.google/sre-book/addressing-cascading-failures/
tags: [canonical]
---
# Addressing cascading failures

Google SRE's full causal model of overload: queues, retries, resource coupling, health-check collapse, load shedding, deadline propagation, and recovery from a death spiral.

**Extract on read:**
- Overload reduces useful throughput while secondary symptoms multiply.
- Bounded queues, early rejection, graceful degradation, and retry budgets contain the feedback loop.
- Recovery may require cutting load far below normal until capacity and caches stabilize.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/addressing-cascading-failures/)
%% trellis:end %%
