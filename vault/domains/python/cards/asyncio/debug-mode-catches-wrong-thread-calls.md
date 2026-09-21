---
id: debug-mode-catches-wrong-thread-calls
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
调试模式对「从错误的线程调用非线程安全 asyncio API」这类 bug 能提供什么帮助？

## A
调试模式打开后，像 `loop.call_soon()`、`loop.call_at()` 这类本身不是线程安全（not thread-safe）的方法，如果被从事件循环所在线程以外的线程调用，会直接抛出异常，而不是在生产模式下悄悄产生不确定的竞态问题——相当于把潜在的跨线程 bug 提前暴露出来。
