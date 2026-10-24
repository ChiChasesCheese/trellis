---
id: pl-sig-python-pitfall-gil-threads
node: signatures.python
type: qa
step: 9
---
## Q
Python 在生产中最常见的性能与并发陷阱是什么？“用线程加速 CPU 计算”和“纯 Python 热循环”的真实表现是什么？

## A
**陷阱一：用多线程加速 CPU 密集任务**。开发者把计算分给 4 个线程，期望 4 倍加速。真实结果（本机，每个线程做一千万次累加）：

```python
ts = [threading.Thread(target=work) for _ in range(4)]
# 1 thread: 0.12 s   4 threads: 0.47 s    (GIL build)
# 4 threads on free-threaded 3.14t: 0.14 s
```

有 GIL 的构建里，4 个线程总时间约 0.47 秒，是单线程的 4 倍，没有任何并行；自由线程构建则是 0.14 秒。症状：CPU 使用率停在 100%（只用了一个核），增加线程毫无作用。

**陷阱二：纯 Python 热循环**。五百万次循环约 145 ms，同样的计算 NumPy 约 7 ms，约 20 倍。症状：分析显示时间全花在你自己的 Python 函数里。

**陷阱三：在 `asyncio` 里阻塞**。在协程里调用 `time.sleep(1)` 或同步的网络库，整个事件循环被卡住：三个任务应并发 1 秒，实际花 3.4 秒。

**陷阱四：内存用对象表示的成本**。一个三属性的普通实例，实例加 `__dict__` 超过 330 字节；上百万个实例会撑爆内存，`__slots__` 或 NumPy 才是出路。

**陷阱五：循环导入与路径遮蔽**、**可变默认参数**、**晚绑定闭包**（`[lambda: i for i in range(3)]` 的三个函数都返回 2）。这些属于语言的小陷阱，linter 能抓到一部分。

**防线**：
1. 先分析（`cProfile`、`py-spy`）再优化，确认瓶颈是 CPU 还是 I/O。
2. CPU 密集：多进程、原生库，或评估自由线程构建。
3. I/O 密集：`asyncio` 或线程池，并确保没有阻塞调用。
4. 规模化的数据结构用 NumPy、`array`、Arrow，而不是 Python 对象列表。
5. 压测时观察 CPU 核使用情况，不只看总延迟。

**教训**：Python 的性能直觉常常与其他语言相反：线程不一定并行，循环不一定快，对象不一定便宜。
