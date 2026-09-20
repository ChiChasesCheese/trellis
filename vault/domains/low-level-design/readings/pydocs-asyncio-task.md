---
nodes: [concurrency.asyncio]
url: https://docs.python.org/3/library/asyncio-task.html
---
# Coroutines and Tasks

值得读：`create_task`/`TaskGroup`/事件循环调度的官方文档，对应
`concurrency-asyncio-event-loop`、`concurrency-asyncio-await-yield-points`、`concurrency-asyncio-gather-taskgroup`
三张卡——协程本身不并发执行，只有包进 Task 交给事件循环调度才会，`await` 才是真正的让出点，读它能补上这条容易被
"async 关键字自动并发"这一直觉误导的机制细节。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-task.html)
%% trellis:end %%
