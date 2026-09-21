---
id: future-create-via-loop-not-direct-construct
node: asyncio.futures
type: qa
source: python-docs
---
## Q
官方文档建议创建 Future 用 `loop.create_future()`，而不是直接 `asyncio.Future()` 构造，为什么？

## A
这样第三方或自定义的事件循环实现（如替代实现）可以注入自己优化过的 Future 实现，而不是被迫使用标准库默认版本；同时官方也建议永远不要在自己代码对外暴露的公共 API 里直接返回裸的 Future 对象，因为它是给回调式底层代码（如 transport/protocol）和 async/await 高层代码打交道用的「胶水」，不是给普通调用者设计的接口。
