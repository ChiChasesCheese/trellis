---
id: taskgroup-exception-group-multiple-failures
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
如果 `asyncio.TaskGroup` 里有不止一个子任务同时抛出异常，这些异常会怎样被汇报给外层代码？

## A
多个异常不会互相覆盖或只保留一个，而是被打包进一个 `ExceptionGroup`（若都是 `Exception` 子类）或 `BaseExceptionGroup`（若含 `BaseException`），作为单一异常在 `async with TaskGroup()` 语句退出时抛出，调用方可以用 `except*` 语法分别处理组内不同类型的异常。
