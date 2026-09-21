---
id: else-clause-scopes-exception-handling
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
为什么把「确定不会失败、只在 try 成功后才该跑」的代码放进 `else` 子句，而不是接着写在 `try` 块里？

## A
`try` 块里任何一行都可能被同一层的 `except` 子句捕获，即使这行代码逻辑上属于「try 成功之后的后续处理」——一旦它自己抛出同类型异常，会被错误地当成 try 主体失败来处理，掩盖真实的 bug。放进 `else` 子句的代码只有在 try 块完全没抛异常、也没有 `return`/`break`/`continue` 提前退出时才会执行，并且它抛出的异常不会被前面同一个 try 语句的 `except` 子句捕获。
