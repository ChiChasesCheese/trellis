---
id: hi-c-lld-intro-b03-py-which-concurrency
node: lld.concurrency.intro.beyond
type: qa
step: 3
---
## Q
**并发入门 · Python：线程、进程、asyncio 怎么选**｜拓展 · 加分

Python 里线程、多进程、asyncio 各适合什么？GIL 怎样影响选择？

## A
**模式。** 按瓶颈选并发模型：I/O 密集用线程或协程，CPU 密集用多进程。

```python
import time
from concurrent.futures import ThreadPoolExecutor


def io_task(_: int) -> int:
    time.sleep(0.2)                  # 等待 I/O 时释放 GIL
    return 1


t0 = time.perf_counter()
with ThreadPoolExecutor(8) as ex:
    list(ex.map(io_task, range(8)))
elapsed = time.perf_counter() - t0
assert elapsed < 0.8                 # 八个各等 0.2 秒，重叠后约 0.2 秒而不是 1.6 秒
```
- **线程：** 阻塞 I/O 时释放 GIL，因此 I/O 密集可重叠；纯 Python 计算持有 GIL，多线程不会更快
- **多进程：** 每个进程自己的解释器与 GIL，能用满多核，代价是数据要序列化传递、启动慢
- **asyncio：** 单线程事件循环，成千上万连接开销小；但一处阻塞调用会卡住全部
- **共享状态风险：** 线程要锁；asyncio 在 `await` 点之间不会被打断，但跨 `await` 的"先检查后操作"仍会出问题
- **3.13 可选无 GIL 构建：** Python 3.13 起提供可选的无 GIL 构建，不是默认
