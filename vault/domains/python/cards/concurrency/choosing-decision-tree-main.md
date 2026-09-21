---
id: choosing-decision-tree-main
node: concurrency.choosing
type: qa
tags: [grown]
---
## Q
面对一个需要并发处理的任务，怎样用一句话给出线程 / 进程 / asyncio 的选型结论？

## A
先看任务是 I/O 密集还是 CPU 密集：CPU 密集的纯 Python 计算用 `multiprocessing`/`ProcessPoolExecutor` 绕开 GIL，或者干脆换成释放 GIL 的 C 实现库（NumPy、DuckDB）;I/O 密集时看调用的库有没有异步版本——如果依赖的是同步阻塞库（如 `requests`、大多数数据库驱动），用 `threading`/`ThreadPoolExecutor`；如果目标是数千级别的高并发连接、且依赖库本身有 async 版本（`aiohttp`、`asyncpg`），用 `asyncio` 换取单线程下更低的调度开销。
