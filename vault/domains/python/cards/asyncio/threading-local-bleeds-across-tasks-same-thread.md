---
id: threading-local-bleeds-across-tasks-same-thread
node: asyncio.contextvars
type: qa
source: python-docs
---
## Q
为什么在 asyncio 代码里用 `threading.local()` 保存「每次请求」的状态（比如当前处理的客户端地址）是危险的？

## A
asyncio 的多个 Task 通常都跑在同一个 OS 线程里，而 `threading.local()` 的值是按线程绑定的，不区分是哪个 Task 在访问；一个 Task 设置的值，会「泄漏」给同一线程里交替执行的其它 Task 读到或覆盖，导致状态意外串到别的请求上——这正是官方文档建议改用 `ContextVar` 而不是 `threading.local()` 的原因。
