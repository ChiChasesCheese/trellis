---
nodes:
- asyncio.event-loop
- asyncio.blocking-and-threads
title: asyncio 事件循环底层 API 参考
corpus: python-docs
section: 29-asyncio-eventloop
url: https://docs.python.org/3/library/asyncio-eventloop.html
tags:
- canonical
---

# asyncio 事件循环底层 API 参考

这是事件循环本身的低层 API 参考，平时写业务代码很少直接用，但理解它能解释高层 API 背后到底发生了什么：loop.call_soon() 把回调排进下一轮循环立即执行，call_later()/call_at() 支持延迟调度；loop.run_in_executor() 是把阻塞的同步函数丢进线程池（或进程池）执行、返回一个可以被 await 的 Future 的底层机制，asyncio.to_thread() 就是它的简化封装。文档还讲了如何监听文件描述符的可读/可写事件、如何注册 Unix 信号处理器，以及错误处理 API（loop.set_exception_handler()）如何捕获没人处理的异常。这篇偏底层，适合在遇到 asyncio 到底是怎么把回调和协程调度起来的这类刨根问底的问题时查阅，日常业务开发用高层 API（asyncio.run、TaskGroup）就够了。
