%% trellis:begin %%
# Content Delivery Network
*Design Problems / Building Blocks & Warm-ups*

Request routing, tiered caches, purge and origin shielding for static and large-file delivery.

**Requires:** [[domains/system-design/map/networking.cdn|CDN]], [[domains/system-design/map/caching.placement|Cache Placement]]

## Readings
- [[solution-cdn|设计题解：内容分发网络（Content Delivery Network，CDN）]]
- [[src-akamai-nygren-paper-cdn|The Akamai Network: A Platform for High-Performance Internet Applications]]
- [[src-cloudflare-anycast-cdn|A Brief Primer on Anycast]]
- [[src-cloudflare-purge-cdn|Instant Purge: invalidating cached content in under 150ms]]
- [[src-cloudflare-tiered-cache-cdn|Tiered Cache Smart Topology]]
- [[src-fastly-shielding-cdn|Let the edge work for you: How shielding improves performance]]

## Drills
- [[design-cdn|Drill: Design a content delivery network (CDN)]]

## Cards (8)
1. [[problems-cdn-shield-reduces-origin-qps-5x]]
2. [[problems-cdn-anycast-vs-geodns-failover-granularity]]
3. [[problems-cdn-cache-key-scope-and-vary]]
4. [[problems-cdn-purge-not-atomic-versioned-urls]]
5. [[problems-cdn-bdp-limits-parallel-segments-fix]]
6. [[problems-cdn-viral-object-shield-20x]]
7. [[problems-cdn-pop-failure-5pct-neighbor-overload]]
8. [[problems-cdn-10x-needs-second-shield-tier]]
%% trellis:end %%

## Notes
