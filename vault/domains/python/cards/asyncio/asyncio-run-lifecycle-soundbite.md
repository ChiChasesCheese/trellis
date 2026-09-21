---
id: asyncio-run-lifecycle-soundbite
node: asyncio.event-loop
type: qa
source: python-docs
---
## Q
面试官追问：`asyncio.run(main())` 这一行背后具体做了哪些事？

## A
它创建一个新的事件循环，把 `main()` 作为任务运行直到完成并返回其结果，随后负责收尾：终结（finalize）尚未关闭的异步生成器、关闭默认执行器（executor，最多等 5 分钟）、最后关闭并丢弃这个事件循环。同一线程内已有事件循环在运行时不能再调用 `asyncio.run()`。
