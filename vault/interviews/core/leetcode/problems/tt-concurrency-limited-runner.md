---
slug: tt-concurrency-limited-runner
---
## Q
**限制并发数的异步任务执行器**｜Medium

实现 `async def run_limited(tasks, limit)`：`tasks` 是无参异步函数列表，同时最多运行 `limit` 个，一个结束立刻补上下一个，每个只调用一次。按输入顺序返回 `("fulfilled", 值)` 或 `("rejected", 异常)`（调用时同步抛出的也要记录）；`limit` 不是正整数抛 `ValueError`。

## A
**一句话。** 用 `Semaphore(limit)` 围住执行区，包装协程拿到名额后才调用任务，结果按下标写入，`TaskGroup` 等全部结束。

```python
async def run_limited(tasks, limit):
    ok = type(limit) is int  # 排除 bool
    if not ok or limit <= 0:
        raise ValueError("limit must be a positive int")
    results = [("rejected", None)] * len(tasks)
    sem = asyncio.Semaphore(limit)

    async def run_one(i, task):
        async with sem:              # 退出时自动归还名额
            try:
                results[i] = ("fulfilled", await task())
            except Exception as exc: # 不捕 BaseException，保留取消
                results[i] = ("rejected", exc)

    async with asyncio.TaskGroup() as tg:
        for i, task in enumerate(tasks):
            tg.create_task(run_one(i, task))
    return results
```

**复杂度。** 调度开销 `O(n)`，空间 `O(n)`。

**易错点。**
- 按 `limit` 个一批 `gather`：`limit = 2` 时 b 先结束，`c` 却要等 `a` 结束才开始，应立刻补上。
- `task()` 写在 `try` 外：同步抛出的 `KeyError` 会直接冒出 `run_limited`，不会记成 `rejected`。
- 只用 `limit <= 0` 检查：`True` 是 `int` 子类能通过，要单独排除。
- 捕获 `BaseException` 或裸 `except`：会吞掉 `CancelledError`，外部取消停不下来。

**追问。**
- 不用 `Semaphore` 怎么做？：起 `min(limit, n)` 个 worker 共享 `iter(enumerate(tasks))` 抢任务。
- 单任务超时？：拿到名额后用 `async with asyncio.timeout(sec)`，超时抛 `TimeoutError`，被记为 `rejected`。

**同模式。** LC 1114 按序打印、LC 1188 设计有限阻塞队列、LC 1226 哲学家进餐
