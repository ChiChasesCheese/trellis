---
id: cpu-bound-code-blocks-whole-loop
node: asyncio.event-loop
type: qa
source: python-docs
---
## Q
为什么一段纯 CPU 密集、不含任何 `await` 的代码会让整个 asyncio 程序看起来「卡住」？

## A
事件循环是单线程、协作式（cooperative）调度：某个任务只有执行到 `await` 一个会真正让出控制权的对象（如 `await task`）时，循环才能切换去运行其它任务。纯 CPU 计算没有让出点，会一直占着这一个线程直到算完，其间循环里的所有其它任务（网络 I/O、定时器回调等）都无法被调度执行。
