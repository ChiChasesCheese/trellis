---
nodes: [reliability.multi-region]
url: https://aws.amazon.com/builders-library/static-stability-using-availability-zones/
tags: [canonical, amazon]
---
# Static stability using Availability Zones (AWS Builders' Library)

The best public writeup of how AWS actually survives zone loss: pre-provision
capacity so failover requires *no* control-plane action at the worst moment.
The reasoning transfers directly to multi-region design — active-active vs
active-passive, and why untested failover is fiction.

**Extract on read:**
- Static stability: keep running when a dependency fails, without needing to launch/scale anything mid-incident.
- Data plane vs control plane — never put a control-plane dependency in your recovery path.
- Over-provision N+1 across zones/regions; "failover automation" that must make changes under stress is the risk itself.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/)

## Archived copy
![[aws-static-stability-clip]]
%% trellis:end %%
