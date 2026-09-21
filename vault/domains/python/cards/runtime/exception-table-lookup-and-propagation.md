---
id: exception-table-lookup-and-propagation
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
异常真的被抛出之后，解释器怎么找到该由哪段代码处理它？当前帧里没有匹配的处理器时会怎样？

## A
解释器用当前正在执行的指令去查这一帧的异常表，看它是否被某个处理器覆盖，查到就跳转过去执行。如果当前帧的异常表里没有条目覆盖这条指令，异常就继续向上冒泡到调用者的帧，检查那里覆盖对应 `CALL` 指令的处理器——逐帧重复，直到找到处理器或到达最外层帧。如果一路都没找到，解释器函数直接返回，异常变成未捕获异常，沿途每一帧都会被记录进回溯（traceback）。
