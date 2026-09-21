---
nodes:
- asyncio.contextvars
title: contextvars：按任务隔离的上下文变量
corpus: python-docs
section: 26-contextvars
url: https://docs.python.org/3/library/contextvars.html
tags:
- canonical
---

# contextvars：按任务隔离的上下文变量

contextvars 模块文档定义了 `ContextVar`、`Token` 与 `Context` 三个对象，以及 asyncio 如何在创建每个 Task 时调用 `copy_context()` 复制当前上下文。读它抓住一个机制：`Context` 是不可变映射，`ContextVar.set()` 只改当前上下文里自己那一项并返回可用于 `reset()` 的 Token；Task 启动时拿到的是复制品，所以 Task 内的 `set()` 不会泄漏到父协程或兄弟 Task，`await` 之间自然隔离。这正是 `threading.local` 在异步代码里出错的原因：一个线程上交替运行着多个 Task。带走三点：`ContextVar` 要定义在模块顶层（每次创建都是新变量）；`Context.run(fn)` 可以在指定上下文里同步运行函数；追踪 ID、请求 ID、`decimal` 精度都靠它跨 await 传播。
