---
nodes:
- networking.cdn
- caching.placement
url: https://developers.cloudflare.com/cache/
tags:
- reference
- index
---
# How CDN caching actually works (Cloudflare docs)

Vendor docs, but the most concrete public description of cache keys, TTL
override hierarchies, tiered caching, and purge mechanics at a real edge.

**Extract on read:**
- What forms the cache key and why query-string handling is a design choice.
- Tiered/hierarchical caching to protect origins from regional misses.
- Purge-by-tag vs purge-by-URL, and their propagation costs.

Related cards: [[networking-cdn-cache-key]], [[networking-push-vs-pull-cdn]]

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.cloudflare.com/cache/)
%% trellis:end %%
