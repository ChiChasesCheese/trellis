---
nodes: [distributed.consensus]
url: https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
tags: [amazon]
---
# Leader election in distributed systems (AWS Builders' Library)

A practitioner's view of leader election: what having a single leader buys
(simple reasoning, cheap ordering), what it costs (single point of failure,
scaling ceiling, correlated risk), and the failure patterns — split brain,
stale leases, leaders that keep working after losing leadership. Grounds the
Raft/Paxos theory in how AWS actually deploys leadered systems.

**Extract on read:**
- Lease-based election on a lock service (DynamoDB lock client) vs consensus-native election.
- Fencing: why a deposed leader must be prevented from acting, and how fencing tokens work.
- Heartbeats, lease length, and the availability/failover-time trade-off.
- When to avoid a leader entirely (partition the work, or make operations idempotent).

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/)

## Archived copy
![[aws-leader-election-clip]]
%% trellis:end %%
