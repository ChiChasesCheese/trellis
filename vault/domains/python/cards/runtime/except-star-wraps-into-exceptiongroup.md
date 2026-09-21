---
id: except-star-wraps-into-exceptiongroup
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
`except*` 处理的目标类型是什么？如果 try 块抛出的是一个普通异常（不是异常组）但类型恰好匹配某个 `except*` 子句，会发生什么？

## A
`except*` 只用来处理「异常组」（`BaseExceptionGroup` 的实例），一次性捕获并分派一批可能互不相关的异常，而不是单个异常；同一个 try 语句不能同时用 `except` 和 `except*`。如果实际抛出的是普通异常但类型匹配了某个 `except*` 子句，Python 会自动把它包一层，变成一个消息为空字符串的 `ExceptionGroup`，保证 `except* ... as e` 里 `e` 的类型始终是 `BaseExceptionGroup`，调用方代码不用分两种情况处理。
