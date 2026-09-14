---
nodes: [distributed.partitioning, distributed.replication, distributed.consistency]
url: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
tags: [canonical, paper, amazon]
---
# Dynamo: Amazon's Highly Available Key-value Store (2007)

The paper behind DynamoDB, Cassandra, and Riak — consistent hashing, sloppy
quorums, hinted handoff, and vector clocks in one real production system.
Still the best single artifact for explaining leaderless replication.

**Extract on read:**
- Consistent hashing with virtual nodes for rebalancing.
- N/R/W tuning and what "eventually consistent" concretely meant for carts.
- The cost: conflict resolution pushed to the application.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

## Archived copy
![[dynamo-paper-clip]]
%% trellis:end %%
