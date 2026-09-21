---
id: await-task-vs-await-coroutine-cede-control
node: asyncio.event-loop
type: qa
source: python-docs
---
## Q
`await some_task`（`Task` 对象）和 `await some_coro()`（协程对象）在是否让出控制权给事件循环上有什么区别？

## A
`await task` 会把控制权真正交还给事件循环：循环可以先去运行其它任务，等该 task 完成后再恢复当前协程。而 `await coroutine`（协程对象本身，未包装成 Task）不会把控制权交给事件循环，其行为等价于直接同步调用一个函数——期间事件循环上的其它任务无法插入运行。
