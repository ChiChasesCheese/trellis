---
id: caching-lease-cas
node: caching.invalidation
type: qa
---
## Q
Even with delete-on-write, cache-aside has a residual stale-set race. How do memcached *leases* (Facebook) close it?

## A
The race: reader misses, reads the old value from the DB; a write commits and deletes the key; the reader then sets its stale value — wrong until TTL ([[caching-delete-not-update]]).

**Leases**: on a miss, the cache hands the reader a lease token; the reader may only set the key *with* that token. Any delete arriving in between **invalidates outstanding leases**, so the stale set is refused.

Bonus: leases throttle stampedes — only the current lease holder may repopulate; other missers briefly wait or serve the last stale value.

## Q zh
即使有 delete-on-write，cache-aside 也有一个残留的过时集合竞争。memcached *租约*（Facebook）如何关闭它？

## A zh
竞争：读者 miss，从 DB 读旧值；写提交并删除键；读者然后设置其过时值 — 错误直到 TTL（[[caching-delete-not-update]]）。

**租约**：在 miss 时，缓存向读者提交租约令牌；读者只能用那个令牌 *设置* 键。任何在两者之间到达的删除 **使未完成的租约无效**，所以过时的集合被拒绝。

奖励：租约限制尖峰 — 只有当前租约持有者可能重新填充；其他 missers 短暂等待或提供最后的过时值。
