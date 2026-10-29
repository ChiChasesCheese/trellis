---
id: uth-python-asyncio-3-blocking
node: python.asyncio
type: qa
step: 3
---
## Q
**协程里 time.sleep 会怎样**｜Python · CPython 3.14

一个协程里调用了 `time.sleep(0.5)`，同时另一个协程只 `await asyncio.sleep(0.1)`，后者什么时候醒来？

## A
**结构。** 单线程的事件循环一轮轮跑回调；回调不返回，就进不了下一轮。

**细节。**

- 实测后者 0.52 秒才醒，不是 0.1 秒：到期的定时器要等下一轮才取出。
- 回调里 `call_soon` 的新回调也要等下一轮：实测顺序 `a, b, c`。
- 调试模式下，超过 `slow_callback_duration`（默认 0.1 秒）的回调会打警告。

**为什么。** 协作式调度不抢占，切换开销极小；代价是任何阻塞调用都拖住全部任务。

**坑。** 阻塞或 CPU 密集的工作用 `asyncio.to_thread` 或进程池。

**对应 LeetCode：** LC 1114 按序打印 · LC 1115 交替打印 FooBar
