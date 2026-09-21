---
id: open-connection-returns-reader-writer-64kib-default
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
`reader, writer = await asyncio.open_connection(host, port)` 返回的两个对象各负责什么？默认的读缓冲区大小是多少？

## A
`reader` 是 `StreamReader`，负责从连接里异步读取数据（`read()`/`readline()`/`readuntil()` 等）；`writer` 是 `StreamWriter`，负责写数据（`write()`）并管理连接关闭。`StreamReader` 的内部缓冲区大小由 `limit` 参数控制，默认是 64 KiB。
