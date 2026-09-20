%% trellis:begin %%
# Distributed Rate Limiter
*Design Problems / Building Blocks & Warm-ups*

Per-key quotas enforced across many gateways inside a 2 ms budget, and what happens when the counter store is down.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/traffic.rate-limiting|Rate Limiting]]

## Readings
- [[solution-rate-limiter|设计题解：分布式速率限制器（Distributed Rate Limiter）]]
- [[src-cloudflare-rate-limiter|Counting things: A lot of a different things]]
- [[src-hellointerview-rate-limiter|Distributed Rate Limiter]]
- [[src-stripe-rate-limiter|Scaling your API with rate limiters]]

## Drills
- [[design-rate-limiter|Drill: Design a distributed rate limiter]]

## Cards (8)
1. [[problems-rate-limiter-check-volume-forces-shard-count]]
2. [[problems-rate-limiter-three-layer-quota-model]]
3. [[problems-rate-limiter-local-first-hybrid-enforcement]]
4. [[problems-rate-limiter-sliding-log-vs-counter-memory]]
5. [[problems-rate-limiter-token-bucket-vs-counter-split]]
6. [[problems-rate-limiter-asymmetric-fail-open-closed]]
7. [[problems-rate-limiter-single-key-shard-hotspot]]
8. [[problems-rate-limiter-10x-shard-count-growth]]
%% trellis:end %%

## Notes
