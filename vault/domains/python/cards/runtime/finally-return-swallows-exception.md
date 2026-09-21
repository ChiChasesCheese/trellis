---
id: finally-return-swallows-exception
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
`finally` 块里如果也写了一条 `return`，会发生什么？try 块里本已抛出但还没处理完的异常会怎样？

## A
`finally` 里的 `return`（或 `break`/`continue`）会直接丢弃 try/except 路径上任何「暂存待重新抛出」的异常，也会覆盖 try 或 except 里已经执行过的 `return`——函数最终返回值以 `finally` 里最后执行的那条 `return` 为准。这是经典陷阱：写了 `finally: return x` 会让 try 块里真实抛出的异常被悄悄吞掉，调用者完全看不到它发生过。
