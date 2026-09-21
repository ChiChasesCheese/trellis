---
id: zero-cost-exception-handling
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
为什么说 CPython 的异常处理是「零成本」（zero-cost）的？没有异常抛出时到底省了什么开销？

## A
`try` 块编译出的字节码里，没有异常时不会执行任何「设置异常处理器」的额外指令——这类伪指令在编译期就被去掉了，替换成一张和字节码分开存放的元数据表（异常表 exception table，存在 code 对象的 `co_exceptiontable` 字段里），只有真的抛出异常时才去查这张表。所以 try 块在「没抛异常」的路径上几乎不比没写 try 多花代价，代价被转嫁到了「真的抛异常」这条冷路径上。
