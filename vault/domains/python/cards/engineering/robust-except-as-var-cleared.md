---
id: robust-except-as-var-cleared
node: engineering.robustness
type: qa
source: python-docs
---
## Q
`except SomeError as e:` 里的变量 `e`，在 `except` 块结束之后还能不能继续用？

## A
不能。Python 会在 `except` 子句的代码块执行完毕时自动清除（相当于执行一次 `del e`）用 `as` 绑定的异常变量，等价于把整个块包进 `try/finally` 并在 `finally` 里 `del e`。这是为了避免异常对象（连同它引用的栈帧）在块外被长期持有造成内存泄漏；如果需要在块外继续使用，必须在块内把它赋给另一个变量。
