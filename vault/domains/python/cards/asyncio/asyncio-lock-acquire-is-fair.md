---
id: asyncio-lock-acquire-is-fair
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
如果有 3 个协程同时在 `await lock.acquire()` 排队等待同一把 `asyncio.Lock`，锁被释放后哪个协程会先拿到？

## A
`asyncio.Lock` 的获取是公平的（fair）：一定是最早开始等待的那个协程优先拿到锁，不存在后来者插队抢占的情况，这和很多语言里锁的默认行为（不保证顺序）不同。
