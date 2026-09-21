---
id: contextvar-must-be-module-level-not-closure
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
官方文档为什么强调 `ContextVar` 必须创建在模块顶层，而不能创建在闭包（closure）内部？

## A
因为 `Context` 对象会对它里面出现过的 `ContextVar` 持有强引用（strong reference）；如果 `ContextVar` 是在某个函数内部临时创建的，只要有任何一个 `Context` 曾经用过它，这个变量就一直被强引用着，永远无法被垃圾回收，造成内存泄漏。创建在模块顶层则只存在一份，生命周期和模块本身一致，不会有这个问题。
