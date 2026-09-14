---
nodes: [traffic.load-balancing]
url: https://web.archive.org/web/20180115194524/https://blog.envoyproxy.io/introduction-to-modern-network-load-balancing-and-proxying-a57f6ff80236
tags: [canonical]
---
# Introduction to Modern Network Load Balancing and Proxying (Matt Klein)

Written by Envoy's creator, this is the one essay that covers the entire
load-balancing landscape — L4 vs L7, algorithms, health checking, DNS/middle/
sidecar topologies — with production judgment behind every claim.
(Medium no longer serves blog.envoyproxy.io; this is the Internet Archive copy.)

**Extract on read:**
- Why L4 breaks down for multiplexed protocols (HTTP/2, gRPC) and L7 fixes it.
- Algorithms in practice: round robin vs least-request vs power-of-two-choices.
- LB high availability itself: DNS, anycast, and consistent-hash ECMP at the edge.

%% trellis:begin %%
## Source
[Open the original ↗](https://web.archive.org/web/20180115194524/https://blog.envoyproxy.io/introduction-to-modern-network-load-balancing-and-proxying-a57f6ff80236)

## Archived copy
![[modern-load-balancing-matt-klein-clip]]
%% trellis:end %%
