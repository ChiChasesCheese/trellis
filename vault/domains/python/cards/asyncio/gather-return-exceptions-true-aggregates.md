---
id: gather-return-exceptions-true-aggregates
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
`asyncio.gather(*aws, return_exceptions=True)` 和默认参数相比，行为上有什么本质区别？

## A
设为 `True` 时，任何一个可等待对象抛出的异常会被当作「和正常返回值一样的结果」直接放进结果列表里（而不是向外传播），调用方需要自己遍历结果列表逐个判断哪些是异常；若全部成功，结果列表顺序仍与传入的 `aws` 顺序一一对应。
