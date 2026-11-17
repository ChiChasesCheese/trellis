---
id: concurrency-depth-cooperative-cancel
node: concurrency-depth.cancel-shutdown
type: qa
step: 1
---
## Q
Python 没有 `thread.kill()`。一个后台线程在循环里干活，怎么让它停下来？为什么用 `stop.wait(0.05)` 而不是 `time.sleep(0.05)`？

## A
**线程不能被强杀，只能让它自己看到停止信号并退出**

- **停止信号**：用 `threading.Event`；工作循环每一轮检查 `stop.is_set()`，设置后在这一轮结束时退出，`finally` 里的清理照常执行；
- **`stop.wait(0.05)` 当作可被打断的 sleep**：`stop` 一设置立刻返回，线程马上退出；`time.sleep(0.05)` 要睡满才看得见信号，间隔是 10 秒就要等 10 秒；
- **取消点要密**：一次操作超过几百毫秒，就要在操作内部（分块、分批）多检查几次，否则取消延迟等于一块的耗时；
- **阻塞在 I/O 上的线程看不到信号**：`socket.recv()` 这类调用要设超时，或者关掉它等待的对象，让调用抛异常返回；
- **守护线程（daemon）不是答案**：进程退出时守护线程被直接丢掉，`finally` 不执行、文件不 flush；
- **调用方 `join(timeout)`**：给停止一个期限，超时了就记日志，别永远等。

```python
import threading

stop = threading.Event()
log = []

def worker():
    while not stop.is_set():
        log.append("tick")           # 做一小块活
        stop.wait(0.05)              # 可被打断的 sleep
    log.append("cleanup")            # 退出前的收尾照常执行

t = threading.Thread(target=worker); t.start()
stop.set(); t.join(timeout=2)
print(t.is_alive(), log[-1])         # False cleanup
```

**知识点：**取消、超时与关闭（Cancellation & Shutdown）
