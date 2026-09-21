---
id: asyncio-future-vs-concurrent-futures-future
node: asyncio.futures
type: qa
source: python-docs
---
## Q
`asyncio.Future` 是仿照 `concurrent.futures.Future`（线程/进程池那套）设计的，两者最关键的行为差异是什么？

## A
`asyncio.Future` 可以被 `await`，而 `concurrent.futures.Future` 不能；`asyncio.Future` 的 `result()`/`exception()` 不接受 `timeout` 参数、且在还没 done 时会抛 `InvalidStateError`；`asyncio.Future` 也不兼容 `concurrent.futures.wait()`/`as_completed()` 这类线程池专用的等待函数，两者是两套不能混用的 API。
