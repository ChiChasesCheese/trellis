---
id: concurrency-threadpool-future
node: concurrency.patterns
type: qa
step: 3
---
## Q
`concurrent.futures.ThreadPoolExecutor` 的 `submit()` 返回的 `Future` 对象给了你什么，任务里抛的异常去哪了？

## A
`submit(fn, *args)` 立刻返回一个 `Future`，任务在池里的某个线程异步执行；`Future` 让你可以在之后任意时刻查询这次执行的状态和结果，而不必阻塞在提交那一刻——`future.done()` 查是否完成，`future.result(timeout=...)` 阻塞等结果，`future.add_done_callback(fn)` 注册完成后要执行的回调。

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    future = pool.submit(risky_call, arg)
    ...
    value = future.result()  # 任务里如果抛了异常，这里原样重新抛出
```

任务函数内部抛出的异常不会让程序崩溃，而是被 `Future` 捕获：调用 `result()` 时会重新抛出同一个异常，`exception()` 可以在不重新抛出的情况下拿到这个异常对象；如果只挂了 `add_done_callback` 而从不调用 `result()`，异常会被悄悄吞掉，只在日志里留下痕迹。
