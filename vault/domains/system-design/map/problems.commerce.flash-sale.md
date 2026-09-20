%% trellis:begin %%
# Flash Sale & High-Contention Inventory
*Design Problems / Commerce, Booking & Money*

A million buyers, a thousand items, ten seconds: admission control and atomic decrement.

**Requires:** [[domains/system-design/map/traffic.rate-limiting|Rate Limiting]], [[domains/system-design/map/distributed.transactions.concurrency-control|Concurrency Control]]

## Readings
- [[solution-flash-sale|设计题解：秒杀与高竞争库存（Flash Sale & High-Contention Inventory）]]
- [[src-alibabacloud-flash-sale|System Stability Assurance for Large Scale Flash Sales]]
- [[src-redis-benchmark-flash-sale|Redis benchmark]]
- [[src-redis-eval-flash-sale|Scripting with Lua]]
- [[src-shopify-flash-sale|Surviving Flashes of High-Write Traffic Using Scriptable Load Balancers (Part I & II)]]

## Drills
- [[design-flash-sale|Drill: Design a flash sale like a 10-second, 1,000-unit product drop]]

## Cards (8)
1. [[problems-flash-sale-hot-key-safety-margin]]
2. [[problems-flash-sale-bottleneck-order]]
3. [[problems-flash-sale-lottery-vs-first-come-first-served]]
4. [[problems-flash-sale-lua-atomic-check-and-decrement]]
5. [[problems-flash-sale-redis-vs-db-division-of-labor]]
6. [[problems-flash-sale-reservation-ttl-vs-ticket-booking]]
7. [[problems-flash-sale-undersell-vs-oversell]]
8. [[problems-flash-sale-10x-100x-evolution]]
%% trellis:end %%

## Notes
