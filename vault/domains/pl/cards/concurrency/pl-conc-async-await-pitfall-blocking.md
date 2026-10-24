---
id: pl-conc-async-await-pitfall-blocking
node: concurrency.async-await
type: qa
step: 8
---
## Q
在 `async` 函数里调用阻塞操作（比如同步 `time.sleep` 或长时间计算）为什么会拖垮整个程序？怎么避免？

## A
`async` 任务是协作式的：事件循环只有在任务执行到 `await` 时才能拿回控制权。任务里一个不让出的阻塞调用，会占住事件循环所在的整条线程，期间所有其他任务都停摆。

Python 实测（用忙等待模拟 100 毫秒的阻塞计算，10 个任务）：
```python
def block(ms):
    end = time.perf_counter() + ms / 1000
    while time.perf_counter() < end: pass

async def bad(i):  block(100); return i
async def good(i): await asyncio.sleep(0.1); return i
```
输出：`10 x bad: 1.00s`，`10 x good: 0.10s`。`bad` 把 10 个任务串成了 1 秒，`good` 的等待全部重叠，只要 0.1 秒。tokio 单线程运行时上用同样的忙等待也是 `10 blocking tasks: 1.00s`。

真实场景里的元凶：同步的网络库（`requests`）、`time.sleep`、大文件读写、哈希或压缩等 CPU 密集代码，以及在 Rust 里用 `std::thread::sleep` 或 `std::sync::Mutex` 持锁很久。

避免办法：
1. 换成异步版本的库和 API。
2. 把阻塞或 CPU 密集的部分丢给线程池：Python `await loop.run_in_executor(None, f)` 或 `asyncio.to_thread(f)`；tokio 用 `tokio::task::spawn_blocking`。
3. 用 asyncio 的调试模式或 tokio 的诊断工具找出「卡住循环」的调用。
