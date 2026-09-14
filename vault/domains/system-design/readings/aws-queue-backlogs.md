---
nodes: [async.queues]
url: https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
tags: [canonical, amazon]
---
# Avoiding insurmountable queue backlogs (AWS Builders' Library)

The best operational essay on queues: how the durability that makes queues
attractive becomes a liability when a backlog grows past what consumers can
ever drain. Covers backpressure, shuffle sharding of queues, and sideline
queues — the failure modes interviewers actually probe.

**Extract on read:**
- Queues turn availability problems into latency problems — until the backlog exceeds drain capacity.
- Bounding queues and shedding at enqueue time beats unbounded "durability".
- Per-tenant fairness: separate or shuffle-shard queues so one hot producer can't starve everyone.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/)

## Archived copy
![[aws-queue-backlogs-clip]]
%% trellis:end %%
