%% trellis:begin %%
# Timeouts, Retries & Idempotency
*Distributed Architecture*

Timeout budgets, retry safety, exponential backoff and jitter, retry storms, idempotency keys, deduplication, and hedging.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/cdn-content/map/runtimes.go-lifecycle|Go Context, Timeouts & Shutdown]], [[domains/cdn-content/map/distributed.consistency|Replication & Consistency]]

**Unlocks:** [[domains/cdn-content/map/distributed.overload|Backpressure, Load Shedding & Circuit Breaking]]

## Readings
- [[dist-aws-retries|Timeouts, retries, and backoff with jitter]]

## Cards (3)
1. [[dist-retries-budget]]
2. [[dist-retries-hedging]]
3. [[dist-retries-idempotency-key]]
%% trellis:end %%

## Notes
