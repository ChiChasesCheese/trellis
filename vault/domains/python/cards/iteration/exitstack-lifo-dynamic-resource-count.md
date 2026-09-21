---
id: exitstack-lifo-dynamic-resource-count
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
`contextlib.ExitStack` 是怎么支持「动态数量」的上下文管理器的？它注册的清理逻辑按什么顺序执行？

## A
`stack.enter_context(cm)` 会立即调用 cm 的 `__enter__()`，并把它的 `__exit__()` 压入 ExitStack 内部维护的一个回调栈；可以在循环里对不确定数量的资源反复调用 `enter_context`。当外层 `with ExitStack() as stack:` 块结束（正常或异常）时，这些 `__exit__()` 按后进先出（LIFO）顺序依次调用，效果等价于把它们写成层层嵌套的 `with` 语句；`stack.callback(func)` 还能把普通清理函数挂到同一个栈上一起管理。
