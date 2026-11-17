---
id: concurrency-depth-mixing-boundaries
node: concurrency-depth.selection
type: qa
step: 3
---
## Q
`async def` 的处理函数里要调一个阻塞的库、一个耗 CPU 的函数，或者从普通线程里要调一个协程，各应该怎么过这条边界？

## A
**阻塞的丢给线程，耗 CPU 的丢给进程，别让事件循环停摆**

- **协程里直接阻塞**：事件循环是单线程，`time.sleep(0.3)` 期间所有协程都停了。实测每 50 ms 一次的心跳，直接阻塞时下一次心跳在 0.36 s 之后才来，用 `asyncio.to_thread` 心跳照常；
- **`asyncio.to_thread(f, *args)`**（3.9+）：在线程池里跑阻塞函数，会复制当前的上下文变量；
- **耗 CPU 的**：`await loop.run_in_executor(process_pool, f, x)`，丢给进程池；
- **线程里调协程**：线程里没有运行中的循环，`asyncio.run_coroutine_threadsafe(coro, loop)` 把协程交给主循环，返回 `concurrent.futures.Future`；
- **别在协程里再 `asyncio.run()`**：抛 `RuntimeError: asyncio.run() cannot be called from a running event loop`；
- **进程和线程混用**：在已经开了多个线程的进程里 `fork`，别的线程持有的锁在子进程里永远不会放开，3.12 起这样做会给出 `DeprecationWarning`；用 `spawn` 或 `forkserver`（macOS 默认就是 spawn）。

```python
import asyncio, time
async def heartbeat(n=3):
    t0, beats = time.perf_counter(), []
    for _ in range(n):
        beats.append(time.perf_counter() - t0)
        await asyncio.sleep(0.05)
    return beats
async def blocked():   time.sleep(0.3)                          # 事件循环停摆
async def offloaded(): await asyncio.to_thread(time.sleep, 0.3) # 丢给线程
async def main():
    for work in (blocked, offloaded):
        beats, _ = await asyncio.gather(heartbeat(), work())
        print(work.__name__, max(beats) < 0.3)   # blocked False / offloaded True
asyncio.run(main())
```

**知识点：**线程、进程与协程的选择（Choosing a Model）
