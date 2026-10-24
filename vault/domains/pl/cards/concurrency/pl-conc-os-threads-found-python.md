---
id: pl-conc-os-threads-found-python
node: concurrency.os-threads
type: qa
step: 4
---
## Q
Python 的 `threading.Thread` 和 `ThreadPoolExecutor` 是什么？Python 线程是真正的 OS 线程吗，怎么拿到线程的返回值？

## A
- **`threading.Thread`**：Python 的线程对象，背后是真正的 OS 线程（POSIX 的 `pthread`）。`Thread(target=f).start()` 启动，`join()` 等待。`target` 的返回值被丢弃。
- **`concurrent.futures.ThreadPoolExecutor`**：线程池。`submit(f, ...)` 返回 `Future`，`future.result()` 阻塞取结果，任务里的异常会在这里重新抛出。
- 受限于 GIL（全局解释器锁）：同一时刻只有一个线程能执行 Python 字节码，所以线程适合等 I/O，不能加速纯 Python 的计算。

最小例子：
```python
with ThreadPoolExecutor(3) as ex:
    fs = [ex.submit(lambda k=k: k*k) for k in (1, 2, 3)]
    print([f.result() for f in fs])
def boom(): raise RuntimeError("boom")
t = threading.Thread(target=boom); t.start(); t.join()
print("main continues")
```
输出：
```
[1, 4, 9]
Exception in thread Thread-1 (boom):
Traceback (most recent call last):
  ...
RuntimeError: boom
main continues
```
说明：
- `lambda k=k: k*k` 用默认参数固定当前的 `k`，否则三个 lambda 共用同一个变量；
- 裸线程里的未捕获异常只被 `threading.excepthook` 打印，`join()` 不会重新抛出，主线程照常往下走；
- 通过 `Future` 提交的任务，异常被保存，在 `result()` 时重新抛出，调用方才能处理；
- `with` 结束时池会等待所有任务完成并关闭线程。
