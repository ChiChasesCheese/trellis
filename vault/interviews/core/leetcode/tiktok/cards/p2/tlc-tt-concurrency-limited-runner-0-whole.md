---
id: tlc-tt-concurrency-limited-runner-0-whole
node: p2.tt-concurrency-limited-runner
type: qa
---
## Q
**限制并发数的异步任务执行器**｜Medium · 近一年被问：美国 0 次、国内 7 次 · 最近 2026-10-26（国内面试记录）

实现 `async def run_limited(tasks, limit)`：`tasks` 是 `n` 个无参的异步函数（调用后返回协程，`0 <= n <= 10^5`），`limit` 是并发上限。同一时刻最多有 `limit` 个任务在执行，一个结束立刻补上下一个；每个任务恰好被调用一次。返回与输入顺序一致的结果列表，每项是 `("fulfilled", 返回值)` 或 `("rejected", 异常)`：任务抛出的异常（包括调用时同步抛出的）都要被记录，不能让整体失败。`limit` 不是正整数时抛 `ValueError`。

例：5 个任务，`limit = 2`；第 2 个任务运行中抛 `RuntimeError("b")`，第 4 个在被调用的瞬间同步抛 `KeyError("sync")`，其余返回 `"A"`、`"C"`、`"D"` → `[("fulfilled", "A"), ("rejected", RuntimeError("b")), ("fulfilled", "C"), ("rejected", KeyError("sync")), ("fulfilled", "D")]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 `asyncio.Semaphore(limit)` 把“执行区”围起来：每个任务包一层协程，拿到名额（`async with sem`）之后才调用任务；包装协程里 `try/except Exception` 把返回值或异常按**下标**写进 `results[i]`；`TaskGroup` 等全部结束。`O(n)`。

**识别。** 「同时最多 k 个、一个结束立刻补上」是**并发池**（bounded concurrency）：Python 里有两种标准写法，信号量（`Semaphore`）和固定 `limit` 个 worker 抢任务。「结果与输入顺序一致」要求按下标写回，不能按完成顺序追加。「异常不能让整体失败」要求每个任务自己兜住异常，因为 `TaskGroup` 里任何一个子任务抛异常都会取消全体。

**推导。** 暴力一：逐个 `await`，上限满足但完全没有并发。暴力二：全部一起 `gather`，并发数等于 `n`，连接数或内存会爆。暴力三：每 `limit` 个一批 `gather`，慢任务拖住整批，下一批要等整批结束才开始，违反“一个结束立刻补上”。浪费在于：缺一个**名额**的概念。洞察：信号量就是名额计数器，一个任务结束归还名额，排在队首的等待者立刻被唤醒；调用任务（`task()`）必须放在拿到名额之后，否则任务会提前启动。

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

运行：上面的 5 个任务、`limit = 2` → `[('fulfilled', 'A'), ('rejected', RuntimeError('b')), ('fulfilled', 'C'), ('rejected', KeyError('sync')), ('fulfilled', 'D')]`；启动日志是 `start a, start b, end b, start c, end c, start d, end a, end d`（`b` 一结束 `c` 立刻开始）；`[]` → `[]`；`limit` 取 `0`、`-1`、`1.5`、`True`、`"2"` 都抛 `ValueError`；10 个任务、`limit = 3` 的峰值并发是 `3`。

**复杂度。** 调度开销 `O(n)`，总耗时由任务本身决定；空间 `O(n)`（`n` 个包装 Task 同时存在）。

**易错点。**
- 按 `limit` 个一批 `gather`：任务 a 耗时 50ms，b、c、d 各 10ms，`limit = 2` 时日志是 `start a, start b, end b, end a, start c, ...`，`c` 要等 `a` 结束才开始；正确做法是 `end b` 之后 `c` 立刻开始。
- 先 `[t() for t in tasks]` 或把 `task()` 写在 `try` 外：同步抛出的 `KeyError("sync")` 会直接从 `run_limited` 抛出，而不是记成 `("rejected", KeyError('sync'))`。
- `limit = True` 能通过 `limit <= 0` 检查，因为 `bool` 是 `int` 的子类，要单独排除。
- 捕获范围写 `Exception`，不要写 `BaseException` 或裸 `except:`，否则会吞掉 `CancelledError`，外部取消停不下来。

**追问。**
- 不用 `Semaphore`：起 `min(limit, n)` 个 worker，共享迭代器 `iter(enumerate(tasks))` 抢任务，一个 worker 做完一个就自己取下一个。
- 单任务超时：`async with asyncio.timeout(sec)` 放在拿到名额之后，到期抛 `TimeoutError`，被 `except Exception` 记为 `rejected`。
- 任务可取消：`except asyncio.CancelledError` 里用 `current_task().cancelling()` 区分“整次调用被取消”（继续 `raise`）和“只有这个任务被取消”（记 `("cancelled", None)`）。

**同模式。** LC 1114 按序打印、LC 1188 设计有限阻塞队列、LC 1226 哲学家进餐；工程里的连接池、`p-limit` 一类的并发限流器。
