---
id: cc-toolbox-cache-expiry-index
node: toolbox.cache
type: qa
---
## Q
10^4 entries, 10^5 "give me any free one" calls, and entries free themselves when their lock expires. Scanning all entries per call is 10^9 steps. Structure?

## A
**Two heaps plus a version counter.** One heap ordered by expiry holding locked entries, one ordered by the recency key holding entries believed free.

- On each call, first drain the expiry heap while `heap[0].expiry <= t` and push those entries into the free heap.
- Then pop the free heap, skipping entries whose version no longer matches ([[cc-toolbox-heap-lazy-invalidation]]).
- **Re-check the popped entry against `t`** instead of trusting the heap — that keeps the answer correct even when queries arrive with non-monotonic timestamps, which a hidden test will do.
- Cost per call is O(log n) amortized instead of O(n); the memory cost is the stale entries, bounded by the number of state changes.

The same two-index shape covers "expiring reservations", "leases", and "TTL cache with an eviction order" ([[cc-toolbox-cache-ttl]]).

## Q zh
10^4 个条目、10^5 次「给我任意一个空闲的」调用，而条目在锁到期时自行释放。每次调用扫描所有条目是 10^9 步。用什么结构？

## A zh
**两个堆加一个版本计数器。** 一个按到期时间排序、装被锁定的条目，另一个按新近度 key 排序、装被认为空闲的条目。

- 每次调用先排空到期堆：当 `heap[0].expiry <= t` 时把那些条目推进空闲堆。
- 然后从空闲堆 pop，跳过版本已不匹配的条目（[[cc-toolbox-heap-lazy-invalidation]]）。
- **对 pop 出来的条目再用 `t` 复核一次**，而不是信任堆 —— 这样即使查询的时间戳非单调（隐藏测试一定会这么干）答案也仍然正确。
- 每次调用摊销 O(log n) 而不是 O(n)；内存代价是那些过期条目，其数量以状态变更次数为界。

同样的双索引形态适用于「会过期的预约」「租约」和「带淘汰顺序的 TTL 缓存」（[[cc-toolbox-cache-ttl]]）。
