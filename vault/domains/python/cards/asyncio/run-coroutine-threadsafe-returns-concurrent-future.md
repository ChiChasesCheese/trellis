---
id: run-coroutine-threadsafe-returns-concurrent-future
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
从一个不是运行事件循环的普通 OS 线程里，想把一个协程提交给正在跑的事件循环去执行，应该用什么 API？它返回的是 `asyncio.Future` 还是别的类型？

## A
用 `asyncio.run_coroutine_threadsafe(coro, loop)`：它是专门设计成可以从别的 OS 线程安全调用的函数（不同于绝大多数 asyncio API），返回的是一个 `concurrent.futures.Future`（不是 `asyncio.Future`），可以直接在调用方线程里用 `future.result(timeout=...)` 同步阻塞等待结果，超时会抛 `TimeoutError`。
