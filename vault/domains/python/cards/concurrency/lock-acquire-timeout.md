---
id: lock-acquire-timeout
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
`lock.acquire(blocking=True, timeout=-1)` 的返回值和 `timeout` 的语义是什么？

## A
返回值是布尔值：成功拿到锁返回 `True`，因为超时或 `blocking=False` 且锁被占用而没拿到返回 `False`。`timeout=-1`（默认）表示无限等待；给一个正的浮点数表示最多等待这么多秒。`blocking=False` 与显式指定正数 `timeout` 不能同时使用（会报错）。对一把已解锁的锁调用 `release()` 会抛出 `RuntimeError`——释放操作没有“幂等”保护。
