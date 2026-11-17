---
id: concurrency-depth-asyncio-cancel
node: concurrency-depth.cancel-shutdown
type: qa
step: 4
---
## Q
`asyncio` 里 `task.cancel()` 之后任务停在哪里？为什么收尾时不能吞掉 `CancelledError`？超时和一组任务一起失败又怎么取消其余的？

## A
**取消在下一个 `await` 处抛 `CancelledError`，收尾后必须重新抛出**

- **停在 `await` 上**：`cancel()` 本身不会打断同步代码，下次任务让出控制权的那个 `await` 抛出 `CancelledError`，所以一段不含 `await` 的长循环取消不了；
- **`except CancelledError` 里做清理然后 `raise`**（示例是这个写法）：实测重新抛出的任务最后 `cancelled() == True`；吞掉它的任务 `cancelled() == False`，等于取消失败，依赖取消的外层超时和 `TaskGroup` 都不再可靠；
- **清理放 `finally`**：要在清理里再 `await`（关连接）时，注意清理期间也可能再被取消；
- **`asyncio.timeout(秒)`**（3.11+）：超时时取消里面的 `await`，在块外变成 `TimeoutError`；
- **`TaskGroup`**（3.11+）：一个任务抛异常，其余全部被取消，退出时把异常汇总成 `ExceptionGroup`，用 `except*` 接；实测同组里一个 10 秒的任务被取消，异常是 `ValueError`；
- **`gather` 不同**：默认一个失败，其余继续跑，不会被取消。

```python
import asyncio
async def worker(log):
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        log.append("cleanup")
        raise                           # 必须重新抛出
async def main():
    log = []
    t = asyncio.create_task(worker(log)); await asyncio.sleep(0)
    t.cancel()
    try: await t
    except asyncio.CancelledError: pass
    print(log, t.cancelled())           # ['cleanup'] True
asyncio.run(main())
```

**知识点：**取消、超时与关闭（Cancellation & Shutdown）
