---
id: concurrency-depth-io-threads-vs-asyncio
node: concurrency-depth.selection
type: qa
step: 1
---
## Q
一个服务要并发调用 20 个各要等 0.2 秒的下游。顺序调用、线程池、`asyncio` 各要多久？线程池该开多大？什么时候不该选线程？

## A
**等 I/O 的任务，线程和协程都有效，按并发量和库支持来选**

- **实测（3.11，每个调用用 `sleep(0.2)` 代替，本机一次 sleep 实际约 0.33 s）**：顺序 6.6 s；线程池 8 个 1.0 s（20 个任务排三批）；线程池 20 个 0.34 s；`asyncio.gather` 0.20 s；
- **线程池大小就是并发上限**：开 8 个，第 9 个任务要等；开得和并发量一样大才能全部同时等；
- **线程的代价**：每个线程有自己的栈，启动 3000 个线程耗时 0.28 s，进程常驻内存从 38 MB 涨到 139 MB；一万个并发连接就不该开一万个线程；
- **协程的代价低**：一万个 `asyncio.sleep` 任务一起等，总共 0.28 s；一个协程只是一个对象，不占线程；
- **协程的前提**：整条调用链都是 `async`。用的客户端库只有阻塞版（`requests`、老的数据库驱动），在协程里调用会卡住事件循环，要么换库，要么丢给线程；
- **默认选线程池**：代码最简单，阻塞库直接用；并发量过千、或本来就是 `async` 生态（长连接网关、WebSocket），才上 `asyncio`。

```python
import asyncio, time
from concurrent.futures import ThreadPoolExecutor

def fetch(i):                  # 阻塞版：sleep 代替网络调用
    time.sleep(0.2); return i
async def afetch(i):           # 协程版：await 处让出事件循环
    await asyncio.sleep(0.2); return i
async def main():
    return sum(await asyncio.gather(*map(afetch, range(20))))

with ThreadPoolExecutor(20) as ex:
    print(sum(ex.map(fetch, range(20))))     # 190
print(asyncio.run(main()))                   # 190
```

**知识点：**线程、进程与协程的选择（Choosing a Model）
