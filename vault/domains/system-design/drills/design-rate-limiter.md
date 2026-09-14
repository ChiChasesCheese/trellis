---
nodes: [traffic.rate-limiting, caching.placement, distributed.time]
tags: [classic]
---
# Drill: Design a distributed rate limiter

Design rate limiting for a public API platform: per-key quotas, multiple
gateway instances, low added latency.

**Constraints to state and honor**
- 100k req/s across ~20 gateway nodes; p99 added latency budget < 2 ms.
- Quotas per API key and per endpoint; both burst and sustained limits.
- A central store outage must not take the API down.

**Grading points**
- Algorithm choice and memory cost per key ([[traffic-token-bucket-vs-sliding-window]], [[traffic-sliding-window-counter]]).
- Local vs centralized enforcement; sync interval vs accuracy trade ([[traffic-distributed-rate-limiting]]).
- Fail-open vs fail-closed when the counter store is down.
- What you return on reject and why ([[traffic-shedding-response]]).
- Clock skew effects on window boundaries ([[distributed-failure-detection]]).

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
