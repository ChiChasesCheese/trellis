---
nodes: [asyncio.coroutines-tasks, asyncio.gather-wait-timeout, asyncio.debugging, asyncio.sync-primitives, asyncio.cancellation]
tags: [drill, interview]
---
# Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug

```python
import asyncio

async def fetch_page(page):
    await asyncio.sleep(0.1)
    if page == 3:
        raise ValueError(f"bad page {page}")
    return [f"item-{page}-{i}" for i in range(3)]

async def fetch_all(n_pages):
    tasks = [asyncio.create_task(fetch_page(p)) for p in range(n_pages)]
    results = asyncio.gather(*tasks)
    return results

def main():
    all_items = fetch_all(5)
    print(all_items)

main()
```

跑起来什么都没打印（或者打印出一个奇怪的对象），也没有任何异常。

**限制与要求**
- 先只读代码找出全部 bug，再动手改；不许边读边改。
- 每找到一个 bug 要说清楚「为什么这是 bug」，不能只说「这里少了 await」。
- 修完之后还要加上：`Semaphore` 限制同时在途的页数、`asyncio.wait_for` 给整体加超时。
- 15 分钟内完成，改完的版本要能跑。

**分关要求**
- 第 1 关（约 6 分钟）：只列出 bug，不改代码。
- 第 2 关（约 6 分钟）：改出能正确运行、能打印结果或正确抛出 `page 3` 异常的版本。
- 第 3 关（约 3 分钟）：加 `Semaphore(N)` 限流 + `wait_for` 超时；追问取消语义——超时触发后，`fetch_page(3)` 会立刻停止执行吗？

**评分点（强答案会命中）**
- `main()` 是普通同步函数直接调用 `fetch_all(5)`，而 `fetch_all` 是协程函数：调用它只会构造并返回一个协程对象，函数体完全不会执行，`print(all_items)` 打印的是协程对象本身，不是结果——必须用 `asyncio.run(fetch_all(5))` 或在事件循环里 `await` 它 [[calling-coroutine-function-only-builds-object]] [[never-awaited-runtimewarning]]
- `results = asyncio.gather(*tasks)` 这一行本身只是构造了一个可等待对象（尽管 `tasks` 都已经是 `Task`），`fetch_all` 里没有 `await results` 就直接 `return`，等于把这个 `gather` 的调用结果原样返回、从未被驱动执行；`gather` 会自动把传入的裸协程包装成 `Task`，但传 `Task` 时它只是照单全收，问题出在外层忘了 `await` [[gather-schedules-coroutines-as-tasks]]
- `asyncio.create_task(fetch_page(p))` 立即把协程调度进事件循环的待运行队列并返回，但不会同步执行；真正开始跑要等到当前协程下一次让出控制权（`await`）之后——如果外层从没 `await` 任何东西，这些 Task 可能从未真正被驱动 [[create-task-schedules-not-runs-synchronously]]
- 如果只 `create_task` 却从不 `await` 对应的 Task 去取结果，`page == 3` 抛出的异常不会立刻传播给任何人，只有这个 Task 被垃圾回收时才会打印一条 `Task exception was never retrieved` 日志——这是「程序看起来正常但后台任务默默炸了」的典型根因 [[task-exception-never-retrieved-log]]
- 限流 + 重试的标准组合：用 `asyncio.Semaphore(N)` 限制同时在途的请求数，每个页面的抓取协程内部再包一层重试逻辑，最后用 `gather`/`TaskGroup` 并发收集，两层互相独立可以叠加 [[paginated-fetch-semaphore-plus-retry-pattern]]
- `wait_for(coro, timeout)` 超时后不是立刻抛异常：会先 `cancel()` 内部任务，等待这次取消真正完成之后才抛 `TimeoutError`，所以实际耗时可能略超过设定的 timeout [[wait-for-timeout-cancels-and-waits]]
- `task.cancel()` 不会让任务立刻停止，只是发出请求，事件循环会在目标协程下一次执行到 `await` 让出控制权时才把 `CancelledError` 注入进去 [[task-cancel-injects-at-next-await]]
- `asyncio.CancelledError` 直接继承自 `BaseException` 而不是 `Exception`，所以业务代码里常见的 `except Exception:` 不会意外吞掉取消信号 [[cancellederror-subclasses-baseexception]]
- 协程里的清理逻辑该用 `try/finally` 而不是只用 `try/except`；如果显式捕获了 `CancelledError`，清理完后通常要重新 `raise`，否则会打乱取消请求本该传达的「这里要停止」语义 [[finally-cleanup-runs-on-cancellation]]

**参考答案**
三个 bug：① `main()` 用同步方式调用协程函数 `fetch_all`，从没进入事件循环；② `fetch_all` 内部 `asyncio.gather(*tasks)` 之后没有 `await`；③ 即使 ① ② 都不发生，`page == 3` 抛出的异常如果只挂在某个从未被 `await` 的 Task 上也会被静默丢弃。

```python
import asyncio

async def fetch_page(sem, page):
    async with sem:
        await asyncio.sleep(0.1)
        if page == 3:
            raise ValueError(f"bad page {page}")
        return [f"item-{page}-{i}" for i in range(3)]

async def fetch_all(n_pages, concurrency=3, timeout=2.0):
    sem = asyncio.Semaphore(concurrency)
    tasks = [asyncio.create_task(fetch_page(sem, p)) for p in range(n_pages)]
    return await asyncio.wait_for(
        asyncio.gather(*tasks, return_exceptions=True), timeout
    )

async def main():
    print(await fetch_all(5))

asyncio.run(main())
```

`asyncio.run(main())` 才真正驱动事件循环；`await asyncio.wait_for(asyncio.gather(...), timeout)` 补上了缺失的 await，`return_exceptions=True` 让 `page 3` 的异常作为结果之一收集起来而不是让整个 `gather` 提前失败。

第 3 关：`wait_for` 超时触发后不会让 `fetch_page(3)` 立刻停止——它先对内部的 `gather` 任务调用 `cancel()`，`CancelledError` 要等到 `fetch_page` 下一次执行到 `await asyncio.sleep(...)` 这个挂起点才会被注入；`wait_for` 会等这次取消真正传播完成后才抛出 `TimeoutError`，所以整体耗时会比 `timeout` 参数略长一点，而不是精确等于它。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
