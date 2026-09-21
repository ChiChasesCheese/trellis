---
id: robust-try-else-minimize-scope
node: engineering.robustness
type: qa
source: python-docs
---
## Q
为什么 `try` 块里最好只放可能抛异常的那一两行代码，把后续处理逻辑放进 `try/except` 的 `else` 子句而不是继续留在 `try` 里？

## A
`try` 子句里任何一行抛出的异常都会被同一个 `except` 捕获，`try` 块越大，就越容易把「本不该被这个 `except` 处理」的异常也吞掉。`else` 子句只在 `try` 块完全没有抛异常时才执行，把「保护的操作」和「操作成功后的后续处理」分开，能避免后续处理里意外触发的同类异常被误判为保护对象的失败。
