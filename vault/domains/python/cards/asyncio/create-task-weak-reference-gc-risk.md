---
id: create-task-weak-reference-gc-risk
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
为什么官方文档强调 `asyncio.create_task()` 返回的 `Task` 对象必须自己保留一个引用（比如存进变量或集合），否则会有风险？

## A
事件循环只持有 Task 的弱引用（weak reference），并不是强引用；如果代码里没有其它地方引用这个 Task，它可能在还没跑完时就被垃圾回收（garbage collected），导致任务莫名其妙「消失」、不执行。常见做法是把后台任务放进一个集合（如 `background_tasks.add(task)`）并在完成回调里再移除。
