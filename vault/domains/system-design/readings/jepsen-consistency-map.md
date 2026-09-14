---
nodes:
- distributed.consistency
- distributed.cap
url: https://jepsen.io/consistency
tags:
- canonical
- reference
- index
---
# Jepsen: Consistency Models

The definitive clickable map of consistency models — linearizability,
sequential, causal, snapshot isolation, serializability — with precise
definitions and the anomalies each one permits. This is the vocabulary
interviewers test loosely and Jepsen defines exactly.

**Extract on read:**
- The two hierarchies (single-object vs transactional) and where they meet.
- Which models survive a partition (sticky availability vs total).

%% trellis:begin %%
## Source
[Open the original ↗](https://jepsen.io/consistency)
%% trellis:end %%
