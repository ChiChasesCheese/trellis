---
id: uth-compose-thread-pool-5-bounded-runner
node: compose.thread-pool
type: qa
step: 5
---
## Q
**借到面试题：限制并发数的任务执行器**｜Java ThreadPoolExecutor · JDK 21

面试要你写「同一时刻最多 `limit` 个任务在跑，一个结束立刻补上」的执行器。怎样借线程池的骨架？

## A
**结构。** 线程池把「等待的任务」和「执行者」分开存：队列里是等待的任务，工人集合里是正在跑的执行者，工人数就是并发上限。面试题有两种对应写法：

- 信号量（`Semaphore(limit)`）：每个任务先抢名额再执行，结束归还，名额数就是工人数上限。
- 固定 `limit` 个 worker 共享一个任务迭代器：做完一个自己去取下一个，对应线程池里工人不停从队列取任务。

**为什么。** 要先拿到名额才调用任务，否则任务会提前启动；结果按下标写回，才能和输入顺序一致。

**坑。** 每 `limit` 个一批 `gather`：慢任务拖住整批，违反「一个结束立刻补上」。

**例题：** 限制并发数的异步任务执行器

`run_limited(tasks, limit)`：`tasks` 是 `n` 个无参的异步函数，同一时刻最多 `limit` 个在执行，一个结束立刻补上下一个；返回与输入顺序一致的 `("fulfilled", 值)` 或 `("rejected", 异常)`，任务抛出的异常都要记录，`limit` 不是正整数时抛 `ValueError`。

```python
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

type Outcome = tuple[str, Any]


async def run_limited[T](tasks: list[Callable[[], Awaitable[T]]], limit: int) -> list[Outcome]:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ValueError(f"limit 必须是正整数，收到 {limit!r}")
    results: list[Outcome] = [("rejected", None)] * len(tasks)
    sem = asyncio.Semaphore(limit)

    async def run_one(i: int, task: Callable[[], Awaitable[T]]) -> None:
        async with sem:                              # 名额在 async with 退出时自动归还
            try:
                results[i] = ("fulfilled", await task())   # 调用本身也在 try 里：同步抛出的异常同样被记录
            except Exception as exc:                 # 不捕获 BaseException，CancelledError 必须继续往外传
                results[i] = ("rejected", exc)

    async with asyncio.TaskGroup() as tg:
        for i, task in enumerate(tasks):
            tg.create_task(run_one(i, task))
    return results
```
