---
id: pl-conc-structured-found-python
node: concurrency.structured-concurrency
type: qa
step: 3
---
## Q
Python 的 `asyncio.TaskGroup`、`CancelledError` 和 `ExceptionGroup` / `except*` 是什么？一个任务失败时，TaskGroup 做了什么？

## A
- **`asyncio.TaskGroup`**（Python 3.11 起）：一个异步上下文管理器，用 `async with` 进入。`tg.create_task(coro)` 在组里启动任务；**离开 `async with` 块时自动等待组内所有任务结束**。
- **取消**：任务被取消时，Python 在它当前的 `await` 点注入 `asyncio.CancelledError` 异常。任务可以捕获它做清理，但应当重新抛出。
- **`ExceptionGroup`**（3.11 起）：把**多个**同时发生的异常装进一个异常；用 `except*` 语法按类型匹配其中的成员（`except* ValueError as eg:`，`eg.exceptions` 是成员列表）。

规则：组内任一任务抛出异常 → TaskGroup 取消所有其他仍在运行的任务 → 等它们结束 → 把收集到的异常包成 `ExceptionGroup` 抛出。

实验：A、C 各需 0.5 秒，B 在 0.1 秒后失败：
```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker("A", 0.5))
        tg.create_task(worker("B", 0.1, fail=True))
        tg.create_task(worker("C", 0.5))
except* ValueError as eg:
    print("caught:", [str(e) for e in eg.exceptions])
print("scope exited; no task outlives it")
```
（`worker` 在 `except asyncio.CancelledError` 里打印 `cancelled` 并重新抛出。）输出：
```
C cancelled
A cancelled
caught: ['B failed']
scope exited; no task outlives it
```
B 失败后，A、C 立即收到取消；`async with` 之后的代码执行时，组内没有任何任务还在跑。

对比裸 `asyncio.create_task(...)`：任务游离在外，失败时异常只在垃圾回收时以 `Task exception was never retrieved` 的形式出现在 stderr。
