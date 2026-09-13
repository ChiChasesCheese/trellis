---
nodes: [caching.hierarchy]
url: https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/
tags: [canonical]
---
# Cache Reserve (Cloudflare Docs)

A production example of edge cache, Tiered Cache, and a persistent upper tier.
The page makes the hierarchy's purpose measurable: origin requests and egress
avoided, storage retained, and operations paid.

**Extract on read:**
- Draw the lookup/fill path through lower tier, upper tier, reserve, and origin.
- Explain why a hierarchy improves origin shielding but adds another dependency.
- Choose metrics that separate local hit ratio from origin avoidance.

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/)
%% trellis:end %%
