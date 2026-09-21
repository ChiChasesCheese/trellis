---
nodes:
- asyncio.event-loop
- asyncio.coroutines-tasks
- asyncio.futures
title: asyncio 概念全景：事件循环、协程与 Future
corpus: python-docs
section: 06-a-conceptual-overview-of-asyncio
url: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html
tags:
- canonical
---

# asyncio 概念全景：事件循环、协程与 Future

这是从零理解 asyncio 最好的入门文章，用类比讲清三个角色如何配合：事件循环（event loop）是一个不断轮询待办任务队列的调度器；协程函数（async def）本身只是配方，必须被包装成 Task 交给循环才会真正执行；Future 是一个承诺未来会有结果的占位符，Task 是能自己跑代码的 Future。文章第二部分动手实现了一个简化版 asyncio.sleep，让你看清 await 在字节码层面到底做了什么，协程在遇到 await 时把控制权交还给事件循环，循环记下这个协程在等什么，等条件满足再把它唤醒。这篇文章解决的不是怎么写 async 代码，而是为什么 async 代码是这样运作的，建议在动手写 asyncio 项目之前先读完建立心智模型。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html)

## Archived copy
![[pydocs-asyncio-overview-clip]]
%% trellis:end %%
