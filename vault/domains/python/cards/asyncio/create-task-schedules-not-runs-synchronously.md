---
id: create-task-schedules-not-runs-synchronously
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
`task = asyncio.create_task(coro())` 这一行执行完，`coro()` 的函数体是已经跑完了、正在跑，还是还没开始跑？

## A
`create_task()` 会立刻把协程包装成 `Task` 并把一个回调加入事件循环的待运行队列（相当于「预约」了执行），但该调用本身不阻塞、立刻返回；协程体真正开始执行要等到当前协程下一次让出控制权（如 `await`）之后。例外是 3.12 起的 `eager_start=True`：此时 Task 在创建瞬间就抢先运行到第一个真正阻塞点。
