---
slug: promise-pool
---
## Q
**LC 2636 Promise 对象池**｜Medium

（原题为 JavaScript，这里用 Python。）给一组异步函数 `functions`（每个返回一个可等待对象）和并发上限 `n`。同时最多运行 `n` 个，一个结束就立即启动下一个，全部完成后返回。

## A
**一句话。** 起 `n` 个工人协程，共享同一个迭代器：每个工人不断从迭代器里取下一个函数并 `await` 它，迭代器取尽就退出，所以任何时刻最多 `n` 个在跑。

```python
async def promise_pool(functions, n):
    it = iter(functions)                 # 所有工人共享同一个迭代器

    async def worker():
        for f in it:                     # 取下一个任务
            await f()

    await asyncio.gather(*(worker() for _ in range(n)))
```

**复杂度。** 调度开销 `O(len(functions))`，并发度不超过 `n`。

**易错点。**
- 一开始就调用全部函数：并发数会超过 `n`，要等有空位才调用。
- 每个工人各自 `iter(functions)`：会重复执行同一批任务，必须共享一个迭代器。
- `n` 大于任务数：多余的工人取不到任务直接退出，没有问题。

**追问。**
- 想拿到每个任务的返回值？：按下标记录结果列表，工人用 `enumerate` 的迭代器取（下标，函数）。

**同模式。** LC 2694 事件发射器、LC 2627 函数防抖、LC 2695 包装数组
