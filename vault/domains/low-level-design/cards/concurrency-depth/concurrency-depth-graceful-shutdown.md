---
id: concurrency-depth-graceful-shutdown
node: concurrency-depth.cancel-shutdown
type: qa
step: 3
---
## Q
服务收到关闭信号时，线程池里正在跑的任务和队列里排着的任务该怎么处理？`with ThreadPoolExecutor()` 退出时和 `shutdown(cancel_futures=True)` 各做了什么？

## A
**先决定排队的任务是做完还是丢掉，再关**

- **`with` 块退出 = `shutdown(wait=True)`**：不再接新任务，但队列里已有的全部做完才返回。实测 1 个 worker 提交 5 个任务，退出后 5 个全跑了；关闭时间 = 队列里剩下的全部耗时；
- **`shutdown(wait=True, cancel_futures=True)`**（3.9+）：队列里没开始的任务全部取消，正在跑的那个跑完。同样的实验只跑了第 0 个，其余 4 个 `cancelled() == True`；
- **正在跑的任务不会被打断**：要它尽快结束，同时给它协作式取消的信号（`Event`）；
- **被取消的任务，调用方的 `Future` 调 `result()` 会抛 `CancelledError`**：别让等待它的请求永远挂着，上层要处理；
- **自己用 `Queue` 写 worker**：放一个哨兵（`None`）每个 worker 一个，worker 看到就退出；队列里排在哨兵前的任务会先做完。3.13 起 `queue.Queue.shutdown()` 可以直接用；
- **顺序**：先停止接新请求，再关池，最后关它依赖的资源（连接池、文件）。反过来，正在跑的任务会撞到已经关掉的资源。

```python
import time
from concurrent.futures import ThreadPoolExecutor

ran = []
def job(i):
    time.sleep(0.2); ran.append(i)

ex = ThreadPoolExecutor(1)
fs = [ex.submit(job, i) for i in range(5)]
time.sleep(0.05)                                   # 让第 0 个开始
ex.shutdown(wait=True, cancel_futures=True)
print(ran, [f.cancelled() for f in fs])
# [0] [False, True, True, True, True]
```

**知识点：**取消、超时与关闭（Cancellation & Shutdown）
