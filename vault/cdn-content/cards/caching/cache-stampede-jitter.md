---
id: cache-stampede-jitter
node: caching.stampede
type: qa
---
## Q
Why does adding random jitter to TTLs help after a fleet-wide cache warm, and what problem remains?

## A
Identical TTLs make entries loaded together expire together, creating a synchronized origin spike. Jitter spreads expirations over time. It does not protect a single extremely hot key when it expires, nor a total cache flush; pair it with request coalescing, early/background refresh, stale serving, and bounded origin load.

## Q zh
fleet-wide cache warm 后，为什么给 TTL 加 random jitter 有帮助？还剩什么问题？

## A zh
相同 TTL 会让一起加载的 entry 同时过期，产生同步 origin spike。jitter 把 expiry 分散到时间轴上。但它不能保护单个极热 key 的到期，也不能解决整库 flush；还需配合 request coalescing、early/background refresh、stale serving 与 bounded origin load。
