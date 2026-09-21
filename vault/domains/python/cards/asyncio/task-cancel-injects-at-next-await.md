---
id: task-cancel-injects-at-next-await
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
调用 `task.cancel()` 之后，目标任务会立刻停止运行吗？

## A
不会立刻停止。`cancel()` 只是发出一个取消请求，事件循环会在下一个调度周期（即目标协程下一次执行到 `await` 让出控制权时）把 `asyncio.CancelledError` 这个异常注入到协程内部抛出；在此之前，协程仍会继续正常执行到那个点为止。
