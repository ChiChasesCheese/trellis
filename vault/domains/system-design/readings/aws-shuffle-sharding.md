---
nodes: [reliability.resilience.containment, traffic.load-balancing]
url: https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
tags: [amazon]
---
# Workload isolation using shuffle-sharding (AWS Builders' Library)

The definitive explanation of shuffle sharding — assigning each customer a
random small subset of nodes so that a poison-pill workload takes down only
the customers who share its exact subset, which combinatorics makes vanishingly
few. Route 53 runs on this; it turns "one bad client hurts everyone on the
shard" into "one bad client hurts almost no one".

**Extract on read:**
- Plain sharding vs shuffle sharding: blast radius 1/shards vs ~1/(combinations).
- The combinatorial math for 2-of-8 style virtual shards and partial overlap.
- Why clients must retry across their shard members for the isolation to pay off.
- Where it applies beyond DNS: queues, load balancers, multi-tenant control planes.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/)

## Archived copy
![[aws-shuffle-sharding-clip]]
%% trellis:end %%
