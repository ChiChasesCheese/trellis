---
nodes: [traffic.gateways]
url: https://microservices.io/patterns/apigateway.html
tags: [canonical, reference]
---
# API Gateway Pattern (microservices.io, Chris Richardson)

The canonical pattern write-up for the front-door component: what a gateway
centralizes, the Backends-for-Frontends variant, and the drawbacks section
interviewers expect you to volunteer.

**Extract on read:**
- What belongs at the gateway: TLS termination, authn, routing, quotas, aggregation.
- BFF: one gateway per client type instead of one god-gateway.
- The bill: extra hop latency, a new SPOF to make highly available, a bottleneck team.

%% trellis:begin %%
## Source
[Open the original ↗](https://microservices.io/patterns/apigateway.html)

## Archived copy
![[microservices-io-api-gateway-clip]]
%% trellis:end %%
