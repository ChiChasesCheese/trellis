---
id: task-inherits-future-except-set-result-exception
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
`asyncio.Task` 是 `asyncio.Future` 的子类，它继承了 Future 的哪些能力，又主动屏蔽了哪两个方法？

## A
`Task` 继承 `Future` 几乎全部的 API（如状态查询、`add_done_callback`、`cancel`），因为 Task 本身也是「未来会有结果的占位符」。但它不继承 `Future.set_result()` 和 `Future.set_exception()`：Task 的结果只能由它包装的协程运行完成或抛异常来产生，不允许外部代码直接替它「写答案」。
