---
nodes: [traffic.rate-limiting, caching.placement, distributed.time, problems.foundations.rate-limiter]
tags: [classic, problem]
---
# Drill: Design a distributed rate limiter

Design rate limiting for a public API platform: per-key quotas, multiple
gateway instances, low added latency.

**Constraints to state and honor**
- 100k req/s across ~20 gateway nodes; p99 added latency budget < 2 ms.
- Quotas per API key and per endpoint; both burst and sustained limits.
- A central store outage must not take the API down.

**Grading points**
- Algorithm choice and memory cost per key ([[traffic-token-bucket-vs-sliding-window]], [[traffic-sliding-window-counter]], [[problems-rate-limiter-sliding-log-vs-counter-memory]], [[problems-rate-limiter-token-bucket-vs-counter-split]]).
- Local vs centralized enforcement; sync interval vs accuracy trade ([[traffic-distributed-rate-limiting]], [[problems-rate-limiter-local-first-hybrid-enforcement]], [[problems-rate-limiter-check-volume-forces-shard-count]]).
- Fail-open vs fail-closed when the counter store is down ([[problems-rate-limiter-asymmetric-fail-open-closed]]).
- Per-key limits alone don't protect the backend — the multi-layer quota model ([[problems-rate-limiter-three-layer-quota-model]]).
- What you return on reject and why ([[traffic-shedding-response]]).
- Clock skew effects on window boundaries ([[distributed-failure-detection]]).
- A single hot key overloading one shard, and why more shards don't fix it ([[problems-rate-limiter-single-key-shard-hotspot]]).

**Solution**: [[solution-rate-limiter]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
