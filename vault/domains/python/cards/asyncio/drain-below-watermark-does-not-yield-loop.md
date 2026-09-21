---
id: drain-below-watermark-does-not-yield-loop
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
如果写缓冲区一直没超过高水位，反复执行 `writer.write(data); await writer.drain()` 会有什么隐藏的坑？

## A
当缓冲区低于高水位时，`drain()` 会立即返回，且**不会**把控制权让给事件循环（不 yield）。这意味着一段密集的 `write()+drain()` 循环可能一直霸占事件循环、阻止其它任务被调度，看起来像是异步代码却表现出同步阻塞的效果；解决办法是在循环里显式插入 `await asyncio.sleep(0)` 主动让出控制权。
