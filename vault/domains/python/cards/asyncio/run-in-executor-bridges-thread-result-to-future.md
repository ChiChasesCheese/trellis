---
id: run-in-executor-bridges-thread-result-to-future
node: asyncio.futures
type: qa
source: python-docs
---
## Q
`await loop.run_in_executor(None, blocking_io)` 把一个跑在线程池里的阻塞函数结果，是怎么接回 `await` 语法的？

## A
`run_in_executor()` 返回的是一个 `asyncio.Future` 对象：线程池里的函数执行完毕后，其返回值（或异常）被写回这个 Future，Future 随之变成 done 状态并唤醒等待它的协程。这样一个同步阻塞函数的结果就被「桥接」成了可以直接 `await` 的对象，调用方完全不需要关心背后是线程在跑。
