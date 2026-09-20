---
nodes: [problems.machines.coffee-machine]
url: https://docs.python.org/3/library/queue.html
---
# queue — Python 标准库

值得读：文档里 `Queue` 几乎总是以生产者-消费者的缓冲区出现——生产者 `put` 任务，工作线程
`get` 任务。本题解把它反过来用作**资源池**：队列里装的是出口编号这种资源，线程 `get()` 阻塞
到有空闲出口，用完 `put()` 归还。两种用法方向正好相反，值得对照着想清楚：任务队列解决的是
削峰与背压（调用方不等结果），资源池解决的是并发度上限（调用方一直在等结果）。咖啡机的
调用方就是站在机器前面按按钮的人，所以要的是后者。相比自己写 `Semaphore` 加一个 id 列表，
队列还白送了编号，于是事件里能写出"这杯从 outlet-2 出"。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/queue.html)

## Archived copy
![[src-python-docs-queue-thread-pool-clip]]
%% trellis:end %%
