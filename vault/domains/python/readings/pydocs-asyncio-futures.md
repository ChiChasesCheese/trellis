---
nodes:
- asyncio.futures
title: asyncio Future 对象参考
corpus: python-docs
section: 30-asyncio-future
url: https://docs.python.org/3/library/asyncio-future.html
tags:
- canonical
---

# asyncio Future 对象参考

asyncio.Future 是一个尚未完成、将来会有结果（或异常）的占位符，Task 就是 Future 的子类，专门用来包装协程。文档讲清了它的核心状态机：set_result() 设置结果并唤醒所有等待者，set_exception() 设置异常（这个异常会在 .result() 被调用时重新抛出），add_done_callback() 注册完成时执行的回调。特别值得注意的是 run_in_executor() 如何把一个运行在线程池里的同步函数的结果桥接成一个能被 await 的 Future，这是同步代码和异步世界对接的关键桥梁。理解 Future 的状态机（pending 到 done，done 之后不能再变）是理解 gather()、wait_for()、TaskGroup 等所有高层并发原语的基础，因为它们本质上都是在组合多个 Future 的完成时机。
