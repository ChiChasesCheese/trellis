---
id: transport-how-protocol-which-bytes
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
在 `Transport`/`Protocol` 这套模型里，`Transport` 和 `Protocol` 各自关心的问题分别是什么？两者是几对几的关系？

## A
`Transport` 关心「字节怎么被传输」（how），是对 socket 之类 I/O 端点的抽象；`Protocol` 关心「该收发哪些字节」（which，及部分 when），是从传输层视角对上层应用逻辑的抽象。二者始终是 1:1 关系：`Protocol` 调用 `Transport` 的方法发送数据，`Transport` 收到数据后回调 `Protocol` 的方法把数据递交上去。
