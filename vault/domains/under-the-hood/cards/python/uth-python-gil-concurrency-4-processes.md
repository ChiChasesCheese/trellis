---
id: uth-python-gil-concurrency-4-processes
node: python.gil-concurrency
type: qa
step: 4
---
## Q
**绕开 GIL：进程、子解释器与 asyncio 怎么选**｜Python · CPython 3.14

CPU 密集的任务怎样才能用满多个核？多进程要付出什么代价？

## A
**背景。** GIL 是「每个解释器一把」。要并行执行 Python 字节码，就得有多个解释器，各带自己的 GIL。

**结构。** 多进程（`multiprocessing`、`ProcessPoolExecutor`）里，每个子进程是一个独立的 Python 进程，真并行。代价是内存不共享：参数和结果要先序列化（pickle）成字节，经管道传过去；启动一个进程也比启动线程慢得多。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="10" y="20" width="100" height="80" rx="3"/>
<rect x="22" y="72" width="76" height="20" rx="3"/>
<line x1="60" y1="100" x2="60" y2="128"/>
<rect x="122" y="20" width="100" height="80" rx="3"/>
<rect x="134" y="72" width="76" height="20" rx="3"/>
<line x1="172" y1="100" x2="172" y2="128"/>
<rect x="234" y="20" width="100" height="80" rx="3"/>
<rect x="246" y="72" width="76" height="20" rx="3"/>
<line x1="284" y1="100" x2="284" y2="128"/>
<line x1="40" y1="130" x2="310" y2="130" stroke-width="2"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="22" y="46" width="76" height="20" rx="3"/>
<rect x="134" y="46" width="76" height="20" rx="3"/>
<rect x="246" y="46" width="76" height="20" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="60.0,128.0 57.0,122.0 63.0,122.0"/>
<polygon points="172.0,128.0 169.0,122.0 175.0,122.0"/>
<polygon points="284.0,128.0 281.0,122.0 287.0,122.0"/>
</g>
<g fill="currentColor">
<text x="60" y="60" font-size="11">自己的 GIL</text>
<text x="60" y="86" font-size="11">自己的内存</text>
<text x="172" y="60" font-size="11">自己的 GIL</text>
<text x="172" y="86" font-size="11">自己的内存</text>
<text x="284" y="60" font-size="11">自己的 GIL</text>
<text x="284" y="86" font-size="11">自己的内存</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="60" y="38" font-size="11">进程 1</text>
<text x="172" y="38" font-size="11">进程 2</text>
<text x="284" y="38" font-size="11">进程 3</text>
<text x="175" y="172" font-size="11">真并行, 但每个任务要付序列化和启动的代价</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="175" y="150" font-size="11">管道: 参数和结果先 pickle 成字节</text>
</g>
</g>
</svg>
```

**细节。**

- 启动方式：macOS 和 Windows 默认 `spawn`（启动全新的解释器）；Python 3.14 起，其他 POSIX 系统的默认值从 `fork` 改成了 `forkserver`。
- 3.14 新增 `InterpreterPoolExecutor`：同一个进程里放多个子解释器，各有各的 GIL，真并行，但不能共享可变对象。

| 任务 | 选择 |
|---|---|
| 成千上万个网络连接在等 | asyncio（单线程，协程） |
| 少量阻塞 I/O | 线程 |
| CPU 密集 | 进程池或子解释器 |

**坑。** 任务太小时，序列化和传输花的时间比计算还多，多进程反而更慢。

**例题：** 限制并发数的异步任务执行器（TikTok 变体题）

实现 `async def run_limited(tasks, limit)`：`tasks` 是 `n` 个无参的异步函数，`limit` 是并发上限，同一时刻最多 `limit` 个在执行，一个结束立刻补上下一个。返回与输入顺序一致的结果列表，每项是 `("fulfilled", 返回值)` 或 `("rejected", 异常)`。

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
