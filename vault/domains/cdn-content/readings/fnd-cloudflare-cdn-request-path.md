---
nodes: [foundations.request-path]
url: https://developers.cloudflare.com/reference-architecture/architectures/cdn/
tags: [canonical]
---
# Content Delivery Network Reference Architecture (Cloudflare)

A concrete end-to-end picture of a request with and without a CDN: DNS and
Anycast routing, the edge reverse proxy, local cache, Tiered Cache, origin, and
the response path. Read it to replace the vague box labelled "CDN" with named
hops that can each add latency or fail.

**Extract on read:**
- Draw the hit and miss paths without looking at the diagrams.
- Explain why a local POP miss does not necessarily mean an origin request.
- Name the telemetry required to attribute time to routing, cache tiers, and origin.

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.cloudflare.com/reference-architecture/architectures/cdn/)
%% trellis:end %%
