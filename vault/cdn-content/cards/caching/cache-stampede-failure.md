---
id: cache-stampede-failure
node: caching.stampede
type: qa
---
## Q
The single refresh for a hot key fails. Should all collapsed waiters immediately retry?

## A
No—that recreates the herd at the worst moment. Return a bounded stale value when safe, or share the same failure with short randomized negative caching/backoff. Permit only controlled retries within the deadline and cap concurrent origin fetches. Ensure the coalescing lock is released on timeout/cancellation so the key cannot wedge forever.

## Q zh
hot key 的唯一 refresh 失败了。所有 collapsed waiter 是否应立刻 retry？

## A zh
不应，这会在最糟时刻重新制造 herd。安全时返回 bounded stale value；否则共享同一 failure，并使用短时 random negative caching/backoff。只允许 deadline 内受控 retry，并限制 concurrent origin fetch。timeout/cancellation 后必须释放 coalescing lock，避免 key 永久卡死。
