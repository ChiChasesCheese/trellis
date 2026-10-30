---
id: tlc-tt-concurrency-limited-runner-4-followup
node: p2.tt-concurrency-limited-runner
type: qa
step: 4
---
## Q
**限制并发数的异步任务执行器**｜追问

信号量版 `run_limited` 写完后，面试官接着问：（1）不用 `Semaphore` 怎么写？（2）给每个任务加单任务超时？（3）整次调用被取消、或者某个任务被取消时怎么处理？

## A
1. **不用 `Semaphore`：固定 worker 池。** 名额不再是计数器，而是 worker 的个数：起 `min(limit, n)` 个 worker，共享一个任务迭代器，做完一个就自己取下一个，天然“一个结束立刻补上”。事件循环是单线程，`next()` 之间不会被抢占，不需要锁。只建 `limit` 个 Task，`n = 10^5` 时比信号量版（同时建 `n` 个 Task）省；信号量版胜在短、上限一眼可见。

```python
async def run_limited_pool[T](tasks: list[Callable[[], Awaitable[T]]], limit: int) -> list[Outcome]:
    results: list[Outcome] = [("rejected", None)] * len(tasks)
    todo = iter(enumerate(tasks))                    # 所有 worker 共享的取任务游标

    async def worker() -> None:
        for i, task in todo:
            try:
                results[i] = ("fulfilled", await task())
            except Exception as exc:
                results[i] = ("rejected", exc)

    async with asyncio.TaskGroup() as tg:
        for _ in range(min(limit, len(tasks))):
            tg.create_task(worker())
    return results
```

   （`limit` 的校验与前面相同，这里省略。）
2. **单任务超时。** 把 `await task()` 包进 `async with asyncio.timeout(sec):`，放在拿到名额**之后**，等名额的时间不算；到期抛 `TimeoutError`，被 `except Exception` 记成 `rejected`，名额随 `async with sem` 归还。
3. **取消。** 整次调用被取消时，`TaskGroup` 把取消传给所有子任务，`except Exception` 不拦 `CancelledError`，没开始的任务不再被调用：6 个任务、`limit = 2`，运行 30ms 后取消，只有任务 0、1 被调用过，且都收到取消。只想取消单个任务时，在包装函数里加 `except asyncio.CancelledError:`，用 `asyncio.current_task().cancelling()` 判断：大于 0 是整次调用被取消，继续 `raise`；否则记 `("cancelled", None)`。

**Python 提醒**：`TimeoutError` 是 `Exception` 的子类，`CancelledError` 是 `BaseException` 的子类，所以 `except Exception` 能兜住超时、放过取消；3.11 起 `asyncio.TimeoutError` 就是内置 `TimeoutError`。
