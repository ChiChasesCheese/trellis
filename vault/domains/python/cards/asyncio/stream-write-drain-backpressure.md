---
id: stream-write-drain-backpressure
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
为什么官方文档要求 `writer.write(data)` 之后必须紧跟 `await writer.drain()`，而不能只调用 `write()` 就不管了？

## A
`write()` 只是把数据放进底层写缓冲区，不保证立刻发送出去；如果写入速度超过网络实际发送速度，缓冲区会持续膨胀吃掉内存。`drain()` 是一个背压（backpressure）/流控（flow control）方法：当缓冲区达到「高水位」（high watermark）时，`drain()` 会阻塞，直到缓冲区被消化到「低水位」（low watermark）以下才返回，从而把写入速度和发送速度匹配起来。
