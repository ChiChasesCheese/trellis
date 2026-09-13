---
nodes: [foundations.concurrency]
url: https://sre.google/sre-book/addressing-cascading-failures/
tags: [canonical]
---
# Addressing Cascading Failures (Google SRE)

Google's production treatment of overload connects thread pools, queue bounds,
latency, load shedding, and graceful degradation. It is the right bridge from
concurrency primitives to the system-level consequence of allowing unlimited
work into a serving process.

**Extract on read:**
- Why a long queue creates latency but not service capacity.
- How bounded queues and early rejection prevent resource exhaustion.
- Which overload paths must be exercised continuously, not only during incidents.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/addressing-cascading-failures/)
%% trellis:end %%
