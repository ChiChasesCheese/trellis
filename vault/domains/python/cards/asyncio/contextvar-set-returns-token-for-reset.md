---
id: contextvar-set-returns-token-for-reset
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
`token = var.set(new_value)` 里返回的 `Token` 对象有什么用？

## A
`Token` 记录了这次 `set()` 调用之前变量的旧值，可以传给 `var.reset(token)` 把变量精确恢复到 `set()` 之前的状态（而不是恢复成某个写死的默认值）；同一个 `Token` 只能用来 `reset` 一次。3.14 起 `Token` 还支持直接当上下文管理器用（`with var.set(...)`），退出时自动帮你调用 `reset()`。
