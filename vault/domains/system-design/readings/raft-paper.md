---
nodes: [distributed.consensus]
url: https://raft.github.io/raft.pdf
tags: [canonical, paper]
---
# In Search of an Understandable Consensus Algorithm (Raft)

The consensus algorithm you'll actually be asked about. Read sections 5
(the algorithm) and 8 (client interaction); skim the rest. The visualization
at https://thesecretlivesofdata.com/raft/ is the fastest first pass.

**Extract on read:**
- Leader election: randomized timeouts, term numbers as logical clocks.
- Log replication and the commit rule (majority match).
- Why a deposed leader can't corrupt state — and where fencing tokens fit.

%% trellis:begin %%
## Source
[Open the original ↗](https://raft.github.io/raft.pdf)

## Archived copy
![[raft-paper-clip]]
%% trellis:end %%
