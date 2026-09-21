---
nodes:
- asyncio.event-loop
title: asyncio.run() 与 Runner
corpus: python-docs
section: 34-asyncio-runner
url: https://docs.python.org/3/library/asyncio-runner.html
tags:
- canonical
---

# asyncio.run() 与 Runner

asyncio.run() 是运行一个 asyncio 程序最简单也是官方推荐的入口：它会创建一个全新的事件循环，运行传入的协程直到完成，然后负责关闭循环、清理未完成的异步生成器，最后销毁循环，这一整套生命周期管理不需要使用者手动操心。文档也介绍了更底层的 asyncio.Runner 上下文管理器，适合需要在多次 run() 调用之间复用同一个事件循环状态（比如测试场景）的情况。文中特别提醒：asyncio.run() 每次调用都会创建全新的循环，不能在一个已经运行着事件循环的环境（比如已经在协程内部）里再调用它，否则会报错。还讲了如何优雅处理 KeyboardInterrupt（Ctrl+C）不把清理逻辑打断。这是几乎每个 asyncio 程序主入口该知道的全部细节。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-runner.html)

## Archived copy
![[pydocs-asyncio-runners-clip]]
%% trellis:end %%
