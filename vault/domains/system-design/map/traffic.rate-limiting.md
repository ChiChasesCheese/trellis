%% trellis:begin %%
# Rate Limiting
*Load Balancing & Traffic*

Token bucket vs sliding window, local vs distributed enforcement, and what to return when you shed.

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/system-design/map/problems.foundations.rate-limiter|Distributed Rate Limiter]], [[domains/system-design/map/problems.commerce.flash-sale|Flash Sale & High-Contention Inventory]]

## Readings
- [[stripe-rate-limiters|Scaling your API with Rate Limiters (Stripe)]]

## Cases
- [[qs-resumable-ingestion-against-a-metered-api|Resumable ingestion against a metered API]] — `quant-stroller`

## Drills
- [[design-rate-limiter|Drill: Design a distributed rate limiter]]
- [[design-flash-sale|Drill: Design a flash sale like a 10-second, 1,000-unit product drop]]

## Cards (8)
1. [[traffic-rate-limiting-vs-load-shedding]]
2. [[traffic-rate-limit-key-choice]]
3. [[traffic-token-bucket-vs-sliding-window]]
4. [[traffic-sliding-window-counter]]
5. [[traffic-rate-vs-concurrency-limiter]]
6. [[traffic-distributed-rate-limiting]]
7. [[traffic-critical-capacity-reservation]]
8. [[traffic-shedding-response]]
%% trellis:end %%

## Notes
