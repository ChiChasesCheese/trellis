---
nodes: [distributed.skew]
url: https://research.google/pubs/consistent-hashing-with-bounded-loads/
tags: [canonical]
---
# Consistent hashing with bounded loads

The paper directly addresses the weakness ordinary consistent hashing leaves unsolved: minimal movement does not guarantee balanced load.

**Extract on read:**
- Random-looking assignment still creates overloaded bins at fleet scale.
- Explicit capacity bounds can cap imbalance while retaining low remapping cost.
- Routing must combine affinity with load limits; adding virtual nodes alone is not a hot-key policy.

%% trellis:begin %%
## Source
[Open the original ↗](https://research.google/pubs/consistent-hashing-with-bounded-loads/)
%% trellis:end %%
