---
id: semaphore-vs-boundedsemaphore-extra-release
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
对一个初始值为 2 的 `Semaphore` 只 `acquire()` 过一次，却连续 `release()` 两次，会出错吗？换成 `BoundedSemaphore` 呢？

## A
普通 `Semaphore` 允许 `release()` 调用次数多于 `acquire()` 次数，内部计数器会照样往上加，不会报错；而 `BoundedSemaphore` 会在计数器超过初始值时主动抛出 `ValueError`，用来在开发阶段就暴露「release 多写了一次」这类配对错误。
