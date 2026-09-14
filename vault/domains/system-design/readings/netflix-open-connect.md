---
nodes: [networking.cdn]
url: https://openconnect.netflix.com/Open-Connect-Overview.pdf
tags: [canonical]
---
# Netflix Open Connect Overview

The clearest public description of a *push* CDN in production: Netflix decides
in advance what each edge appliance should hold, fills it during off-peak
hours, and steers clients to it. The counterexample to the pull/lazy model the
Cloudflare docs describe, which is exactly what makes the push-vs-pull
trade-off concrete.

**Extract on read:**
- Proactive fill: popularity-ranked content pushed to appliances during a nightly fill window, so the edge never takes a cold-miss storm.
- Where the edge lives — embedded inside ISP networks vs at internet exchanges — and why placement, not cache size, sets the hit rate.
- What belongs at the edge: large immutable objects with predictable demand; everything personalized (the control plane) stays in the cloud.

%% trellis:begin %%
## Source
[Open the original ↗](https://openconnect.netflix.com/Open-Connect-Overview.pdf)

## Archived copy
![[netflix-open-connect-clip]]
%% trellis:end %%
