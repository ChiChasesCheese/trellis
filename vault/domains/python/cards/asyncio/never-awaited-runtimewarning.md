---
id: never-awaited-runtimewarning
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
调用了一个协程函数，但既没有 `await` 它、也没有用 `create_task()` 调度它，asyncio 会怎么提醒你？

## A
asyncio 会发出 `RuntimeWarning: coroutine 'xxx' was never awaited`：这个协程对象被创建了却从未被驱动执行过。这是「程序好像什么都没做」这类 bug 最常见的根因之一，修复方式是补上 `await` 或改用 `asyncio.create_task()`。
