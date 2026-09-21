---
id: async-generator-not-fully-iterated-finally-may-not-run
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
用 `async for` 遍历一个异步生成器（async generator）时提前 `break`（没有遍历到耗尽），生成器里的 `finally` 清理代码一定会执行吗？

## A
不一定会立刻执行。如果生成器没有被完全迭代、也没有显式调用 `agen.aclose()`，它的 `finally` 块不会马上跑；asyncio 依赖 `firstiter`/`finalizer` 两个钩子（hook）在生成器最终被垃圾回收或事件循环关闭时才调度执行 `aclose()`，触发时机比很多人预期的晚——排查「清理代码没执行」的 bug 时要留意这一点。
