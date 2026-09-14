---
nodes: [distributed.time]
url: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
tags: [canonical]
---
# How to do distributed locking (Kleppmann, the Redlock critique)

The sharpest short essay on why wall clocks, timeouts, and process pauses
cannot be trusted in a distributed system — argued through a concrete
takedown of Redis's Redlock. Everything the `distributed.time` node claims,
demonstrated on a real design.

**Extract on read:**
- Why leases based on elapsed wall-clock time break under GC pauses and clock drift.
- Fencing tokens: monotonically increasing epochs as the actual safety mechanism.
- Efficiency locks vs correctness locks — only the latter needs consensus.

%% trellis:begin %%
## Source
[Open the original ↗](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)

## Archived copy
![[kleppmann-distributed-locking-clip]]
%% trellis:end %%
