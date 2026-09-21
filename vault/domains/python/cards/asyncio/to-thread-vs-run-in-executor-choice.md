---
id: to-thread-vs-run-in-executor-choice
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
同样是把阻塞调用挪出事件循环，什么时候用 `asyncio.to_thread()`，什么时候要改用 `loop.run_in_executor()`？

## A
`asyncio.to_thread()` 是对「提交到默认线程池执行」这个最常见场景的便捷封装，写法更简洁；如果需要自定义执行器——比如指定线程池大小，或者因为是 CPU 密集任务而必须换成进程池（`ProcessPoolExecutor`）来绕开 GIL——就要用更底层的 `loop.run_in_executor(executor, func, *args)`，可以显式传入自己的执行器实例。
