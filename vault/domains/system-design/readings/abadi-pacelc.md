---
nodes: [distributed.cap]
url: https://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html
tags: [canonical]
---
# Problems with CAP, and Yahoo's little known NoSQL system (Daniel Abadi)

The post where PACELC was born. Abadi shows CAP is asymmetric and misleading —
"consistency vs availability" only describes the rare partition case, while the
trade-off you actually live with every day is consistency vs *latency*. He then
walks PNUTS as the system that picks the unpopular corner.

**Extract on read:**
- Why "CA" is not a real category, and why CAP's C, A and P are not three peers you pick two of.
- PACELC: if Partition then A-vs-C, Else L-vs-C — the else-branch is the one that governs normal operation.
- Where real systems land: Dynamo/Cassandra (PA/EL), PNUTS (PC/EL), fully-ACID replicated stores (PC/EC).

%% trellis:begin %%
## Source
[Open the original ↗](https://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html)

## Archived copy
![[abadi-pacelc-clip]]
%% trellis:end %%
