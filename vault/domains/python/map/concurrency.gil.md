%% trellis:begin %%
# 全局解释器锁（GIL）：它保护什么、何时释放、切换间隔
*并发模型：GIL、线程与进程*

理解 GIL 让同一进程内同一时刻只有一个线程执行字节码、I/O 与部分 C 扩展（NumPy 内核）会释放它、5 ms 切换间隔的含义，以及 GIL 保护的是解释器状态而不是你的数据。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

**Unlocks:** [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]], [[domains/python/map/concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]], [[domains/python/map/concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]]

## Readings
- [[cpyint-04-parallelism-concurrency|CPython Internals · 并行与并发]]
- [[fluent-19-concurrency-models|Fluent Python 2e · 第 19 章 Python 的并发模型]]
- [[fowler-01-getting-to-know-asyncio|Python Concurrency with asyncio · 第 1 章 认识 asyncio]]
- [[pydocs-threading-module|threading 模块：线程、锁与同步原语]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (5)
1. [[gil-not-your-data]]
2. [[gil-switch-interval]]
3. [[gil-vs-multiprocessing]]
4. [[gil-who-releases]]
5. [[gil-why-needed]]
%% trellis:end %%

## Notes
