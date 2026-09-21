---
nodes:
- asyncio.debugging
- asyncio.blocking-and-threads
title: asyncio 开发实践与调试
corpus: python-docs
section: 33-asyncio-dev
url: https://docs.python.org/3/library/asyncio-dev.html
tags:
- canonical
---

# asyncio 开发实践与调试

这是排查 asyncio 疑难问题该读的文档，列出了最常见的几类程序没反应的根因：协程对象创建了但忘记 await（会有专门的警告提示）；gather() 本身也是一个需要被 await 的对象，直接调用不加 await 什么都不会发生；异常留在了一个从未被读取结果的 Task 里，会在垃圾回收时才打印出来，容易被忽略；Jupyter 之类环境本身跑着事件循环，再手动调 asyncio.run() 会报事件循环已在运行。文档建议开启 debug 模式（asyncio.run(main(), debug=True)）能捕获阻塞事件循环超过阈值的慢回调、未等待的协程等一整类问题。异步生成器一节强调要显式调用 aclose() 关闭，否则垃圾回收时的清理行为是未定义的。这是 asyncio 从能跑到跑得稳必须知道的排错手册。
