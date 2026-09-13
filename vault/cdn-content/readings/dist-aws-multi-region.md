---
nodes: [distributed.cross-region]
url: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/multi-region-architecture.html
tags: [canonical]
---
# AWS multi-Region architecture guidance

A first-party view of why systems go multi-Region: availability, latency, recovery objectives, sovereignty, and the operational consequences of replication and failover.

**Extract on read:**
- Active-active and active-passive are state and recovery choices, not topology labels.
- Region loss requires spare survivor capacity and tested traffic steering.
- Replication, failover, residency, and global observability must be designed together.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/multi-region-architecture.html)
%% trellis:end %%
