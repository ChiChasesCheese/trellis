---
nodes:
- asyncio.debugging
- asyncio.coroutines-tasks
title: 异步生成器为什么会漏跑 finally，以及 Task 是怎么被追踪的
corpus: cpython-internals
section: 014-asyncio
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# 异步生成器为什么会漏跑 finally，以及 Task 是怎么被追踪的

这篇解释一个真实会踩到的坑：`async for i in agen(): break` 提前跳出循环后，`agen` 没有被完全迭代完，它的 `finally` 块不会立刻执行——因为事件循环需要在“循环还在运行”的时候才能安全地 await 清理代码。CPython 通过 `sys.set_asyncgen_hooks`（PEP 525）注册两个钩子：第一次迭代时把生成器登记进事件循环的弱引用集合，生成器被判定不再被引用时再由事件循环创建一个任务去调用 `aclose()` 补跑 `finally`，循环关闭前还会兜底 `gather` 一遍所有存活的异步生成器。文档也提到 3.14 把 Task 的追踪从全局 `WeakSet`+字典 改成了每线程双向链表，为的是减少多线程下的锁竞争。读完能解释“为什么我的异步生成器 finally 没打印”这类真实 bug，也知道 Task 本质上是被事件循环/运行时登记追踪的对象，而不是凭空存在的协程包装。
