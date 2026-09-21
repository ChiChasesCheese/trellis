---
id: task-exception-never-retrieved-log
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
用 `asyncio.create_task()` 起了一个任务，任务内部抛了异常，但代码里从没 `await` 过这个 Task 去取结果，异常会怎样？

## A
异常不会立刻抛给任何人：只有当这个 Task 对象最终被垃圾回收时，asyncio 才会打印一条 `Task exception was never retrieved` 的日志，附上原始异常和堆栈。这是「程序看起来正常但其实某个后台任务默默炸了」的典型根因；开启调试模式还能额外打印出这个 Task 最初是在哪里被创建的调用栈。
