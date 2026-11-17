---
id: concurrency-depth-timeout-not-cancel
node: concurrency-depth.cancel-shutdown
type: qa
step: 2
---
## Q
`future.result(timeout=1)` 超时抛了 `TimeoutError`，背后的任务停了吗？`future.cancel()` 能取消什么？要给一个不可信的工具调用加硬超时，该怎么做？

## A
**超时只是调用方不等了，任务还在跑；硬超时要靠进程边界**

- **`result(timeout)` 超时**：抛 `TimeoutError`（3.11 里就是内置的那个），任务线程照样跑完，它占着的池里的位置也不释放；
- **`cancel()` 只能取消还没开始的**：队列里的返回 `True`，已经在跑的返回 `False`，实测同一个池里正在跑的 `cancel()` 是 `False`、排队的是 `True`；
- **所以超时设计要分两层**：调用方设等待上限，任务自己带截止时间（传 `deadline`，循环里检查，I/O 设超时）；
- **硬超时放进子进程**：线程杀不掉，进程可以。`subprocess.run(..., timeout=…)` 超时后会杀掉子进程再抛 `TimeoutExpired`；或者 `multiprocessing.Process.terminate()`；
- **子进程的代价**：启动、序列化、拿不到共享状态；只对风险大的调用（不可信代码、可能死循环的第三方）用；
- **超时后的清理**：被杀的子进程可能留下临时文件和半写的数据，设计时让调用的效果可丢弃（先写临时位置，成功再提交）。

```python
import subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(1) as ex:
    running = ex.submit(time.sleep, 0.3)
    queued = ex.submit(time.sleep, 0.3)
    time.sleep(0.05)                      # 让第一个开始
    print(running.cancel(), queued.cancel())   # False True

try:
    subprocess.run([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.3)
except subprocess.TimeoutExpired:
    print("child killed")                 # 硬超时：子进程被杀
```

**知识点：**取消、超时与关闭（Cancellation & Shutdown）
