---
id: wait-for-timeout-cancels-and-waits
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
`await asyncio.wait_for(coro(), timeout=1.0)` 超时后，`coro()` 会立刻被丢弃、`wait_for` 立刻抛出 `TimeoutError` 吗？

## A
不是立刻抛出。超时发生时 `wait_for` 会先取消（cancel）内部包装的任务，然后**等待这次取消真正完成**之后才抛出 `TimeoutError`，因此实际等待时间可能略微超过设定的 `timeout`；如果取消过程中又产生了别的异常，那个异常会被传播出来而不是 `TimeoutError`。
