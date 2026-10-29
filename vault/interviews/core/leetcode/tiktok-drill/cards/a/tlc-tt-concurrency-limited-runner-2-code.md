---
id: tlc-tt-concurrency-limited-runner-2-code
node: a.tt-concurrency-limited-runner
type: qa
step: 2
---
## Q
**限制并发数的异步任务执行器**｜写出 Python 实现

`run_limited(tasks, limit)`：`tasks` 是 `n` 个（`0 <= n <= 10^5`）无参异步函数，同时最多执行 `limit` 个，一个结束立刻补上；返回与输入同序的 `("fulfilled", 值)` / `("rejected", 异常)` 列表，调用时同步抛出的异常也要记录；`limit` 不是正整数抛 `ValueError`。

## A
**思路。** 每个任务包一层协程：先 `async with sem` 拿名额，再调用并 `await` 任务；结果或异常按下标写进预先建好的 `results`。`TaskGroup` 负责等全部结束，并在外部取消时把取消传给所有子任务。

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

运行：`limit = 2`，任务依次是 `a`（30ms 返回 `"A"`）、`b`（10ms 后抛 `RuntimeError("b")`）、`c`（返回 `"C"`）、调用时同步抛 `KeyError("sync")` 的函数、`d`（返回 `"D"`）→ `[('fulfilled', 'A'), ('rejected', RuntimeError('b')), ('fulfilled', 'C'), ('rejected', KeyError('sync')), ('fulfilled', 'D')]`；`[]` → `[]`；`limit` 为 `0`、`-1`、`1.5`、`True`、`"2"` → `ValueError`；`n = 10^5`、`limit = 100` 的空转任务全部完成，`results[0]` 是 `('fulfilled', 1)`。

**复杂度。** 调度开销时间 `O(n)`，空间 `O(n)`（`n` 个包装 Task）；并发数始终 `<= limit`。

**写法要点。** `async with sem` 把“归还名额”交给上下文管理器，任何退出路径（正常、异常、取消）都不会漏还；`except Exception` 而不是 `BaseException`，让 `CancelledError` 穿过去；`[("rejected", None)] * n` 里共享的是不可变元组，所以安全；`type Outcome = ...` 和 `def f[T](...)` 是 3.12 的新语法；`TaskGroup`（3.11+）比 `gather` 更结构化，外部取消时不会漏掉子任务。
