---
id: pl-conc-gil-found-escape-routes
node: concurrency.gil
type: qa
step: 4
---
## Q
`multiprocessing` 和自由线程构建（free-threaded build）分别是什么？
怎样用它们让 Python 的 CPU 密集任务用上多个核？

## A
**多进程（`multiprocessing`）**：每个子进程是一个独立的 Python 解释器，各有自己的 GIL 和内存，互不干扰，所以可以真正并行。进程之间不能直接共享对象，参数和结果要通过**序列化**（pickle）在进程间传递。
```python
with Pool(4) as p:
    total = sum(p.starmap(count, [(k*N//4, (k+1)*N//4) for k in range(4)]))
```
同样的素数任务（40 万以内，4 份），输出 `4 processes 0.18s`（对比 4 线程 0.32 秒）。加速有限的原因是进程启动、参数与结果的序列化，以及 4 份工作量不均。

**自由线程构建**：CPython 3.13 起提供的另一种构建（可执行文件通常叫 `python3.14t`），**没有 GIL**，线程可以真的同时执行 Python 字节码。用 `sys._is_gil_enabled()` 判断：默认构建返回 `True`，自由线程构建返回 `False`。
```python
# same script, free-threaded interpreter
print(sys._is_gil_enabled())      # False
# 1 thread  0.34s, 4 threads 0.13s
```
同样的 4 线程代码在自由线程构建上从 0.32 秒降到 0.13 秒（约 2.6 倍），单线程慢约 6%（0.34 对 0.32）。它保留了线程共享内存的编程模型，但原本靠 GIL“碰巧安全”的代码需要显式加锁。

**子解释器**：同一进程里的多个互相隔离的解释器，各有自己的 GIL（3.12 起），3.14 提供 `concurrent.interpreters` 模块。比进程轻，但对象不能直接共享。

三条路径对比：多进程成熟、隔离，但要序列化；自由线程共享内存，但生态要适配；子解释器介于两者之间。
