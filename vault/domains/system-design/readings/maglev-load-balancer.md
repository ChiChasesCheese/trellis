---
nodes: [traffic.load-balancing]
url: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf
tags: [canonical, paper]
---
# Maglev: A Fast and Reliable Software Network Load Balancer (NSDI '16)

Google's L4 load balancer, described end to end: how traffic reaches it
(ECMP/anycast), how it picks a backend without breaking existing connections,
and how the balancer itself stays available. Short, concrete, and the answer to
"what actually sits in front of your service".

**Extract on read:**
- L4 mechanics: consistent hashing plus a connection-tracking table, so a machine joining or leaving does not reset every live flow.
- Maglev hashing — near-uniform backend spread with minimal disruption on membership change; the property plain modulo hashing lacks.
- LB high availability: ECMP across a pool of equal balancers rather than an active/passive pair, plus health checking that drains rather than drops.

%% trellis:begin %%
## Source
[Open the original ↗](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf)

## Archived copy
![[maglev-load-balancer-clip]]
%% trellis:end %%
