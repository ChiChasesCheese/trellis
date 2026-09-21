---
id: calling-coroutine-function-only-builds-object
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
写了 `async def foo(): ...`，直接调用 `foo()`（不加 `await`）会发生什么？函数体会执行吗？

## A
调用一个用 `async def` 定义的协程函数（coroutine function）只会构造并返回一个协程对象（coroutine object，`types.CoroutineType` 的实例），函数体不会执行。要让函数体真正跑起来，必须要么直接 `await` 这个协程对象，要么用 `asyncio.create_task()` 把它包装成 `Task` 交给事件循环调度。
